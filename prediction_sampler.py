from situation_finder import *
import matplotlib.pyplot as plt

class PredictionSampler:
    def __init__(self, pic, run_collateral, sit_finder):
        self.pic=pic
        self.run_collateral=run_collateral
        self.sit_finder=sit_finder
        self.sample = []


    def fill_sample(self, attemts):
        for _ in range(attemts):
            point = self.sit_finder.get_next_uncheked_situation()
            outcome = self.run_collateral(point)
            if outcome is not None:
                self.sample.append(outcome)

    def get_hist_unnormed(self):
        hist = {}
        for outcome in self.sample:
            hist[outcome] = hist.get(outcome, 0) + 1
        return hist

    def get_hist_normed(self):
        hist = self.get_hist_unnormed()
        num_elements = 0
        for key in hist.keys():
            num_elements += hist[key]
        for key in hist.keys():
            hist[key] = hist[key] / num_elements
        return hist

    def show_hist(self):
        fig, ax = plt.subplots()
        hist = self.get_hist_normed()
        ps = []
        keys = []
        for key in hist.keys():
            keys.append(str(key))
            ps.append(hist[key])
        ax.bar(keys, ps, color='#774444', edgecolor="k", linewidth=2)
        ax.set_ylabel('p')
        ax.set_ylim([0, 1])
        ax.set_title('Histogram')
        plt.show()

    def get_p_of_one(self):
        hist = self.get_hist_normed()
        return hist.get(True, 0)

    def get_num_ones(self):
        hist = self.get_hist_unnormed()
        return hist.get(True, 0)



