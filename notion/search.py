import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import requests
from config.secret import *

def query_notion(
    self,
    val, # какое значение искать
    column='ID Legioner', # в какой колонке искать
    notion_token=NOTION_TOKEN, 
    database_id=DATABASE_LIGA, 
):
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    headers = {
        'Authorization': f'Bearer {notion_token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    data = {
        'filter': {
            'property': column,
            'title': {
                'equals': val
            }
        }
    }
    response = requests.post(url, headers=headers, json=data).json()
    url = ''.join(response['results'][0]['id'].split('-'))
    return url