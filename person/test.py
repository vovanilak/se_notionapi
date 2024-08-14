import os
import sys 
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from config import test
from server.google import GoogleApi
from config.test import kcal

class Test:
    def __init__(self, answers, verif=[1] * 60):
        self.answers = self.do_kcal(answers)
        self.verif = self.do_kcal(verif)
        self.merged = [round(a + b, 2) for a, b in zip(self.answers, self.verif)]
        self.metas = self.get_grouped_metas(self.merged)
        self.levels = self.get_levels(self.metas)
        self.levels_percent = self.get_levels_percent(self.metas)
        self.result_sum = self.get_result_sum(self.metas)
        self.points = sum(self.merged)
        self.grade_acse = self.grade(self.points)

    def do_kcal(self, metas):
        lst = []
        for i in range(50):
            lst.append(round(metas[i] * test.kcal[i], 2))
        lst.extend(metas[50:])
        return lst

    def get_grouped_metas(self, meta):
        lst = []
        for i in range(0, 60, 10):
            lst.append(meta[i:i + 10])
        return lst

    def normal(self, number, compet):
        return int(round(number / test.max_comp[compet], 2) * 100)

    def get_levels_percent(self, grouped_metas):
        lst = []
        for i in range(5):
            normal = self.normal(sum(grouped_metas[i]), i)
            lst.append(self.find_level(normal, test.level_percent))
        return lst

    def get_levels(self, grouped_metas):
        lst = []
        for i in range(6):
            normal = round(sum(grouped_metas[i]))
            lst.append(self.find_level(normal, test.levels))
        return lst

    def get_result_sum(self, grouped_metas):
        lst = []
        for i in range(5):
            normal = sum(grouped_metas[i]) / test.max_comp[i] * test.percent_max_comp[i] * 100
            lst.append(normal)
        su = round(sum(lst) / sum(test.percent_max_comp))
        res = self.find_level(su, test.level_percent)
        return res
    
    @classmethod
    def grade(cls, points):
        grds = list(test.level_f.keys())
        for r in grds:
            if points in range(r):
                return test.level_f[grds[grds.index(r) - 1]]
        return 'Senior'


    def find_level(self, meta, levels):
        sum_meta = meta
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
        

if __name__ == "__main__": 
    test = Test([2]*60, [1]*60)
    print(test.levels_percent)