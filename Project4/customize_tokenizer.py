import spacy
from spacy.tokenizer import Tokenizer
from spacy.matcher import Matcher
from spacy.language import Language
from spacy.tokens import Token
import re

print("before herference import")
import herference
cr = herference.Herference()

print("Herference loaded")
nlp = spacy.load("pl_core_news_sm")
nlp.add_pipe("herference")

text = cr.predict('Twój przykładowy tekst, którego analizę chcesz przeprowadzić.')
print(text)
doc = nlp(text)

for cluster in text.clusters:
    for mention in cluster:
        print(f"{mention.text} {mention.subtoken_indices}")

print(text.tokenized)



def date_tokenizer(nlp):
    date_pattern = re.compile(r"\b\d{2}\.\d{2}\.\d{4}\b")

    old_tokenizer = nlp.tokenizer
    nlp.tokenizer = Tokenizer(
        nlp.vocab,
        rules=old_tokenizer.rules,
        prefix_search=old_tokenizer.prefix_search,
        suffix_search=old_tokenizer.suffix_search,
        infix_finditer=old_tokenizer.infix_finditer,
        token_match=date_pattern.match,  # Ustawienie wzorca token_match
        url_match=old_tokenizer.url_match,
    )

    Token.set_extension("is_date", default=False, force=True)

    # Add a pipeline component to tag dates
    @Language.component("date_tagger")
    def date_tagger(doc):
        for token in doc:
            if date_pattern.fullmatch(token.text):  # Full match for dates
                token.tag_ = "DATE"  # Set POS to DATE
                token._.is_date = True  # Mark as a date
        return doc

    # Add the component to the pipeline
    nlp.add_pipe("date_tagger", last=True)


# def number_tokenizer(nlp):
#     number_pattern = re.compile(r"\b\d{1,3}(?:\s\d{3})*\b")
#
#     old_tokenizer = nlp.tokenizer
#     nlp.tokenizer = Tokenizer(
#         nlp.vocab,
#         rules=old_tokenizer.rules,
#         prefix_search=old_tokenizer.prefix_search,
#         suffix_search=old_tokenizer.suffix_search,
#         infix_finditer=old_tokenizer.infix_finditer,
#         token_match=number_pattern.match,
#         url_match=old_tokenizer.url_match,
#     )


def number_tokenizer(nlp):
    # Regular expression to match numbers with spaces (e.g., 1 234 567)
    number_pattern = re.compile(r"\b\d{1,3}(?:\s\d{3})*\b")

    # Create a new tokenizer with the custom token_match
    old_tokenizer = nlp.tokenizer
    nlp.tokenizer = Tokenizer(
        nlp.vocab,
        rules=old_tokenizer.rules,
        prefix_search=old_tokenizer.prefix_search,
        suffix_search=old_tokenizer.suffix_search,
        infix_finditer=old_tokenizer.infix_finditer,
        token_match=number_pattern.match,  # Match entire numbers with spaces
        url_match=old_tokenizer.url_match,
    )

    # Add a custom extension for identifying numbers
    Token.set_extension("is_number", default=False, force=True)

    # Pipeline component to tag numbers as NUM
    @Language.component("number_tagger")
    def number_tagger(doc):
        for token in doc:
            if number_pattern.fullmatch(token.text):  # Ensure full match
                token.pos_ = "NUM"  # Set POS to NUM
                token._.is_number = True
        return doc

    # Add the component to the pipeline
    nlp.add_pipe("number_tagger", last=True)




# date_tokenizer(nlp)
# number_tokenizer(nlp)

# Przykładowy tekst
doc = nlp("W 13.11.2023 populacja wynosiła 1 234 567 osób.")

# Wyświetlenie tokenów
# print([token.text for token in doc])

# for token in doc:
#     print(f"{token.text:<12} | POS: {token.pos_}")

for token in doc:
    print(f"{token.text:<12} | POS: {token.pos_} | TAG: {token.tag_}")
