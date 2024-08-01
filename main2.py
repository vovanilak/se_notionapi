from answer import *



def main(who, row_number ):

    with open('./data/notion/new_version2.json', 'r') as f:
        data = json.load(f)
    row = Row('https://docs.google.com/spreadsheets/d/1hgC7-TI2INK2ZIU7gv82hALETcOnI35iRny5I3oV2KE/export?format=csv&gid=673713785',37)
    person = Person(row.data, row.answer, 'ID Legioner')
    test = Test(row.answer)

    imgs = test_result_img(
        person_name=person.title_value,
        grouped_metas=test.metas,
        levels=test.levels,
        result_sum=test.result_sum
    )

    pg = liga_n_staff(
        main=data,
        levels=person.levels,
        grade_acse=test.grade_acse,
        metas=test.metas,
        img_links=imgs,
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
    

    return pub.json()