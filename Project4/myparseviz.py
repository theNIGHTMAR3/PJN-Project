#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 09:55:55 2024

@author: jandac
"""
import spacy
from spacy import displacy
import warnings
from collections import namedtuple
from termcolor import cprint
from nltk import Tree


def extract_deps(deps_parse):
    """
    Extract information from dependency graph arcs.

    Parameters
    ----------
    deps_parse : spacy object
        Result of spacy.displacy.parse_deps().

    Returns
    -------
    roots : List[int]
        Index of the root of the dependency parse tree.
    deps : list of Node
        List of Nodes containg for each word:
            - position of the word (word number in text)
            - list of Edges going to the left
            - list of Edges going to the right
            - number of incoming edges
            - index of the first word accessible from this word by Edge seq
            - index of the last word accessible from this word by Edge seq.

    """
    deps = {}
    roots = []
    Edge = namedtuple("Edge", ["target",    # target word index
                               "label"])
    Node = namedtuple("Node", ["word_pos",  # word index in the sentence
                               "left",      # list of edges going leftwards
                               "right",     # list of edges going rightwards
                               "links",     # number of links for the word
                               "lspan",     # index of the 1st word
                               "rspan"])    # index of the last word
    # print("deps_parse:", deps_parse)
    for w in range(len(deps_parse["words"])):
        deps[w] = Node(w, [], [], 0, w, w)
    for a in deps_parse["arcs"]:
        target = a["end"]   # index of the target word of the arc
        word_pos = a["start"]   # index of the start word of the arc
        if a["dir"] == "left":
            target = a["start"]
            word_pos = a["end"]
        if target not in deps:
            # initial span is just one word
            deps[target] = Node(target, [], [], 0, target, target)
        # increase the number of lionks for the target
        deps[target] = deps[target]._replace(links=deps[target].links + 1)
        if a["dir"] == "left":
            # Appemd the target to left dependencies
            deps[word_pos].left.append(Edge(target, a["label"]))
            if target < deps[word_pos].lspan:
                # And update the span of the word
                deps[word_pos] = deps[word_pos]._replace(lspan=target)
        else:
            # Append the target to right dependencies
            deps[word_pos].right.append(Edge(target, a["label"]))
            if target > deps[word_pos].rspan:
                # And update the span of the word
                deps[word_pos] = deps[word_pos]._replace(rspan=target)
    # Find root
    for word_pos in deps:
        if deps[word_pos].links == 0:
            roots.append(word_pos)
    return roots, deps


def comp_name(head_name):
    """
    Return traditional phrase name for the given head.

    Parameters
    ----------
    head_name : str
        Tag of the head word of the phrase.

    Returns
    -------
    str
        Traditional phrase name for a phrase with the given head.

    """
    phrase_name = {
        "NOUN": "NP",
        "PROPN": "NP",
        "PRON": "NP",
        "GER": "NP",
        "BREV": "NP",
        "VERB": "VP",
        "AUX": "VP",
        "FIN": "VP",
        "PRAET": "VP",
        "ADJ": "ADJP",
        "NUM": "ADJP",
        "ADV": "ADVP",
        "PART": "ADVP",
        "INTJ": "INTP",
        "DET": "DP",
        "CCONJ": "CP",
        "SCONJ": "CP",
        "ADP": "PP"
        }
    if head_name in phrase_name:
        return phrase_name[head_name]
    else:
        return ""


def print_ent(ent):
    """
    Print in color given named entitity and its label.

    Parameters
    ----------
    ent : spacy entitity
        A dict discribing a named entity.

    Returns
    -------
    None.

    """
    bkgr = {"orgName": "on_light_cyan",
            "placeName": "on_yellow",
            "geogName": "on_light_yellow",
            "persName": "on_blue",
            "date": "on_red"}
    if ent.label_ in bkgr:
        cprint(f"{ent.text} ", "black", bkgr[ent.label_], end="")
        cprint(f"{ent.label_}", "black", bkgr[ent.label_], attrs=["bold"],
               end=" ")
    else:
        cprint(f"{ent.text} ", "black", "on_light_grey", end="")
        cprint(f"{ent.label_}", "black", "on_light_grey", attrs=["bold"],
               end=" ")


def mark_components(deps_parse, deps):
    word_braks = {}
    Brakets = namedtuple("Brakets", ["left", "right"])
    for w1 in range(len(deps)):
        word_braks[w1] = Brakets([], [])
    for w1 in range(len(deps)):
        x = deps[w1].lspan
        lst = word_braks[x].left
        lst.append(w1)
        word_braks[x] = word_braks[x]._replace(left=lst)
        x = deps[w1].rspan
        lst = word_braks[x].right
        lst.append(w1)
        word_braks[x] = word_braks[x]._replace(right=lst)
    annot_sent = ""
    for w1 in word_braks:
        for b1 in reversed(word_braks[w1].left):
            p1 = deps_parse["words"][b1]["tag"]
            # Sprawdź, czy pierwszy token w składniku to przyimek (ADP)
            first_token_pos = deps[b1].lspan
            first_token_tag = deps_parse["words"][first_token_pos]["tag"]
            if first_token_tag == "ADP":
                annot_sent += "[PP "
            else:
                if b1 in word_braks[w1].right:
                    annot_sent += f"[{p1} "
                else:
                    annot_sent += f"[{comp_name(p1)} "
        annot_sent += deps_parse["words"][w1]["text"]
        for b1 in reversed(word_braks[w1].right):
            p1 = deps_parse["words"][b1]["tag"]
            # Sprawdź, czy pierwszy token w składniku to przyimek (ADP)
            first_token_pos = deps[b1].lspan
            first_token_tag = deps_parse["words"][first_token_pos]["tag"]
            if first_token_tag == "ADP":
                annot_sent += " PP]"
            else:
                if b1 in word_braks[w1].left:
                    annot_sent += f" {p1}]"
                else:
                    annot_sent += f" {comp_name(p1)}]"
        annot_sent += " "
    return annot_sent

def assemble_component(deps_parse, comp_root, deps):
    local_deps = []
    if deps[comp_root].lspan < deps[comp_root].rspan:
        # Sprawdź, czy pierwszy token to przyimek (ADP)
        first_token_pos = deps[comp_root].lspan
        first_token_tag = deps_parse["words"][first_token_pos]["tag"]
        if first_token_tag == "ADP":
            root_label = "PP"
        else:
            root_label = comp_name(deps_parse["words"][comp_root]["tag"])
        for d in deps[comp_root].left:
            local_deps.append(assemble_component(deps_parse, d[0], deps))
        local_deps.append(Tree(deps_parse["words"][comp_root]["tag"],
                              [deps_parse["words"][comp_root]["text"]]))
        for d in deps[comp_root].right:
            local_deps.append(assemble_component(deps_parse, d[0], deps))
    else:
        root_label = deps_parse["words"][comp_root]["tag"]
        local_deps.append(deps_parse["words"][comp_root]["text"])
    return Tree(root_label, local_deps)

def component_tree(deps_parse, roots, deps):
    """
    Print textual representation of component parse trees.

    Parameters
    ----------
    deps_parse : spaCy structure
        result of a dependency parsing.
    root : int
        word index for dependency parse root.
    deps : structure explained in extract_deps().
        structure containing information about dependency graph.

    Returns
    -------
    None.

    """
    for root in roots:
        local_deps = []
        for d in deps[root].left:
            local_deps.append(assemble_component(deps_parse, d[0], deps))
        local_deps.append(Tree(deps_parse["words"][root]["tag"],
                               [deps_parse["words"][root]["text"]]))
        for d in deps[root].right:
            local_deps.append(assemble_component(deps_parse, d[0], deps))
        t = Tree("S", local_deps)
        t.pretty_print()


def annotate_sentence_components(sent):
    """
    Insert brackets into a text to mark syntactic components.

    Parameters
    ----------
    sent : str
        Text to process (to annotate).

    Returns
    -------
    str
        Annotated text.

    """
    nlp = spacy.load("pl_core_news_sm")
    doc = nlp(sent)
    deps_parse = displacy.parse_deps(doc)
    _, deps = extract_deps(deps_parse)
    return mark_components(deps_parse, deps)


if __name__ == "__main__":
    line = input("Sentence: ")
    while line != "":
        print(annotate_sentence_components(line))
        line = input("Sentence: ")