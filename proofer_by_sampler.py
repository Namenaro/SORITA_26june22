
from utils.point import Point
from stat_hypo import get_p_value_for_paramentric_case


import matplotlib.pyplot as plt

class Proofer:
    def __init__(self, pic,  run_exp, actual_p_for_success_of_exp, sit_finder, max_attempts):
        self.p_value_thresh = 0.0001
        self.max_sample_len = max_attempts
        self.pic = pic
        self.sit_finder = sit_finder
        self.run_exp = run_exp
        self.sample = []
        self.actual_p_for_success_of_exp = actual_p_for_success_of_exp
        self.min_sample_size=3

    def check_p_val(self):
        sample_size1 = len(self.sample)
        p = self.actual_p_for_success_of_exp
        num_successes1=0
        for res in self.sample:
            if res==True:
                num_successes1+=1
        p_val = get_p_value_for_paramentric_case(num_successes1, sample_size1, p)
        return p_val


    def try_sample(self):
        print("try_sample to find statistic proof for hypo...")
        current_p_val = 1
        success = False
        for i in range(self.max_sample_len):
            point = self.sit_finder.get_next_uncheked_situation()
            if point is None:
                break # кончились ситуации
            print("next situation...")
            result = self.run_exp(point)
            self.sit_finder.register_res(point, result)
            if result is not None:
                self.sample.append(result)
                if (len(self.sample)) < self.min_sample_size:
                    continue
                current_p_val = self.check_p_val()
                if current_p_val <= self.p_value_thresh:
                    success = True
                    self.sit_finder.draw()
                    break # доказали гипотезу!
        return success, current_p_val, self.sample


