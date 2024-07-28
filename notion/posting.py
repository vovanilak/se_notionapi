import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from user.source import Row
from user.person import Person
from answer.test import Test
from answer.plot import test_result_img
from template.properties import info_prop
from dotenv import load_dotenv
from config.secret import *
from template.page import liga_n_staff
import json
import requests

load_dotenv()

def post_page2db(
    properties,
    page_content,
    database_id,
    emoji='😎',
    notion_token=NOTION_TOKEN
):
    url = f'https://api.notion.com/v1/pages'
    headers = {
        'Authorization': f'Bearer {notion_token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    dct = {
        "parent": {"database_id": database_id}, 
        "icon": {"type": "emoji", "emoji": emoji},
        "properties": properties,
        "children": page_content
    }
    response = requests.post(url, headers=headers, json=dct)
    return response.json()


if __name__ == '__main__':
    with open('./data/notion/new_version2.json', 'r') as f:
        data = json.load(f)
    row = Row('https://docs.google.com/spreadsheets/d/1hgC7-TI2INK2ZIU7gv82hALETcOnI35iRny5I3oV2KE/export?format=csv&gid=673713785',40)
    person = Person(row.data, row.answer, 'ID Legioner')
    test = Test(row.answer)
    '''imgs = test_result_img(
        person_name=person.title_value,
        grouped_metas=test.metas,
        levels=test.levels,
        result_sum=test.result_sum
    )''' 
    pg = liga_n_staff(
        main=data,
        levels=person.levels,
        grade_acse=test.grade_acse,
        metas=test.metas,
        img_links=['https://a.d-cd.net/bYAAAgBYPOA-1920.jpg']*6,
        test_result_sum=test.result_sum
    )
    pr = info_prop(
        title_value='Петя',
        title_name='ID Legioner',
        row_info=row.data,
        result_points=test.result_sum[0],
        levels=test.levels,
        grade_acse=test.grade_acse,
    )    
    pub = post_page2db(
        properties=pr,
        page_content=pg,
        database_id=DATABASE_LIGA,
        emoji='😎'
    ) 
    print(pub)