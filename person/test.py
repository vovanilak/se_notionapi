import os
import sys 
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from config import test
from server.google import GoogleApi
from config.test import kcal
class Test:
    def __init__(self, answers):
        self.answers = answers
        self.ans_kcal = []
        self.metas = self.get_grouped_metas(self.answers)
        self.levels = self.get_levels(self.metas)
        self.result_sum = self.get_result_sum(self.metas)
        self.points = self.result_sum[0]
        self.grade_acse = self.grade(self.points)

    def get_grouped_metas(self, meta):
        lst = []
        for i in range(0, 60, 10):
            lst.append(meta[i:i + 10])
        return lst

    def get_levels(self, grouped_metas):
        return [self.find_level(compet, test.levels) for compet in grouped_metas]
        
    def get_result_sum(self, grouped_metas):
        su = [sum(s) for s in grouped_metas[:-1]]
        res = self.find_level(su, test.level_f)
        return res
    
    @classmethod
    def grade(cls, points):
        grds = list(test.level_f.keys())
        for r in grds:
            if points in range(r):
                return test.level_f[grds[grds.index(r) - 1]]
        return 'Senior'


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

    def do_kcal(self, metas):
        new = [k for k in kcal]
        

if __name__ == "__main__": 
    test = Test([3]*60)
    print(test.result_sum)