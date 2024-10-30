
#scrapper related
NAME = 'name'
LINKS = 'links'
RAW_TEXT_DIR = 'raw_text_dir'
scrap_url = "https://mechon-mamre.org"

#process related
import os

FILES_PATH = f"{os.getcwd()}/{RAW_TEXT_DIR}"

EXPRESSIONS = (r'\b\d+\b', r'\{.*?\}', r'\(.*?\)',r'[;,-]','(|[|{|}|]|)')