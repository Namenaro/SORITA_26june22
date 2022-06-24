from utils.get_pixels import select_points_on_pic_handly
from utils.get_pictures import get_omni_pics
from utils.point import Point
from clever_sampler import SimpleConditinalSampler
import random


import matplotlib.pyplot as plt
import numpy as np

pics = get_omni_pics()
pic = pics[0]
#select_points_on_pic_handly(pic)
x = np.array(pic).flatten()

def get_hist_unnormed(seq) -> dict:
     hist = {}
     for i in seq:
         hist[i] = hist.get(i, 0) + 1
     return hist

def get_hist_normed(seq)-> dict:
    hist= get_hist_unnormed(seq)
    num_elements =0
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

def collateral_1A(point):
    new_point = Point(x=point.x+1, y=point.y)
    return runA(new_point)

def find_start_point(picture, run_exp):
    Xmax = picture.shape()[1]
    Ymax = picture.shape()[0]
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
    start_point=find_start_point(pic, run_condition)
    sampler = SimpleConditinalSampler(pic, run_condition, run_exp, actual_p_for_success_of_exp, start_point)
    success, p_val, sample= sampler.try_sample()
    print ("cheked: " + str(success) + ', p_val = '+ str(p_val)+ ", sanmple size=" + str(len(sample)))

def start_info():
    hist = get_hist_normed(x)
    print(hist)
    fig, ax = plt.subplots()
    show_hist(hist, ax)
    plt.show()

check_possible_collateral()


