from hebrew_tokenizer.hebrew_tokenizer import HebTokenizer
from logger import LOGGER
import pathlib
from typing import Union
import pandas as pd


from project_consts import EXPRESSIONS, FILES_PATH
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

@dataclass()
class TextStatAnalyzer:
    raw_text: str
    clean_text: str
    verses_list: list[str]
    words_list: list[str]

    def __post_init__(self):
        self.clean_text_lengh = len(self.clean_text)
        self.unique_words_list = list(set(self.words_list))
        self.words_count = len(self.words_list)
        self.unique_words_count = len(self.unique_words_list)
        self.parshiya_ptucha_count = self.raw_text.count("{פ}")
        self.parshiya_stuma_count = self.raw_text.count("{ס}")
        self.words_value_counts = pd.Series(self.words_list,name='word').value_counts().rename('count').reset_index()



@dataclass
class Book:
    title: str
    raw_text: str
    index : int
    clean_text : str = field(init=False)
    full_word_list : list[str] = field(init=False)
    verses_list : list[str] = field(init=False)

    clean_text_lengh : int = field(init=False)
    unique_words_list : list[str] = field(init=False)
    words_count : int = field(init=False)
    unique_words_count : int = field(init=False)
    parshiya_ptucha_count : int = field(init=False)
    parshiya_stuma_count : int = field(init=False)
    words_value_counts : pd.DataFrame = field(init=False)

    def __post_init__(self):

        self.tokenizer = HebTokenizer()
        self.clean_text = self.create_clean_text()
        self.full_word_list = self.tokenizer.get_words(self.clean_text)
        self.verses_list = [verse.strip() for verse in self.clean_text.split('.') if verse != ' ']

        analyzer = TextStatAnalyzer(raw_text=self.raw_text, clean_text=self.clean_text, verses_list=self.verses_list, words_list =self.full_word_list)

        self.clean_text_lengh = analyzer.clean_text_lengh
        self.unique_words_list =  analyzer.unique_words_list
        self.words_count =  analyzer.words_count
        self.unique_words_count =  analyzer.unique_words_count
        self.parshiya_ptucha_count = analyzer.parshiya_ptucha_count
        self.parshiya_stuma_count = analyzer.parshiya_stuma_count
        self.words_value_counts = analyzer.words_value_counts


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


class BookCollection:
    def __init__(self, file_paths: tuple[str, pathlib.Path] = list_files(FILES_PATH)):
        self.number_of_books = 0
        self.file_paths = file_paths
        self.books = {}

        for path_book in self.file_paths:
            self.text_and_name_to_book(path_book)


            #change me!
            break

    def get_book_as_text(self, path: Union[str, pathlib.Path]):
        with open(path, encoding='utf-8') as file:
            text = file.read()
        return text

    def text_and_name_to_book(self, path: Union[str, pathlib.Path]):
        book_title = Path(path).name.split('.')[0]
        book_raw_text = self.get_book_as_text(path)
        LOGGER.info(f"{book_title} proccessed and cleaned")
        self.number_of_books+=1
        book = Book(book_title, book_raw_text, self.number_of_books)
        self.books[book.title] = book
        LOGGER.info(f"{book_title} logged to collection.")




