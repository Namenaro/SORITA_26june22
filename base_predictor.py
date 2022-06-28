from utils.get_pixels import select_points_on_pic_handly
from utils.get_pictures import get_omni_pics
from utils.point import Point
from proofer_by_sampler import Proofer
from situation_finder import SituationFinderInVicinity, SituationFinderRandom
from prediction_sampler import *
from stat_hypo import *
from current_utils import *
import random
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


class SimpleExp:
    def __init__(self, dpoint, run_exp):
        self.dpoint=dpoint
        self.run_exp=run_exp

    def run(self, point):
        new_point = Point(point.x+self.dpoint.x, point.y+self.dpoint.y)
        return self.run_exp(new_point)

class Prediction:
    def __init__(self, p_of_one, sample, p_val, p_abs_diff, simple_exp):
        self.p_of_one = p_of_one
        self.sample = sample
        self.p_val = p_val
        self.p_abs_diff = p_abs_diff #разница по вероятности от того предсказания, которое исправляется этим предсказанием
        self.power=max(p_of_one, 1-p_of_one)#насколько это увереенное предказание

        self.exp = simple_exp
        self.proved_non_trivial = False

class BasePredictor:
    def __init__(self, pic, run_condition):
        self.run_condition=run_condition
        self.name='A'
        self.predictions = []
        self.pic=pic

    def fill_predictions(self, run_exp,radius,trivial_p_one, sample_len):
        for i in range(-radius, radius+1):
            for j in range(-radius, radius+1):
                dpoint = Point(j,i)
                se = SimpleExp(dpoint, run_exp)
                sit_finder = SituationFinderRandom(self.pic, self.run_condition)
                pred_sampler = PredictionSampler(self.pic, se.run, sit_finder)
                pred_sampler.fill_sample(sample_len)
                new_p_of_one=pred_sampler.get_p_of_one()
                num_ones = pred_sampler.get_num_ones()

                p=Prediction(p_of_one=new_p_of_one,
                             sample=pred_sampler.sample,
                             p_val=get_p_value_for_paramentric_case(num_ones, len(pred_sampler.sample), trivial_p_one),
                             p_abs_diff=abs(trivial_p_one-new_p_of_one),
                             simple_exp=se)
                self.predictions.append(p)



    def show_predictions1(self):
        fig, ax = plt.subplots()
        plt.imshow(self.pic, cmap='gray_r')
        point = find_start_point(self.pic, self.run_condition)
        for prediction in self.predictions:
            new_point = Point(point.x +prediction.exp.dpoint.x, point.y +prediction.exp.dpoint.y)
            ax.plot(new_point.x, new_point.y, marker='o', markerfacecolor='red', color='red',
                    linewidth=4)

            if prediction.p_val < 0.00001:
                colorname = 'green'
                ax.plot(new_point.x, new_point.y, marker='o', markerfacecolor=colorname, color=colorname,
                        linewidth=4)
        ax.plot(point.x, point.y, marker='s', markerfacecolor='blue', color='blue')
        plt.show()


    def show_predictions2(self):
        fig, ax = plt.subplots()
        plt.imshow(self.pic, cmap='gray_r')
        point = find_start_point(self.pic, self.run_condition)
        cm=plt.get_cmap('Greens')
        norm = mpl.colors.Normalize(vmin=0, vmax=1)

        for prediction in self.predictions:
            new_point = Point(point.x + prediction.exp.dpoint.x, point.y + prediction.exp.dpoint.y)
            if prediction.p_val < 0.00001:
                val=prediction.power
                str_marker='$'+str(val)+'$'
                c= cm(norm(val))
                ax.plot(new_point.x, new_point.y, marker='s', markerfacecolor=c, color=c, linewidth=4)
                #ax.plot(new_point.x, new_point.y, marker=str_marker, markerfacecolor=c, color=c, linewidth=4, markersize=15)
        sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)
        ax.set_title("насколько это низкоэнтропийное предказание power=max(p_of_one, 1-p_of_one)")
        sm.set_array([])
        ax.plot(point.x, point.y, marker='s', markerfacecolor='blue', color='blue')
        plt.colorbar(sm)
        plt.show()


    def show_predictions3(self):
        fig, ax = plt.subplots()
        plt.imshow(self.pic, cmap='gray_r')
        point = find_start_point(self.pic, self.run_condition)
        cm=plt.get_cmap('Reds')
        norm = mpl.colors.Normalize(vmin=0, vmax=1)

        for prediction in self.predictions:
            new_point = Point(point.x + prediction.exp.dpoint.x, point.y + prediction.exp.dpoint.y)
            if prediction.p_val < 0.00001:
                val=prediction.p_abs_diff
                str_marker='$'+str(val)+'$'
                c= cm(norm(val))
                ax.plot(new_point.x, new_point.y, marker='s', markerfacecolor=c, color=c, linewidth=4)
                #ax.plot(new_point.x, new_point.y, marker=str_marker, markerfacecolor=c, color=c, linewidth=4, markersize=15)
        ax.plot(point.x, point.y, marker='s', markerfacecolor='blue', color='blue')
        sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)
        ax.set_title("разница по вероятности от того предсказания, которое исправляется этим предсказанием")
        sm.set_array([])
        ax.plot(point.x, point.y, marker='s', markerfacecolor='blue', color='blue')
        plt.colorbar(sm)
        plt.show()

    def show_hard_predictions(self, threshold):
        fig, ax = plt.subplots()
        plt.imshow(self.pic, cmap='gray_r')
        point = find_start_point(self.pic, self.run_condition)
        cm = plt.get_cmap('Reds')
        norm = mpl.colors.Normalize(vmin=0, vmax=1)
        counter = 0
        for prediction in self.predictions:
            new_point = Point(point.x + prediction.exp.dpoint.x, point.y + prediction.exp.dpoint.y)
            if prediction.p_val < 0.00001:
                val = prediction.power
                str_marker = '$' + str(val) + '$'
                c = cm(norm(val))
                if val<threshold:
                    continue
                counter+=1
                ax.plot(new_point.x, new_point.y, marker='s', markerfacecolor=c, color=c, linewidth=4)
                # ax.plot(new_point.x, new_point.y, marker=str_marker, markerfacecolor=c, color=c, linewidth=4, markersize=15)
        sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)
        ax.plot(point.x, point.y, marker='s', markerfacecolor='blue', color='blue')
        ax.set_title("разница по вероятности от того предсказания, которое исправляется этим предсказанием")
        sm.set_array([])
        plt.colorbar(sm)
        plt.show()
        print ("num of hard predictions: "+ str(counter))



if __name__ == "__main__":
    pass