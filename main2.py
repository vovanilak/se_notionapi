from answer import *
from config.secret import *
from config.start import *
from user.source import Row
from answer.test import Test
from answer.plot import test_result_img
from template.page import liga_n_staff
from template.properties import info_prop
from notion.search import query_notion
from notion.posting import post_page2db
import json


class Result:
    def __init__(self, who, row_number):
        with open(JSON_FILE, 'r') as f:
            self.data = json.load(f)
        self.who = who
        self.row = Row(who_link[who], row_number)
        self.test = Test(self.row.answer)

    def get_imgs(self): 
        imgs = test_result_img(
            person_name=self.row.name,
            grouped_metas=self.test.metas,
            levels=self.test.levels,
            result_sum=self.test.result_sum
        )
        print(imgs)
        return imgs

    def get_page(self):
        pg = liga_n_staff(
            main=self.data,
            levels=self.test.levels,
            grade_acse=self.test.grade_acse,
            metas=self.test.metas,
            img_links=self.get_imgs(),
            test_result_sum=self.test.result_sum
        )
        return pg

    def get_prop(self, title_value, relation_card=None):
        pr = info_prop(
            title_value=title_value,
            title_name=who_prop[self.who],
            row_info=self.row.data,
            result_points=self.test.result_sum[0],
            levels=self.test.levels,
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
        
    def get_relation_card(self):
        link = query_notion(val=self.row.name)
        return link

    def run(self):
        card_name = {'Легионер': self.row.id, 'Штатный Сотрудник': self.row.name}

        pr = self.get_prop(
            title_value=card_name[self.who]
        )

        pg = self.get_page()
        res = self.post_page(pr, pg, who_db[self.who])
        if self.who == 'Легионер':

            pr = self.get_prop(
                title_value=tmp[self.who],
                relation_card=res['url']
            )

            self.post_page(pr, [], DATABASE_LIGA_PERSON)
        print(res)
        return res

def main():
    result = Result('Штатный Сотрудник', 52)
    r = result.run()
    return r

if __name__ == '__main__':
    main()