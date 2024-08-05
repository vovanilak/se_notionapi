import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from config.secret import *

JSON_FILE = 'data/notion/new_version2.json'
who_prop = {
    'Легионер': 'ID Legioner',
    'Штатный Сотрудник': "Name",
}

who_db = {
    'Легионер': DATABASE_LIGA,
    'Штатный Сотрудник': DATABASE_STAFF,
}

who_link = {
    'Легионер': URL_LIGA,
    'Штатный Сотрудник': URL_STAFF,
}

