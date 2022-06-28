from base_predictor import *



class DerivedPredictor:
    def __init__(self, pic, run_condition, base_predictions):
        self.base_predictions =[]
        for prediction in  base_predictions:
            if prediction.proved_non_trivial:
                self.base_predictions.append(prediction)
        self.pic = pic
        self.run_condition = run_condition
        self.predictions_corrections = []
        self.p_val_threshold = 0.0001

    def check_old_predictions(self, sample_len):
        # перебираем нетривильные предсказания и тестируем их на выживаемость.
        # Для выживщих записываем поправку, для невыживших None
        for prediction in self.base_predictions:
            sit_finder = SituationFinderRandom(self.pic, self.run_condition)
            pred_sampler = PredictionSampler(self.pic, prediction.exp.run_exp, sit_finder)
            pred_sampler.fill_sample(sample_len)
            #pval = get_p_value_for_two_samples(pred_sampler.sample, prediction.sample)
            pval = get_p_value_for_one_sample(pred_sampler.sample, prediction.p_of_one)
            if pval>self.p_val_threshold:
                print(pval)
                self.predictions_corrections.append(None)
            else:
                diff = abs(pred_sampler.get_p_of_one() - prediction.p_of_one)
                self.predictions_corrections.append(diff)

    def show_corrections(self):
        fig, ax = plt.subplots()
        plt.imshow(self.pic, cmap='gray_r')
        cm = plt.get_cmap('Greens')
        norm = mpl.colors.Normalize(vmin=0, vmax=1)
        point = find_start_point(self.pic, self.run_condition)
        for i in range(len(self.predictions_corrections)):
            pld_prediction = self.base_predictions[i]
            correction = self.predictions_corrections[i]
            new_point = Point(point.x + pld_prediction.exp.dpoint.x, point.y + pld_prediction.exp.dpoint.y)
            if correction is None:
                ax.plot(new_point.x, new_point.y, marker='o', markerfacecolor='red', color='red',
                    linewidth=4, alpha=0.3)
            else:
                c = cm(norm(correction))
                ax.plot(new_point.x, new_point.y, marker='s', markerfacecolor=c, color=c, linewidth=4)
                # str_marker = '$' + str(correction) + '$'
                # ax.plot(new_point.x, new_point.y, marker=str_marker, markerfacecolor=c, color=c, linewidth=4, markersize=15)
        sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)
        ax.plot(point.x, point.y, marker='s', markerfacecolor='blue', color='blue')
        ax.set_title("красным неизменившиеся предсказания, зеленым изменившиеся (и насколько) ")
        sm.set_array([])
        plt.colorbar(sm)
        ax.plot(point.x, point.y, marker='s', markerfacecolor='blue', color='blue', alpha=0.3)
        ax.plot(point.x+1, point.y, marker='s', markerfacecolor='blue', color='blue', alpha=0.3)
        plt.show()