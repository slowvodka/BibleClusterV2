from hebrew_tokenizer.hebrew_tokenizer import HebTokenizer
from logger import LOGGER
import pathlib
from typing import Union, Tuple

from project_consts import DEFAULT_INDEX, EXPRESSIONS, FILES_PATH
import os
import re
from pathlib import Path
from dataclasses import dataclass, field

def list_files(directory):
    file_paths = []  # create an empty list to store file paths
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)  # get the full path of the file
            file_paths.append(filepath)  # add the file path to the list
    return tuple(sorted(file_paths))




class BookStatAnalyzer:
    def __init__(self, raw_text):
        return


@dataclass
class Book:
    title: str
    raw_text: str
    index : int
    clean_text : str = field(init=False)
    full_word_list : list[str] = field(init=False)
    verses_list : list[str] = field(init=False)
    word_count: int = field(init=False)
    unique_word_count: int = field(init=False)
    num_of_words_in_text: int = field(init=False)
    num_of_unique_words_in_text: int = field(init=False)
    num_of_parshiya_ptucha: int = field(init=False)
    num_of_parshiya_stuma: int = field(init=False)

    def __post_init__(self):

        self.tokenizer = HebTokenizer()
        self.clean_text = self.create_clean_text()

        self.full_word_list = self.tokenizer.get_words(self.clean_text)
        self.verses_list = self.clean_text.split('.')

        self.num_of_words_in_text = None
        self.num_of_unique_words_in_text = None
        self.num_of_parshiya_ptucha = None
        self.num_of_parshiya_stuma = None


        # self.create_stats()


    def create_clean_text(self, expressions=EXPRESSIONS):
        '''
        remove numbers and brackets and clean text
        '''
        text = self.raw_text

        # replace characters i saw the tokenizer have problems with
        text = text.replace('-', ' ').replace(':', ' ')
        for expression in expressions:
            text = re.sub(expression, '', text)
        # remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        clean_text = self.tokenizer.sanitize(text, remove_diacritics=True, bible_makaf=False)
        return clean_text



    # def create_stats(self):
    #     self.calc_num_of_words_in_text()
    #     self.calc_num_of_unique_words_in_text()
    #     self.calc_num_of_parshiyot_in_text()
    #
    # def calc_num_of_words_in_text(self):
    #     self.num_of_words_in_text = len(self.full_word_list)
    #
    # def calc_num_of_unique_words_in_text(self):
    #     self.num_of_unique_words_in_text = len(set(self.full_word_list))
    #
    # def calc_num_of_parshiyot_in_text(self):
    #     self.num_of_parshiya_ptucha = self.raw_text.count("{פ}")
    #     self.num_of_parshiya_stuma = self.raw_text.count("{ס}")



class BibleProcessor:
    def __init__(self, file_paths: Tuple[Union[str, pathlib.Path]] = list_files(FILES_PATH)):
        self.file_paths = file_paths
        self.bible_books = {}

    def get_book_as_text(self, path: Union[str, pathlib.Path]):
        with open(path, encoding='utf-8') as file:
            text = file.read()
        return text

    def text_and_name_to_book(self, path: Union[str, pathlib.Path]):
        name = Path(path).name.split('.')[0]
        text = self.get_book_as_text(path)
        LOGGER.info(f"{name} proccessed and cleaned")
        book = Book(name, text)
        self.bible_books[book.name] = book

    def process(self, test_mode=True):
        for path_book in self.file_paths:
            self.text_and_name_to_book(path_book)
            if test_mode:
                break


