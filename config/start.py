import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from config.secret import *

JSON_FILE = 'data/notion/new_version2.json'

whoau = {
    'Легионер': {
        'column_name': 'ID Legioner',
        'url': URL_LIGA,
        'db': DATABASE_LIGA,
    },

    'Штатный Сотрудник': {
        'column_name': 'Name',
        'url': URL_STAFF,
        'db': DATABASE_STAFF,
    }
}


