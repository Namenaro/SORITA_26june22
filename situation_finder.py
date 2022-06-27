from utils.point import Point
from utils.get_pixels import select_random_coord_on_pic, get_coords_for_q_radius
from random import randint
import matplotlib.pyplot as plt


class SituationFinderInVicinity:
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
                self.checked_points.add(candidate)
                return candidate

    def register_res(self, point, res):
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



class SituationFinderRandom:
    def __init__(self, pic,  run_condition):
        self.pic = pic
        self.checked_points = set()
        self.unchecked_points=[]
        self.run_condition = run_condition
        for i in range(pic.shape[0]):
            for j in range(pic.shape[1]):
                self.unchecked_points.append(Point(j,i))
        self.checked_and_sucsessed = set()

    def get_next_uncheked_situation(self)->Point:
        while True:
            if len(self.unchecked_points) == 0:
                return None
            index = randint(0, len(self.unchecked_points)-1)
            candidate_point = self.unchecked_points[index]

            if self.run_condition(candidate_point):
                self.checked_points.add(candidate_point)
                self.unchecked_points.pop(index)
                return candidate_point
            self.unchecked_points.pop(index)

    def register_res(self, point, res):
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