import os
from bs4 import BeautifulSoup
import requests
import codecs
from scrapper.scrapper_consts import scrap_url, RAW_TEXT_DIR
from logger import LOGGER
import re


class BibleScrapper:
    '''
    class to keep all hrefs related to a book
    '''

    def __init__(self):
        self.number_of_books = 0
        self.bible = {}
        self.save_path = f"{RAW_TEXT_DIR}"
        self.generate_bible()

    def get_and_fix_book_name(self,all_h1_elements):
        book_name = [h1 for h1 in all_h1_elements if not h1.has_attr('class')][-1].get_text()
        book_name = book_name.replace('/', " ")
        book_name = re.sub(r'\s+', ' ', book_name)
        book_name = book_name.replace(' ', "_")
        return  book_name

    def generate_bible(self):

        while(self.number_of_books <=38):
            self.number_of_books+=1
            book_num = self.number_of_books

            if book_num <= 5:
                url = f"{scrap_url}/i/t/t{str(book_num).zfill(2)}.htm"
            elif book_num <= 35:
                url = f"{scrap_url}/i/t/k/k{str(book_num).zfill(2)}.htm"
            elif book_num == 36:
                url = f"{scrap_url}/b/h/h11.htm"
            elif book_num == 37:
                url = f"{scrap_url}/b/f/f11.htm"
            elif book_num == 38:
                url = f"{scrap_url}/b/h/h51.htm"
            else:
                raise ValueError(f'query index is out of range: {book_num}')

            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            for bold_tag in soup.find_all('b'):
                bold_tag.string = '1'


            if any(ext in url for ext in ["/b/h/h11.", "/b/f/f11.", "/b/h/h51."]):
                title_element = 'title'
                text_element = 't'
            else:
                title_element = 'h1'
                text_element = 'ct'

            all_h1_elements = soup.find_all(title_element)
            book_name = self.get_and_fix_book_name(all_h1_elements)

            LOGGER.info(f'now query: {book_name}')

            ct_paragraphs = soup.find_all('p', class_=lambda x: x and text_element in x.split())
            raw_text = ''
            for paragraph in ct_paragraphs:
                text = paragraph.get_text()
                raw_text = raw_text + ' ' + text

            self.save_text(book_num, book_name, raw_text)

            if book_num == 1:
                break

    def save_text(self, book_num, book_name, raw_text):
        # Open a new file with utf-8 encoding
        LOGGER.info(f'saving raw text of book {book_num, book_name}')

        if not os.path.exists(self.save_path):
            LOGGER.warning(f"{self.save_path} not exists, created new dir")
            os.makedirs(self.save_path)

        with codecs.open(f"{self.save_path}/{book_num}_{book_name}.txt", "w", encoding="utf-8") as f:
            # Write the Hebrew text to the file
            f.write(raw_text)

        LOGGER.info(f"{book_name} was added")