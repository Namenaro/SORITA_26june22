import numpy as np
import scipy.stats.distributions as dist
from scipy import stats

import matplotlib.pyplot as plt

def MY_test_propportion_one(num_ones, sample_len, p_one):
    pass

def MY_test_propportion_two(num_successes1, sample_size1,num_successes2, sample_size2):
    pass

def get_binary_sample(sample_len, p_one):
    sample = stats.bernoulli.rvs(p_one, size=sample_len)
    return sample
#
def test_MV():
    fig, ax = plt.subplots()
    X=[]
    Y=[]
    p1 = 0.2
    p2 = 0.1
    for i in range(1,100):
        sample1 = get_binary_sample(sample_len=i, p_one=p1)
        sample2 = get_binary_sample(sample_len=i, p_one=p2)
        ttest, pval = stats.mannwhitneyu(sample1, sample2, use_continuity=False, alternative="two-sided")
        X.append(i)
        Y.append(pval)
    ax.plot(X, Y, marker='o', markerfacecolor='blue', markersize=10, color='skyblue', linewidth=4)
    ax.set_title("Поведение критерия Манна-Уитни, разница между монетами " + str(abs(p2-p1)))
    ax.set_xlabel("размер выборки (каждой из двух) ")
    ax.set_ylabel("p-значение критерия Манна_Уитни ")
    plt.show()


if __name__ == "__main__":
    test_MV()
