import dataclasses

from processor.main import BookCollection
from scrapper.main import BibleScrapper

if __name__ == '__main__':
#     #scrap
#     # BibleScrapper()
#
#     #process
    bc = BookCollection()
    b1 = list(bc.books.values())[0]
    print(dataclasses.asdict(b1))



