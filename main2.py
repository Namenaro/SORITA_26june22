from utils.get_pixels import select_points_on_pic_handly
from utils.get_pictures import get_omni_pics
from utils.point import Point
from proofer_by_sampler import Proofer
from situation_finder import SituationFinderInVicinity, SituationFinderRandom
from prediction_sampler import *
from stat_hypo import *
from current_utils import *
from base_predictor import *
from derived_predictor import *

import random
import matplotlib.pyplot as plt
import numpy as np

# Составление "алфавита" (рождение неслипшихся точек) для конкретной картинки
pic = get_pic()

# ШАГ 1. Получаем предсказание для случайного пикселя
def empty_run(point):
    return True

def runA(point):
    return sense_0(point, pic)

def runA_right_NotA(point):
    dpoint = Point(1,0)
    if runA(point):
        new_point=Point(point.x+dpoint.x, point.y+dpoint.y)
        if runA(new_point) is False:
            return True
    return False

sit_finder = SituationFinderRandom(pic, empty_run)
pred_sampler = PredictionSampler(pic, runA, sit_finder)
pred_sampler.fill_sample(350)
p_of_one = pred_sampler.get_p_of_one()
#pred_sampler.show_hist()
print ("p_of_one = " + str(p_of_one))
#  результат: A=true очень редкое (не не разовое!) событие

# ШАГ 2: Для A=true собираем список предсказний, для которых доказана нетривиальность ( с учетом распространения определенности)
# Для данного дескриптора(A=true) храним список всех его нетривиальных предсказаний, среди них выделяем группу "уверенных".
# При обходе картинки дескриптор ставится в тех точках, в которых выполнился базовый факт И все уверенные нетривиальные
# предсказания.

predictor = BasePredictor(pic, runA)
predictor.fill_predictions(runA, radius=7, trivial_p_one =p_of_one, sample_len=160)
#predictor.show_hard_predictions(threshold=0.9)
#predictor.show_predictions3()
predictor.show_predictions1()
#predictor.show_predictions2()
predictor.show_prediction4()

# ШАГ 3. Глянем какие выживут предсказания при добавлении факта, что справа случилось неА
new_run_condition = runA_right_NotA
dp = DerivedPredictor(pic, new_run_condition, predictor.predictions)
dp.check_old_predictions(sample_len=5)
dp.show_corrections()

