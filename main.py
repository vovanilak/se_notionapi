from config.secret import *
import pprint
from config.start import *
from person.source import Row
from person.test import Test
from person.plot import test_result_img
from template.page import liga_n_staff
from template.properties import info_prop
from notion.posting import post_page2db
from person.plot import uguu_links
from person.verif import VerifTest
import json


class MainProcess:
    def __init__(self, who, row_number, row_test=0):
        with open(JSON_FILE, 'r') as f:
            self.data = json.load(f)
        self.who = who
        self.row = Row(whoau[who]['url'], row_number)
        self.row_test = row_test
        if self.row_test:
            self.vt = VerifTest(self.row_test)
            self.test = Test(answers=self.row.answer, verif=self.vt.bal_list)
        else:
            self.test = Test(answers=self.row.answer)

    def get_imgs(self): 
        imgs = test_result_img(
            person_name=self.row.name,
            grouped_metas=self.test.metas,
            levels=self.test.levels,
            levels_percent=self.test.levels_percent,
            result_sum=self.test.result_sum
        )
        return imgs
    
    def get_tmp_imgs(self):
        imgs = uguu_links(
            grouped_metas=self.test.metas,
            levels=self.test.levels_percent,
            result_sum=self.test.result_sum
        )
        return imgs

    def get_page(self, imgs):
        pg = liga_n_staff(
            main=self.data,
            levels=self.test.levels,
            levels_percent=self.test.levels_percent,
            grade_acse=self.test.grade_acse,
            source_answers=self.test.grouped_answers,
            source_verif=self.test.grouped_verif,
            img_links=imgs,
            test_result_sum=self.test.result_sum
        )

        return pg

    def get_prop(self, title_value, title_name, relation_card=None):
        pr = info_prop(
            title_value=title_value,
            title_name=title_name, # whoau[self.who]['column_name'],
            row_info=self.row.data,
            result_points=self.test.result_sum[0],
            levels=self.test.levels_percent,
            grade_acse=self.test.grade_acse,
            relation_card=relation_card,
        )

        return pr

    def post_page(self, pr, pg, db):
        pub = post_page2db(
            properties=pr,
            page_content=pg,
            database_id=db,
            emoji='😎'
        )
        return pub
    
    def do_pretty(self):
        txt = ''
        for m, l, k in zip(self.test.metas, self.test.levels, self.test.levels_percent):
            txt += f'{m}\n{l}\n{k}\n\n'
        txt += f'\n{self.test.result_sum}'
        return txt
    

    def run(self):
        card_name = {'Легионер': self.row.id, 'Штатный Сотрудник': self.row.name}

        #pg = self.get_page(['https://drive.google.com/file/d/1q8hcUK7RObb1zbAwDzccv5myaQN5jbtn/preview'])
        pg = self.get_page(self.get_imgs())
        if self.who == 'Штатный Сотрудник':
            pg = pg[:-6]
            
        pr = self.get_prop(
            title_value=card_name[self.who],
            title_name=whoau[self.who]['column_name'],
        )

        res = self.post_page(pr, pg, whoau[self.who]['db'])
        if self.who == 'Легионер':
            pr = self.get_prop(
                title_value=self.row.id,
                title_name='ID Person',
                relation_card=res['url'].split('/')[-1].split('-')[-1] # https://www.notion.so/s-e/0108241SE-f416ee110a904c0c9a244c97d2682ecf 
            )
            person_res = self.post_page(pr, [], DATABASE_LIGA_PERSON)

        return res

def main():
    mp = MainProcess('Легионер', 55, 108)
    #r = mp.get_prop(title_name='ID Legioner', title_value='Петя')
    r = mp.run()
    print(
        mp.test.levels_percent, 
        mp.test.grade_acse, 
        mp.test.result_sum,
        mp.test.grouped_answers, 
        mp.test.grouped_verif, 
        sep='\n\n'
    )
    
    return r 
    
if __name__ == '__main__':
    print(main(), sep='\n\n') #main()