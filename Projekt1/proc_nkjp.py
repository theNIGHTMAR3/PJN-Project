#!/usr/bin/python3
import os
import xml.etree.ElementTree as ET
import sys


def tag_uri_and_name(elem):
    """
    Divide element name with a prefix being namespace
    into namespace uri and tag.
    :param elem: element in an xml tree
    :return: a 2-tuple: namespace uri and tag
    """
    if elem.tag[0] == "{":
        uri, ignore, tag = elem.tag[1:].partition("}")
    else:
        uri = None
        tag = elem.tag
    return uri, tag


def get_next_morph(filename):
    """
    Get the next word with all its annotations.
    :param filename: file named ann_morphosyntax.xml in $NKJP
    :return: a 3-tuple with the word, its possible interpretations,
    and the correct interpretation
    """
    events = ["start-ns", "start", "end"]
    xmlns = ""
    path = []
    ctags = []
    msds = []
    interps = []
    disamb = []
    base = ""
    orth = ""
    for (event, elem) in ET.iterparse(filename, events=events):
        # React to opening and closing of tags
        tag = ""
        if event == "start-ns":
            if elem[0] == "":
                xmlns = elem[1]
        elif event == "start":
            # For tag openings, construct a path to the current tag.
            # The path is a list.
            # Use either tags, or tags concatenated with some attribute
            # values (e.g. "type", "name", or "value") as path items.
            # Store path current leaves in variable `branch'
            ns, tag = tag_uri_and_name(elem)
            branch = tag
            if tag == "fs":
                branch = tag + ":" + elem.attrib["type"]
            elif tag == "f":
                branch = tag + ":" + elem.attrib["name"]
            elif tag == "symbol":
                if path[-1] == "f:ctag":
                    # The part-of-speech tag for the word
                    ctags.append(elem.attrib["value"])
                elif (path[-1] == "f:msd"
                      or path[-1] == "vAlt" and path[-2] == "f:msd"):
                    # Possible morphosyntactic descriptions of the word,
                    # as obtained from a morphological analyzer
                    msd = elem.attrib["value"]
                    # They are appended to the part-of-speech
                    msd_suffix = msd
                    if msd != "":
                        msd_suffix = ":" + msd
                    for c in ctags:
                        # Append msds to each part-of-speech unless empty
                        if c == "ign":
                            interps.append("ign")
                        else:
                            interps.append(base + ":" + c + msd_suffix)
                    msds.append(elem.attrib["value"])
            path.append(branch)
        elif event == "end":
            branch = path.pop()
            if branch == "f:interps":
                # The end of possible interpretations
                # Clear the list
                ctags = []
                msds = []
            elif branch == "string":
                # Assign extracted values
                if path[-1] == "f:orth":
                    # Word in the text
                    orth = elem.text
                elif path[-1] == "f:base":
                    # Lemma
                    base = elem.text

                #####################################
                # 3 steps up
                elif path[-3] == "f:disamb":
                    disamb = elem.text
                #####################################

            elif branch == "seg":
                yield orth, interps, disamb
                orth = ""
                interps = []
                disamb = ""



def find_morf(input):
    cur_path = os.path.dirname(__file__)
    file_path = os.path.join(cur_path, 'resources', input, 'ann_morphosyntax.xml')
    mm = get_next_morph(file_path)
    for m in mm:
        orth, interps, disamb = m
        print("orth=", orth, ", interps=", interps, ", disamb=", disamb, sep='')



if (__name__ == "__main__"):
    input =  '$NKJP/010-2-000000001'
    # for setname in input:
    #     print(setname)
    #     mm = get_next_morph("C:/Users/micha/Desktop/Informatyka/PJN-Project/Projekt1/resources/ann_morphosyntax.xml")
    #     # mm = get_next_morph(setname + "/ann_morphosyntax.xml")
    #     for m in mm:
    #         orth, interps, disamb = m
    #         print("orth=", orth, ", interps=", interps, ", disamb=", disamb,
    #               sep='')

    cur_path = os.path.dirname(__file__)
    file_path = os.path.join(cur_path, 'resources', input,'ann_morphosyntax.xml')


    print('START')
    mm = get_next_morph(file_path)
    # mm = get_next_morph(setname + "/ann_morphosyntax.xml")
    for m in mm:
        orth, interps, disamb = m
        print("orth=", orth, ", interps=", interps, ", disamb=", disamb, sep='')

