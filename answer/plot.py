import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import plotly.graph_objects as go
import plotly.io as pio
import time
from config.test import level_f
from server.google import GoogleApi
from answer.test import Test
from user.source import Row

def plot_radar_chart(data1, lower_bound_value, upper_bound_value, lower_ttl, upper_ttl):
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
    


def plot_bar_chart_with_annotations(levels):
    import plotly.graph_objects as go
    import plotly.io as pio
    import time

    special_number = 0
    for l in levels:
        special_number += l[0]
    # Сортировка словаря по ключам и получение отдельных списков значений и ключей
    sorted_data = sorted(level_f.items(), key=lambda item: item[0])
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



def test_result_img(person_name, grouped_metas, levels, result_sum):
    api = GoogleApi(
        service_path='./data/google/se_google_key.json',
        root_folder_id='1wbmhJP3JEsL2_n2bgXaD4yl7PAbx6k_R'
    )

    folder_id = api.folder_here(person_name)
    if folder_id:
        api.del_file(folder_id)
    result = []

    img = plot_bar_chart_with_annotations(levels)
    link = api.create_n_load(
        folder_name=person_name,
        img_path=img,
        img_name='result')
    os.remove(img)
    result.append(link)

    for i in range(5):
        data1 = grouped_metas[i]
        lower_bound_value = levels[i][1] // 10
        upper_bound_value = levels[i][2] // 10
        lower_ttl = levels[i][3]
        upper_ttl = levels[i][4]
        img = plot_radar_chart(data1, lower_bound_value, upper_bound_value, lower_ttl, upper_ttl)
        link = api.create_n_load(
            folder_name=person_name, 
            img_path=img, 
            img_name=str(i))
        os.remove(img)
        result.append(link)

    return result

if __name__ == '__main__':
    row = Row('https://docs.google.com/spreadsheets/d/1hgC7-TI2INK2ZIU7gv82hALETcOnI35iRny5I3oV2KE/export?format=csv&gid=673713785', 40)
    test = Test(row.answer)
    imgs = test_result_img(
        person_name='test',
        grouped_metas=test.metas,
        levels=test.levels,
        result_sum=test.result_sum
    )
    print(imgs)