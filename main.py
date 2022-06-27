from utils.get_pixels import select_points_on_pic_handly
from utils.get_pictures import get_omni_pics
from utils.point import Point
from proofer_by_sampler import Proofer
from situation_finder import SituationFinderInVicinity, SituationFinderRandom
from prediction import *
from stat_hypo import *

import random
import matplotlib.pyplot as plt
import numpy as np

pics = get_omni_pics()
pic = np.array(pics[0])
#select_points_on_pic_handly(pic)
x = pic.flatten()

def get_hist_unnormed(seq) -> dict:
     hist = {}
     for i in seq:
         hist[i] = hist.get(i, 0) + 1
     return hist

def get_hist_normed(seq)-> dict:
    hist= get_hist_unnormed(seq)
    num_elements = 0
    for key in hist.keys():
        num_elements+=hist[key]
    for key in hist.keys():
        hist[key]=hist[key]/num_elements
    return hist

def show_hist(hist, ax):
    ps = []
    keys = []
    for key in hist.keys():
        keys.append(str(key))
        ps.append(hist[key])
    ax.bar(keys, ps, color='#774444', edgecolor="k", linewidth=2)
    ax.set_ylabel('p')
    ax.set_ylim([0, 1])
    ax.set_title('Histogram')

def sense_0(point, picture): #hist on omni pic ={255: 0.9264399092970521, 0: 0.07356009070294785}
    xlen=picture.shape[1]
    ylen=picture.shape[0]
    if point.x >= 0 and point.y >= 0 and point.x < xlen and point.y < ylen:
        val = picture[point.y, point.x]
        if  val == 0:
            return True
        else:
            return False
    return None

def runA(point):
    return sense_0(point, pic)

def empty_run(point):
    return True

def collateral_1A(point):
    new_point = Point(x=point.x+1, y=point.y)
    return runA(new_point)

def find_start_point(picture, run_exp):
    Xmax = picture.shape[1]
    Ymax = picture.shape[0]
    while True:
        point = Point(random.randrange(Xmax), random.randrange(Ymax))
        if run_exp(point):
            print ("start_point = "+ str(point))
            return point

def check_possible_collateral():
    print("right shift test")
    run_condition =runA
    run_exp = collateral_1A
    actual_p_for_success_of_exp=0.07356009070294785
    start_point = find_start_point(pic, run_condition)
    #sit_finder = SituationFinderInVicinity(pic, start_point, run_condition)
    sit_finder = SituationFinderRandom(pic, run_condition)
    proofer = Proofer(pic,  run_exp, actual_p_for_success_of_exp, sit_finder, max_attempts=20)
    success, p_val, sample= proofer.try_sample()
    print ("pair condition-collateral cheked: " + str(success) + ', p_val = '+ str(p_val)+ ", sample size=" + str(len(sample)))


    sit_finder = SituationFinderRandom(pic, run_condition)
    pred_sampler = PredictionSampler(pic, collateral_1A, sit_finder)
    pred_sampler.fill_sample(250)
    print("p(1)=" + str(pred_sampler.get_p_of_one()))
    pred_sampler.show_hist()

def test_sample_against_sample():
    NO_CONDITION_SIZE=60
    CONDITION_SIZE=3

    sit_finder1 = SituationFinderRandom(pic, empty_run)
    pred_sampler1 = PredictionSampler(pic, collateral_1A, sit_finder1)
    pred_sampler1.fill_sample(NO_CONDITION_SIZE)
    print("p(1)=" + str(pred_sampler1.get_p_of_one()))

    sit_finder2 = SituationFinderRandom(pic, runA)
    pred_sampler2 = PredictionSampler(pic, collateral_1A, sit_finder2)
    pred_sampler2.fill_sample(CONDITION_SIZE)
    print("p(1|1->)=" + str(pred_sampler1.get_p_of_one()))

    pval=get_p_value_for_two_samples(pred_sampler1.sample, pred_sampler2.sample)
    print("two samples PVAL=" + str(pval))





def start_info():
    hist = get_hist_normed(x)
    print(hist)
    fig, ax = plt.subplots()
    show_hist(hist, ax)
    plt.show()

#check_possible_collateral()
test_sample_against_sample()

