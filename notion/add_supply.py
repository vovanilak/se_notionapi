import json
from pprint import pprint
import os 

os.chdir('notionapi')

    
add = [ 
    {
        "heading_1": {
        "rich_text": [{
          "type": "text",
          "text": {
            "content": "ПРЕДЛОЖЕНИЕ ДЛЯ НАНИМАТЕЛЕЙ",
          }
        }]
        }
    },

    {
        "object": "block",
        "column_list": {
            'children': [
                {
                    "column": {
                            "children": [{
                                "object": "block",
                                "image": {
                                    "external": {
                                        "url": "https://file.notion.so/f/f/b6724791-6712-4c10-aad8-84f47558b581/bb7bbca0-d4b2-4ba9-af3b-611f51843c16/APRL.svg?id=b05d2982-fd24-4405-84f0-d8a195106bec&table=block&spaceId=b6724791-6712-4c10-aad8-84f47558b581&expirationTimestamp=1717660800000&signature=eN1h0aHC3BFI1O1aMz6PGqlOVye1QQw4g_u-tbWpFZk&downloadName=APRL.svg"
                                    }
                                }
                        }]
                    }
                },

                {
                    "column": {
                            "children": [{
                                "object": "block",
                                'paragraph': {'color': 'default',
                                'rich_text': [{'href': None,
                                           'plain_text': 'Провайдером данного специалиста '
                                                         'выступает ',
                                           'text': {'content': 'Провайдером данного '
                                                               'специалиста выступает ',
                                                    'link': None},
                                           'type': 'text'},
                                          {'href': 'https://t.me/PCAPRIL',
                                           'plain_text': 'Продюсерский центр АПРЕЛЬ',
                                           'text': {'content': 'Продюсерский центр АПРЕЛЬ',
                                                    'link': {'url': 'https://t.me/PCAPRIL'}},
                                           'type': 'text'}]},
                            },

                            {
                                'paragraph': {'color': 'default',
                                'rich_text': [{'href': None,
                                   'plain_text': 'Директор ',
                                   'text': {'content': 'Директор ', 'link': None},
                                   'type': 'text'},
                                  {'href': 'https://t.me/KodZima77',      
                                   'plain_text': 'Дмитрий Коротыш',       
                                   'text': {'content': 'Дмитрий Коротыш', 
                                            'link': {'url': 'https://t.me/KodZima77'}},
                                   'type': 'text'}]},
                              'type': 'paragraph'},
                            ]
                    }
                }
            ]
        }
    },
    
    {'in_trash': False,
      'paragraph': {'color': 'default',        
                    'rich_text': [{'href': None,
                                   'plain_text': 'Совместно с Центром оценки и '
                                               
      'развития компетенций ',
                                   'text': {'content': 'Совместно с Центром оценки '      
                                               
            'и развития компетенций ',
                                            'link': None},
                                   'type': 'text'},
                                  {'href': 'https://systems.education/acse',
                                   'plain_text': 'Systems Education',
                                   'text': {'content': 'Systems Education',
                                            'link': {'url': 'https://systems.education/acse'}},
                                   'type': 'text'},
                                  {'href': None,
                                   'plain_text': ', мы помогаем нанимателям найти '       
                                               
      'лучших специалистов.\n'
            'Нашим Легионерам помогаем найти '       
                                           
  'работу, соответствующую их '
                                           
  'требованиям и профессиональным '        
                                           
  'навыкам.',
                                   'text': {'content': ', мы помогаем нанимателям '       
                                               
            'найти лучших '
                                               
            'специалистов.\n'
            'Нашим Легионерам помогаем найти '       
                                           
  'работу, соответствующую их '
                                           
  'требованиям и профессиональным '        
                                           
  'навыкам.',

                                            'link': None},
                                   'type': 'text'}]},
  'type': 'paragraph'},

 {'in_trash': False,
  'numbered_list_item': {'color': 'default',
                         'rich_text': [{'href': None,
                                        'plain_text': 'Определяем и развиваем профессиональные компетенции.',
                                        'text': {'content': 'Определяем и развиваем профессиональные компетенции.',
                                                 'link': None},
                                        "annotations": {'bold': True},
                                        'type': 'text'}]},
  'type': 'numbered_list_item'},

 {'in_trash': False,
  'numbered_list_item': {'color': 'default',
                         'rich_text': [{'href': None,
                                        'plain_text': 'Подбираем карьерный '
                                                      'трек, и сопровождаем во '
                                                      'время испытательного '
                                                      'срока.',
                                        'text': {'content': 'Подбираем '
                                                            'карьерный трек, и '
                                                            'сопровождаем во '
                                                            'время '
                                                            'испытательного '
                                                            'срока.',
                                                 'link': None},
                                        "annotations": {'bold': True},
                                        'type': 'text'}]},
  'type': 'numbered_list_item'},
  
 {'in_trash': False,
  'numbered_list_item': {'color': 'default',
                         'rich_text': [{'href': None,
                                        'plain_text': '',
                                        'text': {'content': 'Повышаем '
                                                            'коммерческую '
                                                            'ценность '
                                                            'специалиста на '
                                                            'рынке труда.',
                                                 'link': None},
                                        "annotations": {'bold': True},
                                        'type': 'text'}]},
  'type': 'numbered_list_item'},

]
print(len(add))
with open('data/test.json', 'r') as file:
    result = json.load(file)

result.extend(add)

with open('data/test2.json', 'w') as file:
    json.dump(result, file)