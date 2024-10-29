from processor.main import BibleProcessor
from scrapper.main import BibleScrapper

if __name__ == '__main__':
    #scrap
    # BibleScrapper()

    #process
    bb= BibleProcessor()
    bb.process()
    print((bb.bible_books))