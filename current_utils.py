from utils.get_pixels import select_points_on_pic_handly
from utils.get_pictures import get_omni_pics
from utils.point import Point
from proofer_by_sampler import Proofer
from situation_finder import SituationFinderInVicinity, SituationFinderRandom
from prediction_sampler import *
from stat_hypo import *
import random

def get_pic():
    pics = get_omni_pics()
    pic = np.array(pics[0])
    return pic

def sense_0(point, picture): #hist on omni pic ={255: 0.9264399092970521, 0: 0.07356009070294785}
    xlen=picture.shape[1]
    ylen=picture.shape[0]
    if point.x >= 0 and point.y >= 0 and point.x < xlen and point.y < ylen:
        val = picture[point.y, point.x]
        if val == 0:
            return True
    return False




def get_hist_unnormed(seq) -> dict:
    hist = {}
    for i in seq:
        hist[i] = hist.get(i, 0) + 1
    return hist



def get_hist_normed(seq) -> dict:
    hist = get_hist_unnormed(seq)
    num_elements = 0
    for key in hist.keys():
        num_elements += hist[key]
    for key in hist.keys():
        hist[key] = hist[key] / num_elements
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

def find_start_point(picture, run_exp):
    Xmax = picture.shape[1]
    Ymax = picture.shape[0]
    while True:
        point = Point(random.randrange(Xmax), random.randrange(Ymax))
        if run_exp(point):
            print ("start_point = "+ str(point))
            return point