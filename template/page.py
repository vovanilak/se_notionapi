import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from config.test import level_text
import json

from person.source import Row
from person.test import Test

def liga_n_staff(
    main, # json-шаблон
    levels,
    levels_percent,
    source_answers,
    source_verif,
    test_result_sum,
    grade_acse,
    img_links=None
):
    counter = 1
    flag = 0
    for i in range(len(main)):
        if "table" in main[i]:
            # даблица подкомпетенции
            if len(main[i]['table']["children"]) > 9 and len(main[i]['table']["children"][0]['table_row']['cells']) >= 3:
                children = main[i]['table']["children"]
                for j in range(10):
                    #print(children[j + 1])
                    children[j + 1]["table_row"]['cells'][2][0]['text']['content'] = str(source_answers[counter - 1][j])
                    if counter < 6:
                        children[j + 1]["table_row"]['cells'][3][0]['text']['content'] = str(source_verif[counter - 1][j])
                    #if source_answers[counter - 1][j] < 3:
                    if source_verif[counter - 1][j] == 0:
                        children[j + 1]["table_row"]['cells'][2][0]['annotations'] = {'color': 'red', 'bold': True}
                        children[j + 1]["table_row"]['cells'][3][0]['annotations'] = {'color': 'red', 'bold': True}
                #children[j + 2]["table_row"]['cells'][2][0]['text']['content'] = str(levels[counter - 1][0])

            # итог подкомпетенции с грейдом
            elif len(main[i]['table']["children"]) == 3 and len(main[i]['table']["children"][0]['table_row']['cells']) == 3 and flag:
                children = main[i]['table']["children"]
                children[0]['table_row']['cells'][2][0]['text']['content'] = str(levels_percent[counter - 1][0])
                children[1]['table_row']['cells'][0][0]['text']['content'] = str(levels_percent[counter - 1][3])
                children[1]['table_row']['cells'][2][0]['text']['content'] = str(levels_percent[counter - 1][4])
                children[2]['table_row']['cells'][0][0]['text']['content'] = str(levels_percent[counter - 1][1])
                children[2]['table_row']['cells'][1][0]['text']['content'] = str(levels_percent[counter - 1][0])
                children[2]['table_row']['cells'][2][0]['text']['content'] = str(levels_percent[counter - 1][2])
                counter += 1
                
            # баллы итоговые с грейдом
            elif len(main[i]['table']["children"]) == 2 and not flag:
                children = main[i]['table']["children"]
                children[0]['table_row']['cells'][0][0]['text']['content'] = str(test_result_sum[3])
                children[0]['table_row']['cells'][2][0]['text']['content'] = str(test_result_sum[4])
                children[1]['table_row']['cells'][0][0]['text']['content'] = str(test_result_sum[1])
                children[1]['table_row']['cells'][1][0]['text']['content'] = str(test_result_sum[0])
                children[1]['table_row']['cells'][2][0]['text']['content'] = str(test_result_sum[2])

            # итоговая таблица с рекомендациями
            elif len(main[i]['table']["children"]) == 8 and not flag:
                children = main[i]['table']["children"]
                for j in range(6):
                    children[j + 1]["table_row"]['cells'][2][0]['text']['content'] = str(levels_percent[j][0])
                children[-1]["table_row"]['cells'][2][0]['text']['content'] = str(test_result_sum[0])
        
        elif "image" in main[i] and counter == 1: 
            del main[i]['image']
            main[i]['type'] = 'embed'
            main[i]['object'] = 'block'
            main[i]['embed'] = {'url': img_links[0]}
            counter += 1

        elif "quote" in main[i]:
            flag = 1

        elif 'heading_1' in main[i] and 'children' in main[i]['heading_1']:
            main[i]['heading_1']['children'] = liga_n_staff(
                main=main[i]['heading_1']['children'],
                levels=levels,
                levels_percent=levels_percent,
                grade_acse=grade_acse,
                source_answers=source_answers,
                source_verif=source_verif,
                img_links=img_links,
                test_result_sum=test_result_sum
                )

        elif i == 0 and 'heading_2' in main[i]:
            text = f'По результатам ассесмента перед вами специалист с предварительно подтвержденным грейдом уровня {grade_acse} ({test_result_sum[0]} пойнтов).'
            main[i]['heading_2']['rich_text'][0]['plain_text'] = text
            main[i]['heading_2']['rich_text'][0]['text']['content'] = text

        elif i == 3 and 'paragraph' in main[i] and counter == 1:
            text = level_text[grade_acse]
            main[i]['paragraph']['rich_text'] = [{"type": "text", "text": {"content": text}, "plain_text": text}]
            
        elif 'callout' in main[i-1]:
            text = level_text[grade_acse]
            main[i]['paragraph']['rich_text'] = [{"type": "text", "text": {"content": text}, "plain_text": text}]
        

        #elif "callout" in main[i]:
        #    counter -= 1

    return main

if __name__ == '__main__':
    with open('./data/notion/new_version2.json', 'r') as f:
        data = json.load(f) 
    row = Row('https://docs.google.com/spreadsheets/d/1hgC7-TI2INK2ZIU7gv82hALETcOnI35iRny5I3oV2KE/export?format=csv&gid=673713785',40)
    #print(row.data['id'], row.data['name'])
    person = Person(row.data, row.answer, 'ID Legioner')
    test = Test(row.answer)
    
    pg = liga_n_staff(
        main=data,
        levels=person.levels,
        grade_acse=test.grade_acse,
        metas=test.metas,
        img_links=['https://a.d-cd.net/bYAAAgBYPOA-1920.jpg']*6,
        test_result_sum=test.result_sum
    )

    #print(pg)

