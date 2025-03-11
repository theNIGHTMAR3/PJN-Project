#!/usr/bin/python3
import pdfplumber
import re


def print_chapters(filename):
    """
    Print chapters in a PDF file (in Polish).
    :param filename: PDF file name
    :return: nothing
    Processing is simplified. The file may contain no chapters.
    """
    with pdfplumber.open(filename) as pdf:
        page_number = 1
        for p in pdf.pages:
            t = p.extract_text()
            for r in re.findall(r'^(Rozdział)\W(\w*)', t,
                                re.M | re.I):
                print(r[0], r[1], 'strona', page_number)
            page_number = page_number + 1


if (__name__ == "__main__"):
    import sys
    for filename in sys.argv[1:]:
        print(filename)
        print_chapters(filename)
