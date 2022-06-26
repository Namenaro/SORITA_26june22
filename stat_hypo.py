import numpy as np
import scipy.stats.distributions as dist
from statsmodels.stats.proportion import proportions_ztest

def get_p_value_for_two_samples(num_successes1, sample_size1,num_successes2, sample_size2):
    # чем ниже п-валью, тем больше вероятность, что выборки "разные"
    # т.е. чем ниже, тем лучше
    counts = np.array([num_successes1, num_successes2])
    nobs = np.array([sample_size1, sample_size2])
    stat, pval = proportions_ztest(counts, nobs)
    return pval

def get_p_value_for_paramentric_case(num_successes1, sample_size1, p):
    # чем ниже п-валью, тем больше вероятность, что выборка взята из монеты с параметром p
    # т.е. чем ниже, тем лучше
    stat, pval = proportions_ztest(num_successes1, sample_size1, p)
    return pval

def MY_test_propportion_one(num_ones, sample_len, p_one):
    pass

def MY_test_propportion_two(num_successes1, sample_size1,num_successes2, sample_size2):
    pass


def test_one_sample():
    p_one = 0.07
    num_ones = 5
    sample_len = 10

    stat, pval = proportions_ztest(num_ones, sample_len, p_one)

    print(pval)


if __name__ == "__main__":
    test_one_sample()