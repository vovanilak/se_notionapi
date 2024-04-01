import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

WORKDIR = 'notionapi'
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_STAFF = os.getenv('DATABASE_STAFF')
DATABASE_LIGA = os.getenv('DATABASE_LIGA')
DATABASE_LIGA_PERSON = os.getenv('DATABASE_LIGA_PERSON')
URL_LIGA = os.getenv('URL_LIGA')
URL_STAFF = os.getenv('URL_STAFF')

if os.path.exists(WORKDIR) and os.path.isdir(WORKDIR):
    os.chdir(WORKDIR)

levels = {
    0: 'OutIT',
    15: 'Junior-intern',
    20: 'Junior',
    30: 'Middle',
    40: 'Senior',
}
level_f = {
    0: 'OutIT',
    72: 'Junior-intern',
    108: 'Junior',
    162: 'Middle',
    216: 'Senior',
}
url = 'https://docs.google.com/spreadsheets/d/10oAnGTq7BT8R8vFca8Yd1am5cGBigP_L7vRypvtucI8/export?format=csv'
url = 'data.csv'

class Anketa:

    levels = {
        0: 'OutIT',
        15: 'Junior-intern',
        20: 'Junior',
        30: 'Middle',
        40: 'Senior',
    }

    level_f = {
    0: 'OutIT',
    72: 'Junior-intern',
    108: 'Junior',
    162: 'Middle',
    216: 'Senior',
    }

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


    def get_id(self):
        source = self.iso2date(self.created_date)
        source = pd.Timestamp(datetime.strptime(str(self.created_date)[:10], "%Y-%m-%d"))
        d = source.day
        m = source.month
        y = source.year
        date_list = self.other_dates[self.other_dates.dt.month == m].reset_index()
        date_list = date_list['dt_created']
        inx = date_list[date_list == source].index[0]
        id = str(d).rjust(2, '0') + str(m).rjust(2, '0')  + str(y)[2:] + str(inx + 1) + 'SE'
        return id

    def iso2date(self, iso_format):
        from datetime import datetime
        iso_datetime = pd.Timestamp(datetime.strptime(iso_format + '+00:00', "%Y-%m-%dT%H:%M:%S.%fZ%z"))
        return iso_datetime

    def get_dates(self):
        from datetime import datetime
        import pandas as pd
        #anket_dates = self.main_data['dt_created'].apply(lambda a: datetime.strptime(a, "%Y-%m-%dT%H:%M:%S.%fZ") if isinstance(a, str) and a[0].isdigit() else None)
        anket_dates = self.main_data['dt_created'].apply(lambda a: pd.Timestamp(datetime.strptime(str(a)[:10], "%Y-%m-%d")) if isinstance(a, str) and a[0].isdigit() else pd.NaT)

        #anket_dates = pd.to_datetime(self.main_data['dt_created'], format="%Y-%m-%d", errors='coerce')
  
        return anket_dates

    def get_proporties(self):
        dct = {"properties": {
            "title": [
                {
                    "text": {
                        "content": self.id
                    }
                }
            ],
            #"My grade": {'name': self.my_grade},
            #"Опыт работы в ИТ": {"number": self.it_work_experience},
            #"Город": {'name': self.city}
            }
        }
        return dct

    def get_personal_proporties(self):
        dct = {
            "properties": {   
                "Name": {
                    'title': [
                        {
                            "text": {
                                "content": self.id
                            }
                        }
                    ]
                },

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
                        'id': self.post_to_notion(),
                    }],
                },

            }
        }
        return dct

    def query_notion(self, notion_token, database_id, search, column):
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
                    'equals': search
                }
            }
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("Страница успешно создана в Notion!")
        else:
            print(f"Ошибка при создании страницы. Код ответа: {response.status_code}, Текст ответа: {response.text}")
        self.url = ''.join(response.json()['results'][0]['id'].split('-'))
        return self.url

    def get_page(self):
        import json

        img_links = self.test_result_img()
        
        with open(self.json_file, 'r') as file:
            main = json.load(file)
        counter = 1
        for i in range(len(main)):
            if "table" in main[i]:
                if len(main[i]['table']["children"]) > 2 and len(main[i]['table']["children"][0]['table_row']['cells']) == 3:
                    children = main[i]['table']["children"]
                    for j in range(10):
                        children[j + 1]["table_row"]['cells'][2][0]['text']['content'] = str(self.test_result[counter]['meta'][j])
                        if self.test_result[counter]['meta'][j] < 3:
                            children[j + 1]["table_row"]['cells'][2][0]['annotations'] = {'color': 'red', 'bold': True}
                    children[j + 2]["table_row"]['cells'][2][0]['text']['content'] = str(self.test_result[counter]['level'][0])
                    
                elif len(main[i]['table']["children"]) == 2 and counter < 7:
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

                elif len(main[i]['table']["children"]) == 8:
                    children = main[i]['table']["children"]
                    for j in range(1, 7):
                        children[j]["table_row"]['cells'][2][0]['text']['content'] = str(self.test_result[j]['level'][0])
                    children[-1]["table_row"]['cells'][2][0]['text']['content'] = str(self.test_result_sum[0])
            elif "image" in main[i] and counter < 8:
                main[i]['image']['external']['url'] = img_links[counter - 1]
                counter += 1
        return main

    def post_to_notion(self, notion_token, database_id, title, column):
        import requests
        url = f'https://api.notion.com/v1/pages'
        headers = {
            'Authorization': f'Bearer {notion_token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28',
        }
        dct = {
            "parent": {"database_id": database_id}, "icon": {"type": "emoji", "emoji": "😎"},
            "properties": {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ],
            #"My grade": {'name': self.my_grade},
            #"Опыт работы в ИТ": {"number": self.it_work_experience},
            #"Город": {'name': self.city}
            }
        }
        main = self.get_page()
        result = {**dct, "children": main}
        response = requests.post(url, headers=headers, json=result)
        self.query_notion(notion_token, database_id, search=title, column=column)

        if response.status_code == 200:
            print("Страница успешно создана в Notion!")
        else:
            print(f"Ошибка при создании страницы. Код ответа: {response.status_code}, Текст ответа: {response.text}")

    def post_person_to_notion(self, notion_token, database_result, database_person):
        url = f'https://api.notion.com/v1/pages'
        headers = {
            'Authorization': f'Bearer {notion_token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28',
        }
        dct = {
            "parent": {
                "database_id": database_person
                },
            'icon': {
                "type": "emoji", 
                "emoji": "🤓"
                },
            "properties": {   
                "Name": {
                    'title': [
                        {
                            "text": {
                                "content": self.id
                            }
                        }
                    ]
                },

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
                        'id': self.query_notion(notion_token, database_result, search=self.id, column='ID Legioner')
                    }],
                },

            }
        }
        response = requests.post(url, headers=headers, json=dct)

        if response.status_code == 200:
            print("Страница успешно создана в Notion!")
        else:
            print(f"Ошибка при создании страницы. Код ответа: {response.status_code}, Текст ответа: {response.text}")

    def post_liga(self, notion_token, database_result, database_person):
        self.post_to_notion(notion_token, database_result, title=self.id, column='ID Legioner')
        self.post_person_to_notion(notion_token, database_result, database_person)


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
        su = [self.test_result[i]['level'][0] for i in range(1, 7)]
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
        result = [int(response.split('.')[0]) - 1 for response in responses]

        return result

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
        url = self.post_uguu(f"{new_file}.png")
        os.remove(f"{new_file}.png")
        return url
        
    def test_result_img(self):
        result = []
        for i in range(1, len(self.test_result) + 1):
            data1 = self.test_result[i]['meta']
            lower_bound_value = self.test_result[i]['level'][1] // 10
            upper_bound_value = self.test_result[i]['level'][2] // 10
            lower_ttl = self.test_result[i]['level'][3]
            upper_ttl = self.test_result[i]['level'][4]
            result.append(self.plot_radar_chart(data1, lower_bound_value, upper_bound_value, lower_ttl, upper_ttl))
        result.append(self.plot_bar_chart_with_annotations())
        print('Графики на сервере!')
        return result

    def post_uguu(self, img_path):
        import requests
        url = ' https://uguu.se/upload'
        response = requests.post(url, files={"files[]": open(img_path, 'rb')})
        res = response.json()
        return res['files'][0]['url']

    def plot_bar_chart_with_annotations(self):
        import plotly.graph_objects as go
        import plotly.io as pio
        import time

        special_number = 0
        for v in self.test_result.values():
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
        url = self.post_uguu(f"{new_file}.png")
        os.remove(f"{new_file}.png")
        return url

def main():
    '''
    want = int(input('Что ты хочешь?\n\n0 - Pro LIGA IT\n1 - AC/SE штатных сотрудников\n>>> '))
    number = int(input('Какой номер строки?\n>>> '))
    if want:
        person = Anketa(url=URL_STAFF,
                        row=number,
                        json_file='data/staff.json',
                        start_result_column=11)
        print(person.id)
        person.post_to_notion(NOTION_TOKEN, DATABASE_STAFF, title=person.name, column='Name')
        
    else:
        person = Anketa(url=URL_LIGA,
                        row=number,
                        json_file='data/short2_back.json',
                        start_result_column=13)
        print(person.id)
        
        person.post_liga(
            NOTION_TOKEN, 
            database_result=DATABASE_LIGA, 
            database_person=DATABASE_LIGA_PERSON
            )
    '''
    person = Anketa(url=URL_STAFF,
                row=30,
                json_file='data/staff.json',
                start_result_column=11)
    print(person.id)

if __name__ == '__main__':
    main()


