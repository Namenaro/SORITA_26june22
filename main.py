from utils.get_pixels import select_points_on_pic_handly
from utils.get_pictures import get_omni_pics



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

def show_hist(hist,ax):
    ps = []
    keys = []
    for key in hist.keys():
        keys.append(str(key))
        ps.append(hist[key])
    ax.bar(keys, ps, color='#774444', edgecolor="k", linewidth=2)
    ax.set_ylabel('p')
    ax.set_ylim([0, 1])
    ax.set_title('Histogram')


hist = get_hist_normed(x)
print(hist)

fig, ax = plt.subplots()
show_hist(hist, ax)
plt.show()




