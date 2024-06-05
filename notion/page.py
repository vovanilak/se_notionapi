import json

def user_page(test_result, test_result_sum, test_result_img: list, json_file):

    img_links = test_result_img()
    
    with open(json_file, 'r') as file:
        main = json.load(file)
    counter = 1
    for i in range(len(main)):
        if "table" in main[i]:
            if len(main[i]['table']["children"]) > 2 and len(main[i]['table']["children"][0]['table_row']['cells']) == 3:
                children = main[i]['table']["children"]
                for j in range(10):
                    children[j + 1]["table_row"]['cells'][2][0]['text']['content'] = str(test_result[counter]['meta'][j])
                    if test_result[counter]['meta'][j] < 3:
                        children[j + 1]["table_row"]['cells'][2][0]['annotations'] = {'color': 'red', 'bold': True}
                children[j + 2]["table_row"]['cells'][2][0]['text']['content'] = str(test_result[counter]['level'][0])
                
            elif len(main[i]['table']["children"]) == 2 and counter < 7:
                children = main[i]['table']["children"]
                children[0]['table_row']['cells'][0][0]['text']['content'] = str(test_result[counter]['level'][3])
                children[0]['table_row']['cells'][2][0]['text']['content'] = str(test_result[counter]['level'][4])
                children[1]['table_row']['cells'][0][0]['text']['content'] = str(test_result[counter]['level'][1])
                children[1]['table_row']['cells'][1][0]['text']['content'] = str(test_result[counter]['level'][0])
                children[1]['table_row']['cells'][2][0]['text']['content'] = str(test_result[counter]['level'][2])
                

            elif len(main[i]['table']["children"]) == 2:
                children = main[i]['table']["children"]
                children[0]['table_row']['cells'][0][0]['text']['content'] = str(test_result_sum[3])
                children[0]['table_row']['cells'][2][0]['text']['content'] = str(test_result_sum[4])
                children[1]['table_row']['cells'][0][0]['text']['content'] = str(test_result_sum[1])
                children[1]['table_row']['cells'][1][0]['text']['content'] = str(test_result_sum[0])
                children[1]['table_row']['cells'][2][0]['text']['content'] = str(test_result_sum[2])

            elif len(main[i]['table']["children"]) == 8:
                children = main[i]['table']["children"]
                for j in range(1, 7):
                    children[j]["table_row"]['cells'][2][0]['text']['content'] = str(test_result[j]['level'][0])
                children[-1]["table_row"]['cells'][2][0]['text']['content'] = str(test_result_sum[0])
        elif "image" in main[i] and counter < 8:
            main[i]['image']['external']['url'] = img_links[counter - 1]
            counter += 1
    return main