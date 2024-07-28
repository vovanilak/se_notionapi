import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_STAFF = os.getenv('DATABASE_STAFF')
DATABASE_LIGA = os.getenv('DATABASE_LIGA')
DATABASE_LIGA_PERSON = os.getenv('DATABASE_LIGA_PERSON')
URL_LIGA = os.getenv('URL_LIGA')
URL_STAFF = os.getenv('URL_STAFF')