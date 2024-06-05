import os
import json
from dotenv import load_dotenv
import requests
from pprint import pprint

load_dotenv()


class Parser:
    def __init__(
        self, 
        notion_key = os.getenv("NOTION_TOKEN"), 
    ):
        self.notion_key = notion_key
        self.trash = ('archived', 'created_by', 'created_time', 'id', 'last_edited_by', 'last_edited_time', "parent", "object", "annotations", "has_children")

        self.headers = {
            'Authorization': f'Bearer {self.notion_key}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28',
        }
        self.co = 0

    def traverse_dict(self, data):
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                if key not in self.trash:
                    result[key] = self.traverse_dict(value)
            return result
        elif isinstance(data, list):
            result = []
            for item in data:
                result.append(self.traverse_dict(item))
            return result
        else:
            return data

    def block(
        self,
        block_id: str,
    ):
        url = f'https://api.notion.com/v1/blocks/{block_id}'
        headers = {
            'Authorization': f'Bearer {self.notion_key}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28',
        }
        result = requests.get(url, headers=headers).json()
        return result

    def block_children(
        self,
        block_id: str,
    ):
        url = f'https://api.notion.com/v1/blocks/{block_id}/children?page_size=100'
        headers = {
            'Authorization': f'Bearer {self.notion_key}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28',
        }
        result = requests.get(url, headers=headers).json()['results']
        return result


    def best_result(
        self,
        page_id: str,
    ):
        url = f'https://api.notion.com/v1/blocks/{page_id}/children?page_size=100'
        response = requests.get(url, headers=self.headers).json()
        result = []
        #co = 0      # для таблицы с примером
        for dct in response['results']:
            if dct["type"] == "table":
                block_id = dct['id']
                local = f'https://api.notion.com/v1/blocks/{block_id}/children'
                children = requests.get(local, headers=self.headers).json()['results']
                for_add = []
                for child in children:
                    #print(len(child["table_row"]['cells']), len(child))
                    if self.co == 0:
                        print('first table')
                        for_add.append({"type": "table_row", "table_row": child["table_row"]})
                        continue
                    # 3 колонки на 2 строки
                    elif  len(children) == 2 and child == children[-1]:
                        for cell in child["table_row"]['cells']:
                            if cell:
                                cell[0]['text']['content'] = ""
                                cell[0]['plain_text'] = ""

                    elif len(child["table_row"]['cells']) > 2 and len(child) > 2 and child != children[0]:
                        for cell in child["table_row"]['cells'][2:]:
                            for c in cell:
                                c['text']['content'] = ""
                                c['text']['link'] = None
                                c['plain_text'] = ""
                                c['href'] = None

                    elif len(child["table_row"]['cells']) == 2 and len(child) > 6:
                        for c in child["table_row"]['cells'][1]:
                            c['text']['content'] = ""
                            c['text']['link'] = None
                            c['plain_text'] = ""
                            c['href'] = None

                    for_add.append({"type": "table_row", "table_row": child["table_row"]})

                dct["table"]["children"] = for_add
                self.co += 1
            
            #elif len(child["table_row"]['cells']) == 11 and len(child) == 11 and co:
            elif self.co == 1:
                print('yes!')
                print(self.co)
                tmp = {"type": "table", "table": 
                {"table_width": 11, "has_column_header": False, "has_row_header": False, "children":
                [{"type": "table_row", "table_row": {"cells": [
                    [{"type": "text", "text": {"content": "5"}, "plain_text": "5"}], 
                    [{"type": "text", "text": {"content": "4"}, "plain_text": "4"}], 
                    [{"type": "text", "text": {"content": "3"}, 
                    "annotations": {"color": "green", "bold": True}, "plain_text": "3"}],
                    [{"type": "text", "text": {"content": "2"}, "plain_text": "2"}], 
                    [{"type": "text", "text": {"content": "1"}, 
                    "annotations": {"color": "blue"}, "plain_text": "1"}], 
                    [{"type": "text", "text": {"content": "0"}, 
                    "annotations": {"color": "purple", "bold": True}, "plain_text": "0"}],
                    [{"type": "text", "text": {"content": "1"}, 
                    "annotations": {"color": "blue", "bold": True}, "plain_text": "1"}],
                    [{"type": "text", "text": {"content": "2"}, 
                    "annotations": {"color": "blue", "bold": True}, "plain_text": "2"}],
                    [{"type": "text", "text": {"content": "3"}, "plain_text": "3"}], 
                    [{"type": "text", "text": {"content": "4"}, "plain_text": "4"}], 
                    [{"type": "text", "text": {"content": "5"}, "plain_text": "5"}]
                    ]}}]}}
                self.co += 1
                result.append(tmp)
                print(len(result))
                continue


            elif 'heading_1' in dct and dct['heading_1']["is_toggleable"]:
                block_id = dct['id']
                block_name = self.block(block_id)['heading_1']['rich_text']
                children = self.best_result(block_id)
                """
                tmp = {
                    "type": "toggle",
                    "toggle": {
                        'rich_text': block_name,
                    },
                    "children": children
                }
                """
                tmp = {
                    "heading_1": {
                        'rich_text': block_name,
                        "children": children
                    },
                }
                dct = tmp


            elif dct['type'] == 'image':
                img_block = {
                    "type": "image",
                    "image": {
                        "type": "external", 
                        "external": {
                            "url": "https://a.d-cd.net/bYAAAgBYPOA-1920.jpg"
                        }
                    }
                }
                dct = img_block
            result.append(dct)
        final = self.traverse_dict(result)
        return final
    
def main():
    pars = Parser()
    #pprint(pars.block(
    #    block_id='872d4b80-bb02-4a8a-b740-86e0eb2ad8e5',
    #))
    res = pars.best_result(page_id='6ba09cccf46d4e8c8a5aa044f3fd3481')
    with open('notionapi/data/new_version.json', 'w') as f:
        json.dump(res, f)


if __name__ == '__main__':
    main()
