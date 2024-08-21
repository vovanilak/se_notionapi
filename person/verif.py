import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import pandas as pd
import json
from config.secret import URL_TEST

class VerifTest:
    def __init__(self, row_number):
        self.row_number = row_number - 2
        data = self.read_res(self.row_number)
        self.ver_answers = data[0]
        self.real_bal = data[1]
        self.correct_answer = self.readjson()
        self.bal_list = self.is_correct_answers(self.ver_answers, self.correct_answer)

    def read_res(self, row_number, table_path=URL_TEST, start_answer_column=8):
        df = pd.read_csv(table_path)
        ans = df.iloc[row_number, start_answer_column:].to_dict()
        bal = df.iloc[row_number, 2].split(' / ')[0] # 2 колонка - это ответы
        return ans, int(bal)

    def is_correct_answers(self, ver_answers, right_answers):
        bal = [0] * 50 + [1] * 10
        def easy_sent(sent):
            return ''.join(sent.lower().strip().split())
        for ask in ver_answers:
            if easy_sent(ver_answers[ask]) == easy_sent(right_answers[ask]):
                ind = list(right_answers.values()).index(right_answers[ask])
                bal[ind] = 1
                #print(bal[-1])
                #print(ver_answers[ask], right_answers[ask], sep='\n', end='\n\n')
        return bal

    def cheсk(self):
        def check_word_in_df(df, word):
            mask = df.map(lambda x: word.lower() in str(x).lower())
            return mask.any().any()
        df = pd.read_csv(URL_TEST)
        num = 0
        for search_string in self.correct_answer:
            if not check_word_in_df(df, search_string):
                print(search_string)
        return num

    def excel2dict(self, table_path='data/answer.xlsx'):
        df = pd.read_excel(table_path)
        df.set_index('Компетенция', inplace=True)
        dct = dict(zip(df['Вопросы'], df['Ответы']))
        return dct
        

    def savedict(self, dct):
        with open('data/answer.json', 'w') as f:
            json.dump(dct, f)

    def readjson(self, file='data/answer.json'):
        with open(file, 'r') as f:
            return json.load(f)
    

if __name__ == '__main__':
    vt = VerifTest(58) #30 31 
    print(vt.bal_list, vt.real_bal, sum(vt.bal_list))

