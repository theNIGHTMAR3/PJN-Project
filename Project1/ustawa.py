#!/usr/bin/python3
import pdfplumber
import re
import os
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal, LTChar
from typing import Iterable, Any
from pathlib import Path

# pdf_file = 'D20211805Lj.pdf'
# cur_path = os.path.dirname(__file__)
# pdf_file_path = os.path.join(cur_path, 'resources', pdf_file)

def print_chapters(filename):
    """
    Print chapters in a PDF file (in Polish).
    :param filename: PDF file name
    :return: nothing
    Processing is simplified. The file may contain no chapters.
    """
    print('Processing chapters from given file')
    print(filename)

    cur_path = os.path.dirname(__file__)
    pdf_file_path = os.path.join(cur_path, 'resources', filename)

    print(extract_title(pdf_file_path))

    with pdfplumber.open(pdf_file_path) as pdf:
        page_number = 1
        for p in pdf.pages:
            t = p.extract_text()
            for line in t.split('\n'):
                match = re.match(r'^(Tytuł|Część|Księga|Dział|Rozdział|Oddział)\W(\w*)', line, re.M | re.I)
                if match and (match.group(1)[0].isupper() and (match.group(2)[0].isupper() or match.group(2)[0].isdigit())):
                    print(match.group(1), match.group(2), 'strona', page_number)
            page_number += 1


def extract_title(filename):
    """
    Extract the title written in Times 12px font from the first page of a PDF file.
    :param filename: PDF file name
    :return: Title as a string
    """
    path = Path(filename).expanduser()
    pages = extract_pages(path)
    title = ''
    for page in pages:
        for element in page:
            if isinstance(element, LTTextBoxHorizontal):
                for text_line in element:
                    if 'TYTUŁ WSTĘPNY' in text_line.get_text():
                        return title.strip()
                    for character in text_line:
                        if isinstance(character, LTChar):
                            if character.fontname in ['ABCDEE+Times', 'ABCDEE+Times,Bold'] and round(character.size) == 12:
                                title = title + character.get_text()
        break  # Only process the first page
    return None


def show_ltitem_hierarchy(o: Any, depth=0):
    """Show location and text of LTItem and all its descendants"""
    if depth == 0:
        print('element                        font                  stroking color  text')
        print('------------------------------ --------------------- --------------  ----------')

    print(
        f'{get_indented_name(o, depth):<30.30s} '
        f'{get_optional_fontinfo(o):<20.20s} '
        f'{get_optional_color(o):<17.17s}'
        f'{get_optional_text(o)}'
    )
    count = 0
    if isinstance(o, Iterable):
        for i in o:
            show_ltitem_hierarchy(i, depth=depth + 1)
            count=count+1
            if count==20:
                break

def get_indented_name(o: Any, depth: int) -> str:
    """Indented name of class"""
    return '  ' * depth + o.__class__.__name__

def get_optional_fontinfo(o: Any) -> str:
    """Font info of LTChar if available, otherwise empty string"""
    if hasattr(o, 'fontname') and hasattr(o, 'size'):
        return f'{o.fontname} {round(o.size)}pt'
    return ''

def get_optional_color(o: Any) -> str:
    """Font info of LTChar if available, otherwise empty string"""
    if hasattr(o, 'graphicstate'):
        return f'{o.graphicstate.scolor}'
    return ''


def get_optional_text(o: Any) -> str:
    """Text of LTItem if available, otherwise empty string"""
    if hasattr(o, 'get_text'):
        return o.get_text().strip()
    return ''


if (__name__ == "__main__"):
    # path = Path('resources/D20211805Lj.pdf').expanduser()
    # pages = extract_pages(path)
    # show_ltitem_hierarchy(pages)

    print_chapters('none')


