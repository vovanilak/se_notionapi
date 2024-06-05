import requests
from dotenv import load_dotenv
import os
from pprint import pprint, pformat
import json
import os

load_dotenv()

NOTION_TOKEN=os.getenv('NOTION_TOKEN')
TRASH = ('archived', 'created_by', 'created_time', 'id', 'last_edited_by', 'last_edited_time', "parent", "object", "annotations", "has_children")
#TRASH = []
WORKDIR = 'notionapi/notion'

if os.path.exists(WORKDIR) and os.path.isdir(WORKDIR):
    os.chdir(WORKDIR)

pageid = '22be90b314b246b792acf0ae0b2b84b4'
pageid = '6ba09cccf46d4e8c8a5aa044f3fd3481'
pageid = '5e4093d0244f42f789ac10eb8622923c' # тест таблица
url = f'https://api.notion.com/v1/blocks/{pageid}/children?page_size=105'

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
}

response = requests.get(url, headers=headers)

def bytes_to_dict(bytes_obj):
    str_data = bytes_obj.decode('utf-8')
    dict_data = json.loads(str_data)
    return dict_data

def traverse_dict(data):
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if key not in TRASH:
                result[key] = traverse_dict(value)
        return result
    elif isinstance(data, list):
        result = []
        for item in data:
            result.append(traverse_dict(item))
        return result
    else:
        return data

def traverse_dict_v2(data):
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if key not in TRASH:
                result[key] = traverse_dict(value)
        return result
    else:
        return data

def pprint2file(data, path='template_example.json'):
    pprinted_data = pformat(data)
    with open(path, 'w') as file:
        json.dump(data, file)

def best_result():
    response = requests.get(url, headers=headers).json()
    result = []
    co = 0      # для таблицы с примером
    for dct in response['results']:
        print(dct['id'])
        if dct["type"] == "table":
            block_id = dct['id']
            local = f'https://api.notion.com/v1/blocks/{block_id}/children'
            children = requests.get(local, headers=headers).json()['results']
            for_add = []
            for child in children:
                print(len(child["table_row"]['cells']), len(child))
                if  len(children) == 2 and child == children[-1]:
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

                elif len(child["table_row"]['cells']) == 11 and len(child) == 11 and not co:
                #elif co == 1:
                    print('yes!')
                    co += 1
                    child["table_row"]['cells']  = [
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
                        ]

                for_add.append({"type": "table_row", "table_row": child["table_row"]})
            dct["table"]["children"] = for_add
            result.append(dct)
        
        elif "is_toggleable" in dct.keys() and dct["is_toggleable"]:
            block_id = dct['id']
            local = f'https://api.notion.com/v1/blocks/{block_id}/children'
            children = requests.get(local, headers=headers).json()['results']
            tmp = {
                "type": "toggle",
                "toggle": {
                    "rich_text": [{
                    "type": "text",
                    "text": {
                        "content":  dct["heading_1"]["rich_text"][0]["text"]["content"],
                        "link": null
                    }
                    }],
                    "children": children
                }
            }
            result.append(tmp)

        
        elif 'column_list' in dct.keys():
            pass

        elif isinstance(dct, list):
            tmp = {
                "toggle": {
                    "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": "Additional project details",
                    }
                    }],
                    "children":dct
                }
            }
            result.append(tmp)

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
            result.append(img_block)
            '''img_block = {
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": dct["image"]["file"]["url"]
                    }
                }
                }
            result.append(img_block)
            result.append(
                {
                    "type": "text",
                    "text": {
                        "content": "Image here"
                    },
                        "plain_text": "Image here"
                }
            )'''
        else: 
            result.append(dct)
    final = traverse_dict(result)
    #print(final)
    with open('../data/test.json', 'w') as file:
        json.dump(final, file)

def full_notion():
    response = requests.get(url, headers=headers).json()
    result = []
    for dct in response['results']:
        result.append(dct)
    final = traverse_dict(result)
    with open('../data/new_version.json', 'w') as file:
        json.dump(final, file)

def main():
    best_result()
    #full_notion()
    #result = traverse_dict(bytes_to_dict(response.content))
    #pprint2file(traverse_dict_v2(response.json()), 'page_v2.json')
    #with open('template_example.json', 'w') as file:
    #    json.dump(file)

if __name__ == '__main__':
    main()




