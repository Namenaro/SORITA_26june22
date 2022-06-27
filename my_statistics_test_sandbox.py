import numpy as np
import scipy.stats.distributions as dist
from scipy import stats

import matplotlib.pyplot as plt
from math import sqrt

def z_proportion(num_ones, sample_len, p_one):
    #https://mse.msu.ru/wp-content/uploads/2020/03/%D0%9B%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-6-%D0%9F%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0-%D0%B3%D0%B8%D0%BF%D0%BE%D1%82%D0%B5%D0%B7.pdf
    p=num_ones/sample_len #доля признака в выборке
    q0=1-p_one
    z=(p-p_one)/sqrt(p_one*q0/sample_len)  #z сходится по распределению к стандартной нормальной величине при sample_len → ∞.
    # рассчитываем  p-value
    pvalue = 2 * dist.norm.cdf(-np.abs(z))  # Multiplied by two indicates a two tailed testing.
    return pvalue



def get_binary_sample(sample_len, p_one):
    sample = stats.bernoulli.rvs(p_one, size=sample_len)
    return sample
#
def test_MV():
    fig, ax = plt.subplots()
    X=[]
    Y=[]
    p1 = 0.2
    p2 = 0.9
    for i in range(1,100):
        sample1 = get_binary_sample(sample_len=i, p_one=p1)
        sample2 = get_binary_sample(sample_len=i, p_one=p2) #np.array([0,0,0]) #
        ttest, pval = stats.mannwhitneyu(sample1, sample2, use_continuity=False, alternative="two-sided")
        print (pval)
        X.append(i)
        Y.append(pval)
    ax.plot(X, Y, marker='o', markerfacecolor='blue', markersize=10, color='skyblue', linewidth=4)
    ax.set_title("Поведение критерия Манна-Уитни, разница между монетами " + str(abs(p2-p1)))
    ax.set_xlabel("размер выборки (каждой из двух) ")
    ax.set_ylabel("p-значение критерия Манна-Уитни ")
    ax.set_ylim([-0.1, 1.1])
    plt.show()

def show_z_proportion():
    fig, ax = plt.subplots()
    X = []
    Y = []
    p_1=0.1
    p_2=0.2
    for i in range(1,100):
        sample = get_binary_sample(sample_len=i, p_one=p_1)
        num_ones=sum(sample)
        print(num_ones)
        p_val = z_proportion(num_ones, sample_len=len(sample), p_one=p_2)
        X.append(i)
        Y.append(p_val)
    ax.plot(X, Y, marker='o', markerfacecolor='blue', markersize=10, color='skyblue', linewidth=4)
    ax.set_title("Поведение z-теста доли в выборке, разница между монетами " + str(abs(p_2 - p_1)))
    ax.set_xlabel("размер выборки (каждой из двух) ")
    ax.set_ylabel("p-значение z-теста доли в выборке ")
    ax.set_ylim([-0.1, 1.1])
    plt.show()

def test_z_propportion():
    num_ones=2
    sample_len=20
    p_one=0.2
    p_val = z_proportion(num_ones, sample_len, p_one)
    print (p_val)

if __name__ == "__main__":
    #test_MV()
    test_z_propportion()
    #show_z_proportion()
