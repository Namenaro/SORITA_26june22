from utils.get_pixels import select_random_coord_on_pic, get_coords_for_q_radius
from utils.point import Point
from stat_hypo import get_p_value_for_paramentric_case


import matplotlib.pyplot as plt

class SimpleConditinalSampler:
    def __init__(self, pic, run_condition, run_exp, actual_p_for_success_of_exp, start_point):
        self.p_value_thresh = 0.0001
        self.max_sample_len = 200
        self.pic = pic
        self.sit_finder = SituationFinder(pic, start_point, run_condition)
        self.run_exp = run_exp
        self.sample = []
        self.actual_p_for_success_of_exp = actual_p_for_success_of_exp
        self.min_sample_size=1

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
        current_p_val = 1
        success = False
        for i in range(self.max_sample_len):
            point = self.sit_finder.get_next_uncheked_situation()
            if point is None:
                break # кончились ситуации

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


class SituationFinder:
    def __init__(self, pic, start_point, run_condition):
        self.pic=pic
        self.start_point = start_point
        self.run_condition = run_condition

        self.checked_points=set()
        self.checked_and_sucsessed = set()

        self.current_vicinity_radius =0
        self.points_to_check = [start_point]

    def _generate_next_batch(self):
        self.current_vicinity_radius+=1
        self.points_to_check = get_coords_for_q_radius(self.start_point,
                                                       self.current_vicinity_radius,
                                                       XMAX=self.pic.shape[1],
                                                       YMAX=self.pic.shape[0])
        print("generated points: "+ str(len(self.points_to_check)))

    def get_next_uncheked_situation(self)->Point:
        while True:
            if len(self.points_to_check) == 0:
                self._generate_next_batch()
            if len(self.points_to_check)==0:
                return None
            candidate = self.points_to_check.pop()
            if self.run_condition(candidate):
                return candidate

    def register_res(self, point, res):
        self.checked_points.add(point)
        if res is True:
            self.checked_and_sucsessed.add(point)

    def draw(self):
        fig, ax = plt.subplots()
        plt.imshow(self.pic, cmap='gray_r')

        for point in self.checked_points:
            ax.plot(point.x, point.y, marker='o',  markerfacecolor='red', markersize=15, color='red',
                    linewidth=4)
        for point in self.checked_and_sucsessed:
            ax.plot(point.x, point.y, marker='o',  markerfacecolor='green', markersize=12, color='green',
                    linewidth=4)
        plt.show()
