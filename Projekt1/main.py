import pdfplumber
import os
import re

from getnews import parse_month
from ustawa import print_chapters
from proc_nkjp import find_morf

WORD = 'uczestnik'
pdf_file = 'D20211805Lj.pdf'
txt_file = 'D20211805Lj.txt'

cur_path = os.path.dirname(__file__)
pdf_file_path = os.path.join(cur_path, 'resources', pdf_file)
txt_file_path = os.path.join(cur_path, 'resources', txt_file)


def save_pdf_to_txt(file_path):
    print('Converting pdf to txt')
    with pdfplumber.open(file_path) as pdf:
        with open(txt_file_path, 'w', encoding='utf-8') as file:
            for page in pdf.pages:
                print('page: ', page.page_number)
                text = page.extract_text()
                if text:
                    file.write(text)


def KWIC(word, txt_path, context_size=33):
    print('Key word in context')
    fixed_word = rf'\W{word}\W(\w*)'
    # fixed_word = rf'\b{word}\b'
    regex = re.compile(fixed_word)
    with open(txt_path, 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', ' ')
        for match in regex.finditer(text):
            start = match.start()
            left_context = text[max(0, start - context_size):start]
            right_context = text[start + len(match.group()):start + len(match.group()) + context_size]
            print(f"{left_context}\t{match.group()}\t{right_context}")


def KWIC_extended(word, txt_path, context_size=33):
    print('Key word in context extended')
    regex = re.compile(word)
    with open(txt_path, 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', ' ')
        for match in regex.finditer(text):
            start = match.start()
            end = match.end()
            left_context = text[max(0, start - context_size):start]
            right_context = text[end:end + context_size]
            print(f"{left_context}\t{text[start:end]}\t{right_context}")


if __name__ == "__main__":
    # save_pdf_to_txt(pdf_file_path)
    # KWIC(WORD, txt_file_path)
    # KWIC_extended(WORD, txt_file_path)
    # parse_month(0,0)
    print_chapters(pdf_file_path)
    # find_morf('$NKJP/010-2-000000001')


