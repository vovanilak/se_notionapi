import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import json
from utils.dictionry import insert_value
from person.source import Row
from config.proporties import *
from config.secret import *
from person.test import Test
from pprint import pprint


def staff(links):
        self.img_links = self.test_result_img()
        with open(self.json_file, 'r') as file:
            main = json.load(file)[:-6]
        try:
            prop = self.info_prop(
                self.name,
                'Name'
            )
        except Exception:
            prop = self.title_prop(title_name='Name', title_value=self.name)

def title_prop(title_value, title_name):
    for_all = {
        title_name: {
            'title': [
                {
                    "text":{
                        "content": title_value
                    } 
                    
                }
            ],
        },
        

    }
    
    return for_all
 

def info_prop(
    title_value, # значение заголовка (Петя, Вася)
    title_name, # название титульника
    row_info=None, 
    result_points=None,
    relation_card=None, # для персональных карточек
    levels=None, 
    grade_acse=None,
):
    columns = list(real_prop.keys()) 
    dct = {}
    inf = row_info
    for k in columns:
        if k in inf.keys() and real_prop[k] in dd[title_name].keys():
            if k == 'phone':
                inf[k] = '+' + str(inf[k]).split('.')[0]
            elif k == 'Возраст':
                inf[k] = int(inf[k])
            elif k in ('Как вы считаете, какому грейду вы сейчас соответствуете?', 
            'Как вы считаете, какому грейду сейчас соответствуете?'):
                if inf[k].startswith('Я'):
                    inf[k] = 'Я не аналитик и хочу им стать'
                else:
                    inf[k] = inf[k].split()[0]
            elif k == 'Предпочтительный формат работы':
                lst = []
                for f in inf[k].split('\n'):
                    lst.append(
                        {
                            'name': job_format[f]
                        }
                    )

                dct.update({
                    real_prop[k]: {
                        'multi_select': lst
                    }
                })
                continue

            dct.update({
                real_prop[k]: insert_value(dd[title_name][real_prop[k]], inf[k])
            })
    if title_name == 'ID Legioner':
        dct.update(
            {
                'Центр оценки компетенций': {
                    'select': {
                        'name': 'AC/SE'
                    }
                }
            }
        )
    if title_name in ('ID Legioner', 'Name'):
        dct.update(
            {
                'Дивизион': {
                    'select': {
                        'name': 'Системный анализ'
                    }
                },
                'Профиль специалиста': {
                    'select': {
                        'name': 'Системный аналитик'
                    }
                            
                        },
                'Points': {
                    'number': result_points,
                },

                'AC/SE grade': {
                    'select': {
                        'name': grade_acse,
                    }
                },
            }
        )

        for i, c in enumerate(skill_column):
            dct.update(
                {
                    c: {
                        'number': levels[i][0]
                    }
                }
            )

    elif title_name == 'ID Person':
        dct.update(
            {
                'Фамилия и Имя': {
                    'rich_text': [
                        {
                            "text": {
                                "content": title_value
                            }
                        }
                    ]

                },
                "ID card": {
                    "relation": [{
                        'id':  relation_card
                    }],
                },

            }
        )

    dct.update(title_prop(title_name=title_name, title_value=title_value))
    return dct

if __name__ == '__main__':
    row = Row(URL_LIGA, 52)
    test = Test(row.answer)
    pr = info_prop(
        title_value='Петя',
        title_name='ID Legioner',
        row_info=row.data,
        result_points=test.result_sum[0],
        levels=test.levels,
        grade_acse=test.grade_acse,
    )
    pprint(pr)