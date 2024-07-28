import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from datetime import datetime
from answer.test import Test
from user.source import Row
from config.test import level_f
import pandas as pd

class Person:
    def __init__(self, source_row, answer, who):
        test_result = Test(answer)
        if who in ('Name', 'ID Person'):
            self.title_value=source_row['name'] # значение заголовка (Петя, Вася)
        else:
            self.title_value=source_row['id'],
        self.title_name=who # название титульника: ID Legioner, ID Person, Name
        self.row_info=source_row
        self.result_points=test_result.result_sum[0]
        self.relation_card=None # для персональных карточек
        self.levels=test_result.levels
        self.grade_acse=self.grade_acse(self.result_points)
        

    @classmethod
    def grade_acse(cls, grade):
        grds = list(level_f.keys())
        for r in grds:
            if grade in range(r):
                return level_f[grds[grds.index(r) - 1]]
        return 'Senior'

    def get_attributes_dict(self):
        attributes_dict = {}
        for attr_name in dir(self):
            if not attr_name.startswith("__") and not callable(getattr(self, attr_name)) and attr_name != 'row_info':
                attributes_dict[attr_name] = getattr(self, attr_name)
        return attributes_dict


if __name__ == '__main__':
    row = Row('https://docs.google.com/spreadsheets/d/1hgC7-TI2INK2ZIU7gv82hALETcOnI35iRny5I3oV2KE/export?format=csv&gid=673713785',30)
    #print(row.data['id'], row.data['name'])
    person = Person(row.data, row.answer, 'ID Legioner')
    print(person.get_attributes_dict())
