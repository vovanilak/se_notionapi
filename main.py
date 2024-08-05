import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime
from dotenv import load_dotenv
from pprint import pprint
from server.google import GoogleApi
import os

load_dotenv()

WORKDIR = 'notionapi'

if os.path.exists(WORKDIR) and os.path.isdir(WORKDIR):
    os.chdir(WORKDIR)

url = 'https://docs.google.com/spreadsheets/d/10oAnGTq7BT8R8vFca8Yd1am5cGBigP_L7vRypvtucI8/export?format=csv'
url = 'data.csv'

class Anketa:
    NOTION_TOKEN = os.getenv('NOTION_TOKEN')
    DATABASE_STAFF = os.getenv('DATABASE_STAFF')
    DATABASE_LIGA = os.getenv('DATABASE_LIGA')
    DATABASE_LIGA_PERSON = os.getenv('DATABASE_LIGA_PERSON')
    URL_LIGA = os.getenv('URL_LIGA')
    URL_STAFF = os.getenv('URL_STAFF')

    levels = {
        0: 'Outside',
        12: 'Junior-intern',
        18: 'Junior',
        24: 'Pre-Middle',
        27: 'Middle',
        32: 'Pre-Senior',
        36: 'Senior',
        41: 'Lead',
    }

    level_f = {
        0: 'Outside',
        60: 'Junior-intern',
        90: 'Junior',
        121: 'Pre-Middle',
        135: 'Middle',
        162: 'Pre-Senior',
        180: 'Senior',
    }

    level_text = {
        "Outside": "Outside: Не обладает необходимыми для Junior-intern навыками, не имеющий достаточно опыта работы с программными средствами (0-59 поинтов)",
        "Junior-intern" : "Junior-intern: Специалист с начальными техническими навыками, способный выполнять задачи проекта/команды только под контролем наставника (60-89 поинтов)",
        "Junior": "Junior: Специалист с формирующимися навыками ответственности, требует привлечения наставника при необходимости (90-120 поинтов)", 
        "Pre-Middle": "Pre-Middle: Специалист с приемлемым уровнем самостоятельности, при котором формируются навыки ответственности и эффективности (121-134 поинтов)", 
        "Middle": "Middle: Специалист, с хорошо развитыми техническими навыками, тактическим мышлением, планированием и контролем поставленных задач. Полностью самостоятельный, достигает результата за счет личной эффективности (135-161 поинтов)", 
        "Pre-Senior" : "Pre-Senior: Специалист выступает техническим консультантом команды, мыслит и принимает стратегические решения на уровне проекта / отдела (162-179 поинтов)", 
        "Senior": "Senior: Специалист является техническим лидером команды с глубокими знаниями, опытом и экспертизой. Решает задачи на уровне проекта / отдела (180-200 поинтов)", 
        "Lead" : "Lead: Специалист является компетентным лидером команды, обеспечивает условия реализации стратегии компании. Основная функция - организация работы команды и контроль выполнения задач (180-200 поинтов)"
    }
    
    question_level = {
        'Не понимаю': 0,
        'Не знаю': 0,
        "Не владею": 0,
        "Знаю только": 1,
        "Знаю теорию": 2,
        "Испытываю сложности": 2,
        "Использую на": 3,
        "Владею и": 3,
        "Владею в": 4,
    }
        
    skill_column = [
        'К1. ВЗАИМОДЕЙСТВИЕ С ЛЮДЬМИ',
        'К2. МОДЕЛИРОВАНИЕ БИЗНЕСА И ДОМЕНА',
        'К3. ИНЖЕНЕРИЯ ТРЕБОВАНИЙ',
        'К4. СИСТЕМНОЕ ПРОЕКТИРОВАНИЕ',
        'К5. ИНТЕГРАЦИЯ ИС',
        'К6. ЛИЧНОСТНЫЕ КАЧЕСТВА'
    ]

    def __init__(self, url, row, json_file, start_result_column):
        import pandas as pd
        self.main_data = pd.read_csv(url)
        self.data = self.main_data.iloc[row - 2, :]
        self.start_column = start_result_column
        self.json_file = json_file
        self.other_dates = self.get_dates()
        self.created_date = self.data['dt_created']
        self.id = self.get_id()
        self.name = self.data['name']
        self.test_result = self.get_result()
        self.test_result_sum = self.get_result_sum()
        self.url = None
        self.api = GoogleApi(
            service_path='data/google/se_google_key.json',
            root_folder_id='1wbmhJP3JEsL2_n2bgXaD4yl7PAbx6k_R'
            #root_folder_id='1mnyu7zvD1yNgAtZDWmKeeSMdmXRYuOYu'
            #root_folder_id='19i_mtgS6DTCMhtzPpt3wKdnN0vH_U8iW'
        )
        #self.img_links = self.test_result_img()
        self.img_links = None


    def get_id(self):
        source = pd.Timestamp(datetime.strptime(str(self.created_date)[:10], "%Y-%m-%d"))
        d = source.day
        m = source.month
        y = source.year
        date_list = self.other_dates[self.other_dates.dt.month == m].reset_index()
        date_list = date_list['dt_created']
        inx = date_list[date_list == source].index[0]
        id = str(d).rjust(2, '0') + str(m).rjust(2, '0')  + str(y)[2:] + str(inx + 1) + 'SE'
        return id


    def get_dates(self):
        from datetime import datetime
        import pandas as pd
        #anket_dates = self.main_data['dt_created'].apply(lambda a: datetime.strptime(a, "%Y-%m-%dT%H:%M:%S.%fZ") if isinstance(a, str) and a[0].isdigit() else None)
        anket_dates = self.main_data['dt_created'].apply(lambda a: pd.Timestamp(datetime.strptime(str(a)[:10], "%Y-%m-%d")) if isinstance(a, str) and a[0].isdigit() else pd.NaT)

        #anket_dates = pd.to_datetime(self.main_data['dt_created'], format="%Y-%m-%d", errors='coerce')
  
        return anket_dates

    def get_page(self, main):
        counter = 1
        flag = 0
        for i in range(len(main)):
            if "table" in main[i]:
                if len(main[i]['table']["children"]) > 2 and len(main[i]['table']["children"][0]['table_row']['cells']) == 3:
                    children = main[i]['table']["children"]
                    for j in range(10):
                        children[j + 1]["table_row"]['cells'][2][0]['text']['content'] = str(self.test_result[counter]['meta'][j])
                        if self.test_result[counter]['meta'][j] < 3:
                            children[j + 1]["table_row"]['cells'][2][0]['annotations'] = {'color': 'red', 'bold': True}
                    children[j + 2]["table_row"]['cells'][2][0]['text']['content'] = str(self.test_result[counter]['level'][0])
                    
                elif len(main[i]['table']["children"]) == 2 and counter < 6 and flag:
                    children = main[i]['table']["children"]
                    children[0]['table_row']['cells'][0][0]['text']['content'] = str(self.test_result[counter]['level'][3])
                    children[0]['table_row']['cells'][2][0]['text']['content'] = str(self.test_result[counter]['level'][4])
                    children[1]['table_row']['cells'][0][0]['text']['content'] = str(self.test_result[counter]['level'][1])
                    children[1]['table_row']['cells'][1][0]['text']['content'] = str(self.test_result[counter]['level'][0])
                    children[1]['table_row']['cells'][2][0]['text']['content'] = str(self.test_result[counter]['level'][2])
                    

                elif len(main[i]['table']["children"]) == 2:
                    children = main[i]['table']["children"]
                    children[0]['table_row']['cells'][0][0]['text']['content'] = str(self.test_result_sum[3])
                    children[0]['table_row']['cells'][2][0]['text']['content'] = str(self.test_result_sum[4])
                    children[1]['table_row']['cells'][0][0]['text']['content'] = str(self.test_result_sum[1])
                    children[1]['table_row']['cells'][1][0]['text']['content'] = str(self.test_result_sum[0])
                    children[1]['table_row']['cells'][2][0]['text']['content'] = str(self.test_result_sum[2])


                elif len(main[i]['table']["children"]) == 8 and not flag:
                    children = main[i]['table']["children"]
                    for j in range(1, 6):
                        children[j]["table_row"]['cells'][2][0]['text']['content'] = str(self.test_result[j]['level'][0])
                    children[-1]["table_row"]['cells'][2][0]['text']['content'] = str(self.test_result_sum[0])
            
            elif "image" in main[i] and counter < 6:
                #main[i]['image']['external']['url'] = self.img_links[counter - 1]
                del main[i]['image']
                main[i]['type'] = 'embed'
                main[i]['object'] = 'block'
                main[i]['embed'] = {'url': self.img_links[counter]}
                #if counter == 1:
                #    del self.img_links[counter - 1]
                counter += 1

            elif "quote" in main[i]:
                flag = 1

            elif 'heading_1' in main[i] and 'children' in main[i]['heading_1']:
                main[i]['heading_1']['children'] = self.get_page(main[i]['heading_1']['children'])

            elif i == 0 and 'heading_2' in main[i]:
                text = f'По результатам ассесмента перед вами специалист с предварительно подтвержденным грейдом уровня {self.grade_acse(self.test_result_sum[0])} ({self.test_result_sum[0]} пойнтов).'
                main[i]['heading_2']['rich_text'][0]['plain_text'] = text
                main[i]['heading_2']['rich_text'][0]['text']['content'] = text

            elif i == 3 and 'paragraph' in main[i] and counter == 1:
                text = self.level_text[self.grade_acse(self.test_result_sum[0])]
                main[i]['paragraph']['rich_text'] = [{"type": "text", "text": {"content": text}, "plain_text": text}]
                
            elif 'callout' in main[i-1]:
                text = self.level_text[self.grade_acse(self.test_result_sum[0])]
                main[i]['paragraph']['rich_text'] = [{"type": "text", "text": {"content": text}, "plain_text": text}]
            

            elif "callout" in main[i]:
                counter -= 1
        #if self.start_column == 11 and 'heading_2' in main[0]:
        #    del main[-1]
        return main

    
    def insert_value(self, dictionary, value):
        if not isinstance(dictionary, dict):
            return

        keys = list(dictionary.keys())
        last_key = keys[-1]
        
        if isinstance(dictionary[last_key], dict):
            dictionary[last_key] = self.insert_value(dictionary[last_key], value)
        elif isinstance(dictionary[last_key], list):
            for i, item in enumerate(dictionary[last_key]):
                if isinstance(item, dict):
                    dictionary[last_key][i] = self.insert_value(item, value)
        else:
            dictionary[last_key] = value
        
        return dictionary

    def title_prop(self, title_value, title_name):
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


    @classmethod
    def grade_acse(cls, grade):
        grds = list(cls.level_f.keys())
        for r in grds:
            if grade in range(r):
                return cls.level_f[grds[grds.index(r) - 1]]
        return 'Senior'
        
 

    def info_prop(
        self, 
        title_value,
        title_name,
    ):
        real_prop = {
            'phone': 'Phone', # staff
            'email': 'Email', # staff
            'Какой ваш опыт работы в IT?': 'Опыт работы в ИТ', # liga
            'В каком городе вы проживаете?': 'Город', # liga, staff
            'Предпочтительный формат работы': 'Формат работы', # liga
            'Как вы считаете, какому грейду вы сейчас соответствуете?': 'My grade', # liga,
            'Как вы считаете, какому грейду сейчас соответствуете?': 'My grade', # staff,
            'Возраст': 'Возраст', # liga, staff
            'name': 'Фамилия и Имя', 
            'iwork': 'Компания',
            'city': 'Город',
        }

        job_format = {
            'Удалёнка': 'Удалёнка',
            'В офисе': 'Офис',
            'Готов к переезду в другой город / страну': 'Готов к релокации',
            'Комбинированный формат': 'Комбинированный',
            "Только фултайм": "Только фултайм",
            "Частичная занятость": "Партайм",
        }
        
        dd = {'Name': {
                'Город': {
                    'select': {
                        'name': 'lol'
                    }
                },
                'Возраст': {
                    'number': 0
                },
                'Phone': {
                    "phone_number": '+7'
                }, 
                'Email': {
                    "email": 'em'
                },
                'My grade': {
                    'select': {
                        'name': 'test'
                    }
                },
                'Опыт работы в ИТ': {
                    'rich_text': [
                        {
                            "text": {
                                "content": 'test'
                            }
                        }
                    ]
                },
                'Компания': {
                    'rich_text': [
                        {
                            "text": {
                                "content": 'test'
                            }
                        }
                    ]
                }
        },
        'ID Legioner': {
            'Формат работы': {
                'multi_select': [
                        {
                            'name': 'test'
                        }
                    ]
            },
            'Город': {
                'select': {
                    'name': 'lol'
                }
            },
            'Возраст': {
                'number': 0
            },
            'Опыт работы в ИТ': {
                'rich_text': [
                    {
                        "text": {
                            "content": 'test'
                        }
                    }
                ]
            },
            'My grade':{
                'select': {
                    'name': 'test'
                }
            },

        },
        'ID Person': {
            'Phone': {
                "phone_number": '+7'
            }, 
            'Email': {
                "email": 'em'
            },
            'Возраст': {
                'number': 0
            },
        }
        }
        

        columns = list(real_prop.keys()) 
        dct = {}
        inf = self.data.dropna()
        for k in columns:
            if k in inf.index and real_prop[k] in dd[title_name].keys():
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
                    real_prop[k]: self.insert_value(dd[title_name][real_prop[k]], inf[k])
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
                        'number': self.test_result_sum[0]
                    },

                    'AC/SE grade': {
                        'select': {
                            'name': self.grade_acse(self.test_result_sum[0]),
                        }
                    },
                }
            )

            for i, c in enumerate(self.skill_column):
                dct.update(
                    {
                        c: {
                            'number': self.test_result[i + 1]['level'][0]
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
                                    "content": self.name
                                }
                            }
                        ]

                    },
                    "ID card": {
                        "relation": [{
                            'id':  self.url_card(
                                val=title_value,
                            )
                        }],
                    },

                }
            )
        dct.update(self.title_prop(title_name=title_name, title_value=title_value))
        return dct

    #### NOTION

    @classmethod
    def query_notion(
        cls,
        val, # какое значение искать
        column, # в какой колонке искать
        notion_token=NOTION_TOKEN, 
        database_id=DATABASE_LIGA, 
    ):
        import requests
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
        response = requests.post(url, headers=headers, json=data)
        # url = ''.join(response.json()['results'][0]['id'].split('-'))
        return response.json()

    def url_card(self, val):
        response = self.query_notion(
            val=val,
            column='ID Legioner',
        )
        url = ''.join(response['results'][0]['id'].split('-'))
        return url

    @classmethod
    def post_to_notion(
        cls,
        database_id, 
        prop: dict,
        page_content: list,
        emoji: str, # "😎", "🤓"
        notion_token=NOTION_TOKEN, 
    ):
        import requests
        url = f'https://api.notion.com/v1/pages'
        headers = {
            'Authorization': f'Bearer {notion_token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28',
        }

        dct = {
            "parent": {"database_id": database_id}, 
            "icon": {"type": "emoji", "emoji": emoji},
            "properties": prop,
            "children": page_content
        }
        response = requests.post(url, headers=headers, json=dct)
        return response.json()

    def post_staff(
        self,
        notion_token=NOTION_TOKEN, 
        database_result=DATABASE_LIGA, 
        database_person=DATABASE_LIGA_PERSON,
    ):
        import json
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

        a = self.post_to_notion(
            database_id=self.DATABASE_STAFF,
            prop=prop,
            page_content=self.get_page(main),
            emoji="😎",
        )
        return a


    def post_liga(
        self,
        notion_token=NOTION_TOKEN,
        database_result=DATABASE_LIGA,
        database_person=DATABASE_LIGA_PERSON,
    ):
        import json
        self.img_links = self.test_result_img()
        with open(self.json_file, 'r') as file:
            main = json.load(file)
        try:
            prop = self.info_prop(
                self.id,
                'ID Legioner'
            )
            
        except Exception:
            prop = self.title_prop(title_name='ID Legioner', title_value=self.id)
        a = self.post_to_notion(
            database_id=database_result,
            prop=prop,
            page_content=self.get_page(main),
            emoji="🥷🏻"
        )

        prop = self.info_prop(title_name='ID Person', title_value=self.id)
        b = self.post_to_notion(
            database_id=database_person,
            prop=prop,
            page_content=[],
            emoji="🤓"
        )
        return a, b
        

    def get_result(self):
        dct = {}
        n = 1
        for i in range(self.start_column, self.start_column + 60, 10):
            dct[n] = {'meta': None, 'level': None}
            dct[n]['meta'] = self.get_responses(i, i + 10)
            dct[n]['level'] = self.find_level(dct[n]['meta'], self.levels)
            n += 1
        return dct

    def get_result_sum(self):
        su = [self.test_result[i]['level'][0] for i in range(1, 6)]
        res = self.find_level(su, self.level_f)
        return res

    def find_level(self, meta, levels):
        sum_meta = sum(meta)
        sorted_keys = sorted(levels.keys())

        lower_bound = None
        upper_bound = None

        for i in range(len(sorted_keys)):
            if sum_meta == sorted_keys[i]:
                lower_bound = sorted_keys[i]
                upper_bound = sorted_keys[i + 1] if i + 1 < len(sorted_keys) else sorted_keys[i]
                break
            elif sum_meta < sorted_keys[i]:
                lower_bound = sorted_keys[i - 1] if i > 0 else sorted_keys[i]
                upper_bound = sorted_keys[i]
                break

        lower_bound_name = levels.get(lower_bound, "Неизвестно")
        upper_bound_name = levels.get(upper_bound, "Неизвестно")

        return [sum_meta, lower_bound, upper_bound, lower_bound_name, upper_bound_name]


    def get_responses(self, com1, com2):

        # Выборка данных из указанной строки
        responses = self.data.iloc[com1:com2].values
        result = [self.question_level[' '.join(response.split()[1:3])] for response in responses]

        return result

    #### IMAGE ####

    def plot_radar_chart(self, data1, lower_bound_value, upper_bound_value, lower_ttl, upper_ttl):
        import plotly.graph_objects as go
        import plotly.io as pio
        import time


        labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

        fig = go.Figure()

        # Добавляем основную линию
        fig.add_trace(go.Scatterpolar(
            r=data1 + data1[:1],
            theta=labels + labels[:1],
            fill='toself',
            name='Специалист'
        ))

        # Создаем массив для нижней и верхней границы
        constant_lower_bound = [lower_bound_value] * len(labels)
        constant_upper_bound = [upper_bound_value] * len(labels)

        # Добавляем линию нижней границы
        fig.add_trace(go.Scatterpolar(
            r=constant_lower_bound + constant_lower_bound[:1],
            theta=labels + labels[:1],
            name=lower_ttl,
            line=dict(dash='dash')
        ))

        # Добавляем линию верхней границы
        fig.add_trace(go.Scatterpolar(
            r=constant_upper_bound + constant_upper_bound[:1],
            theta=labels + labels[:1],
            name=upper_ttl,
            line=dict(dash='dash')
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    dtick=1,  # Устанавливаем шаг оси радиуса в 1
                    range=[0, 4]  # Устанавливаем диапазон оси радиуса от 0 до 4
                ),
            ),
            showlegend=True,
            legend=dict(
                x=0.5,
                y=-0.3,  # Устанавливаем отрицательное значение Y для размещения под графиком
                orientation='h',  # Горизонтальное размещение легенды
                xanchor='center'  # Центрируем легенду
            )
        )

        new_file = str(time.time())
        pio.write_image(fig, f"{new_file}.png", scale=2)
        return f'{new_file}.png'
        
    def test_result_img(self):
        folder_id = self.api.folder_here(self.name)
        if folder_id:
            self.api.del_file(folder_id)
        result = []

        img = self.plot_bar_chart_with_annotations()
        link = self.api.create_n_load(
            folder_name=self.name,
            img_path=img,
            img_name='result')
        os.remove(img)
        result.append(link)

        for i in range(1, len(self.test_result)):
            data1 = self.test_result[i]['meta']
            lower_bound_value = self.test_result[i]['level'][1] // 10
            upper_bound_value = self.test_result[i]['level'][2] // 10
            lower_ttl = self.test_result[i]['level'][3]
            upper_ttl = self.test_result[i]['level'][4]
            img = self.plot_radar_chart(data1, lower_bound_value, upper_bound_value, lower_ttl, upper_ttl)
            link = self.api.create_n_load(
                folder_name=self.name, 
                img_path=img, 
                img_name=str(i))
            os.remove(img)
            result.append(link)
        
        return result
        
    def uguu_links(self):
        result = []

        img = self.plot_bar_chart_with_annotations()
        link_uguu = self.post_uguu(img)
        result.append(link_uguu)
        os.remove(img)

        for i in range(1, len(self.test_result) + 1):
            data1 = self.test_result[i]['meta']
            lower_bound_value = self.test_result[i]['level'][1] // 10
            upper_bound_value = self.test_result[i]['level'][2] // 10
            lower_ttl = self.test_result[i]['level'][3]
            upper_ttl = self.test_result[i]['level'][4]
            img = self.plot_radar_chart(data1, lower_bound_value, upper_bound_value, lower_ttl, upper_ttl)
            link_uguu = self.post_uguu(img)
            result.append(link_uguu)
            os.remove(img)
        
        return result
    @classmethod
    def post_uguu(cls, img_path):
        import requests
        url = ' https://uguu.se/upload'
        response = requests.post(url, files={"files[]": open(img_path, 'rb')})
        res = response.json()
        return res['files'][0]['url']

    def post_google(
        self, 
        img_path,
            img_name,
            folder_name,
            ):
            link = self.api.create_n_load(folder_name, img_path, img_name)
            return link



    def plot_bar_chart_with_annotations(self):
        import plotly.graph_objects as go
        import plotly.io as pio
        import time

        special_number = 0
        for v in list(self.test_result.values())[:-1]:
            special_number += v['level'][0]
        # Сортировка словаря по ключам и получение отдельных списков значений и ключей
        sorted_data = sorted(self.level_f.items(), key=lambda item: item[0])
        values = [item[0] for item in sorted_data]
        labels = [item[1] for item in sorted_data]

        # Определение позиции для вставки особого числа
        insert_position = 0
        for i, value in enumerate(values):
            if special_number <= value:
                insert_position = i
                break
        else:
            insert_position = len(values)

        # Вставка особого числа и метки для него
        special_label = "Специалист"
        labels.insert(insert_position, special_label)
        values.insert(insert_position, special_number)

        # Определение цветов для столбцов
        colors = ['blue' if value != special_number else 'red' for value in values]

        fig = go.Figure(data=[go.Bar(
            x=labels,
            y=values,
            marker_color=colors,
            text=values,  # Добавляем значения как текст для каждого столбца
            textposition='auto'  # Позиционирование текста
        )])

        new_file = str(time.time())
        pio.write_image(fig, f"{new_file}.png", scale=2)
        return f'{new_file}.png' 


def full():
    want = int(input('Куда добавить карточку?\n0 - Pro LIGA IT\n1 - AC/SE штатных сотрудников\n>>> '))
    number = int(input('Какой номер строки?\n>>> '))
    if want:
        person = Anketa(url=Anketa.URL_STAFF,
                        row=number,
                        json_file='data/notion/new_version2.json',
                        start_result_column=11)
        k = person.post_staff()
        print(k)
        
    else:
        person = Anketa(url=Anketa.URL_LIGA,
                        row=number,
                        json_file='data/notion/new_version2.json',
                        start_result_column=13)
        res = person.post_liga()
        print(*res, sep='\n\n')

def part():
    person = Anketa(url=Anketa.URL_LIGA,
                    row=10,
                    json_file='data/notion/new_version.json',
                    start_result_column=13)
    print(person.test_result)

def test():
    import json
    person = Anketa(url=Anketa.URL_STAFF,
                    row=30,
                    json_file='data/notion/new_version.json',
                    start_result_column=11)
    with open('data/new_version.json', 'r') as file:
        main = json.load(file)
    k = person.get_page(main)
    print(k)
    with open('tmp.json', 'w') as js:
        json.dump(k, js)
if __name__ == '__main__':
    full()


