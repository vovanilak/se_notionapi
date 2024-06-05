import requests
from dotenv import load_dotenv
import os

load_dotenv()

test_prop = {
    'properties': {
            "title": [
                {
                    "text": {
                        "content": 'lool'
                    }
                }
            ],
            "Дивизион": {
                'name': 'Системный анализ'
            },
            "Профиль специалиста": {
                'name': 'Системный аналитик'
            }
        }
}

test_page = [ {"type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "YEEES"}, "plain_text": "YEEES"}], "is_toggleable": False, "color": "default"}}]

def page_db(
    notion_token: str, 
    database_id: str, 
    proporties: dict, 
    page: list
    ):

    url = f'https://api.notion.com/v1/pages'
    headers = {
        'Authorization': f'Bearer {notion_token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }
    db = {
        "parent": {
            "database_id": database_id
            }, 
        "icon": {
            "type": "emoji", 
            "emoji": "😎"
        },
        }
    result = {**db, **proporties, "children": page}
    response = requests.post(url, headers=headers, json=result)

    if response.status_code == 200:
        print("Страница успешно создана в Notion!")
    else:
        print(f"Ошибка при создании страницы. Код ответа: {response.status_code}, Текст ответа: {response.text}")


page_db(
    notion_token=os.getenv('NOTION_TOKEN'),
    database_id=os.getenv('DATABASE_STAFF'),
    page=test_page,
    proporties=test_prop,

)

def page_rel_db(self, notion_token, database_id, database_parent):

    url = f'https://api.notion.com/v1/pages'
    headers = {
        'Authorization': f'Bearer {notion_token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }
    db = {"parent": {"database_id": database_id}}
    prop = self.get_personal_proporties(database_parent)
    result = {**db, **prop}
    response = requests.post(url, headers=headers, json=result)

    if response.status_code == 200:
        print("Страница успешно создана в Notion!")
    else:
        print(f"Ошибка при создании страницы. Код ответа: {response.status_code}, Текст ответа: {response.text}")