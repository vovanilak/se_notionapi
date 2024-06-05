import requests
from dotenv import load_dotenv
import os
from pprint import pprint, pformat
import json
from get_template import bytes_to_dict, traverse_dict, pprint2file
import os

load_dotenv()

NOTION_TOKEN=os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('DATABASE_LIGA')

WORKDIR = 'notionapi/notion'

if os.path.exists(WORKDIR) and os.path.isdir(WORKDIR):
    os.chdir(WORKDIR)

url = f'https://api.notion.com/v1/pages'
headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
}

with open('../data/test2.json', 'r') as file:
    result = json.load(file)


notion_data = {
    "parent": {"database_id": DATABASE_ID},
    "properties": {
        "title": [
            {
                "text": {
                    "content": "00"
                }
            }
        ]
    },
    "children": result[:101]
}

response = requests.post(url, headers=headers, json=notion_data)
#result = bytes_to_dict(response.content)['properties']
#print(result.keys())

#pprint(notion_data)

#with open('proporties.json', 'w') as inp:
#    json.dump(result, inp)

#    ['My grade', 'Образование', 'Дивизион', 'Ожидания ЗП', 'ID Legioner', 'Профиль специалиста', 'Пол', 'Формат работы', 'Тип метасотрудника', 'Статус поиска', 'AC/SE grade', 'Tags', 'Возраст (лет)', 'Город', 'URL', 'Опыт работы в ИТ', 'Домен', 'Points']

if response.status_code == 200:
    print("Страница успешно создана в Notion!")
else:
    print(f"Ошибка при создании страницы. Код ответа: {response.status_code}, Текст ответа: {response.text}")
