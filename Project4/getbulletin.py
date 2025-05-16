#!/usr/bin/python
import locale
from bs4 import BeautifulSoup
# import re
import urllib.request
import spacy
from spacy import displacy
import warnings
from myparseviz import mark_components, print_ent, extract_deps, component_tree
import re
from spacy.tokenizer import Tokenizer
from spacy.language import Language


nlp = spacy.load("pl_core_news_sm")


# Add a custom entity ruler to match dates
ruler = nlp.add_pipe("entity_ruler", before="ner")
date_pattern = [{"label": "DATE", "pattern": [{"TEXT": {"REGEX": r"^\d{1,2}\.\d{1,2}\.\d{4}$"}}]}]
ruler.add_patterns(date_pattern)

# date tokenizer
def custom_tokenizer(nlp):
    prefix_re = spacy.util.compile_prefix_regex(nlp.Defaults.prefixes)
    suffix_re = spacy.util.compile_suffix_regex(nlp.Defaults.suffixes)
    infixes = [inf for inf in nlp.Defaults.infixes if not re.search(r'\s', inf)]
    infix_re = spacy.util.compile_infix_regex(infixes)  #

    date_regex = re.compile(r'^\d{1,2}\.\d{1,2}\.\d{4}$')

    # update tokenizer
    nlp.tokenizer = Tokenizer(
        nlp.vocab,
        prefix_search=prefix_re.search,
        suffix_search=suffix_re.search,
        infix_finditer=infix_re.finditer,
        token_match=date_regex.match
    )

    # change tag
    @Language.component("set_date_tag")
    def set_date_tag(doc):
        for ent in doc.ents:
            if ent.label_ == "DATE":
                for token in ent:
                    token.tag_ = "DATE"
        return doc

    nlp.add_pipe("set_date_tag", last=True)


def process_text(text):
    """
    Print POS lemmas & categories of words, parse tree and named entities.

    Parameters
    ----------
    text : str
        Text to process.

    Returns
    -------
    None.

    """
    # switch off annoying SpaCy warinings
    warnings.filterwarnings("ignore")
    if text == "":
        return
    # Print the text as is.
    print("\n\nOriginal text:")
    print(text)
    # Print words, lemmas, POS tags, and explanations for POS tags
    print("\nWords, lemmas, POS tags, explanations for POS tags:")
    # text = "Spotkanie odbędzie się 12.05.2023. To jest jedna liczba: 12 451 987. Kot jest na stole."
    doc = nlp(text)
    number_start_regex = re.compile(r"\d{1,3}$")
    number_group_regex = re.compile(r"^\d{3}")

    # merge NUM tags into one token
    # ###################################################
    saved_indexes = []
    i = 0
    while i < len(doc):
        token = doc[i]
        # first number
        if not saved_indexes:
            if re.search(number_start_regex, token.text):
                saved_indexes = [i]
        # next numbers
        else:
            if re.search(number_group_regex, token.text):
                saved_indexes.append(i)
            else:
                # finish, check if got any numbers
                if len(saved_indexes) > 1:
                    with doc.retokenize() as retokenizer:
                        span = doc[saved_indexes[0]:saved_indexes[-1]+1]
                        retokenizer.merge(span, attrs={"POS": "NUM"})
                    i -= (len(saved_indexes) - 1)
                saved_indexes = []
        i += 1

    # last tokens, check if got any numbers
    if len(saved_indexes) > 1:
        with doc.retokenize() as retokenizer:
            span = doc[saved_indexes[0]:saved_indexes[-1]+1]
            retokenizer.merge(span, attrs={"POS": "NUM"})

    # ###################################################

    n = 0
    for token in doc:
        n += 1
        print(f"{n:2}.", token.text, token.lemma_,
              token.tag_, spacy.explain(token.tag_))
    # Print a parse tree with components.
    deps_parse = displacy.parse_deps(doc)
    roots, deps = extract_deps(deps_parse)
    print("\nComponents marked in the text:")
    print(mark_components(deps_parse, deps))
    print("\nComponents as a tree:")
    component_tree(deps_parse, roots, deps)
    n = 0
    # Print the text with named entities marked and categorized
    for ent in doc.ents:
        if ent.start_char > n:
            print(doc.text[n:ent.start_char], end=" ")
        print_ent(ent)
        n = ent.end_char
    if n < len(doc.text):
        print(doc.text[n:])
    else:
        print()


def read_category(element):
    """
    Process a single category of news in the bulletin.

    Parameters
    ----------
    element : bs4 element type
        root element of the category.

    Returns
    -------
    None.

    """
    h3 = element.find("h3", class_="bulletin__category")
    if h3 is not None:
        category = h3.text
        print(f"\n\nKategoria: {category}")
    # options = {"compact": True}
    d1 = element.find("div", class_="bulletin__articles")
    for a1 in d1.find_all("article", class_="bulletin__article article"):
        h4 = a1.find("h4", class_="article__title")
        if h4 is not None:
            art_tit = h4.text
            print(f"\n\n------ tytuł: {art_tit}")
        d2 = a1.find("div", class_="article__content")
        without_paragraphs = True
        for t1 in d2.find_all(["p", "li"]):
            without_paragraphs = False
            process_text(t1.text.strip())
        if without_paragraphs:
            process_text(d2.text.strip())


def read_bulletin(edition):
    """
    Read one edition of the GUT bulletin.

    Parameters
    ----------
    edition : str
        Edition number or current number.

    Returns
    -------
    None.

    """
    base_url = "https://biuletyn.pg.edu.pl"
    url = f"{base_url}/{edition}"
    with urllib.request.urlopen(url) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        d1 = soup.find("div", class_="row bulletin")
        for d2 in d1.find_all("div", class_="bulletin__categories"):
            read_category(d2)


if (__name__ == "__main__"):
    custom_tokenizer(nlp)
    import argparse
    locale.setlocale(locale.LC_ALL, "pl_PL.utf8")
    desc = "Process a GUT bulletin."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("number", type=int, nargs="?",
                        help="Bulletin number.")
    args = parser.parse_args()
    nr = "numer_aktualny"
    if "number" in args and args.number is not None:
        nr = f"biuletyn-{args.number}"
    read_bulletin(nr)