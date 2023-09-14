import numpy as np
#import DTLearner
import RTLearner
#import LinRegLearner
class BagLearner(object):
    def __init__(self, learner, kwargs, bags, boost, verbose = False):
        self.learners = []
        self.kwargs = kwargs
        for i in range(bags):
            self.learners.append(learner(**kwargs))
        self.bags = bags
        self.boost = boost
        self.verbose = verbose

    def author(self):
        return "vpatel436"

    def add_evidence(self, data_x, data_y):
        for i in self.learners:
            point = np.random.choice(data_x.shape[0], data_x.shape[0], replace=True)
            i.add_evidence(data_x[point], data_y[point])
    def query(self, points):
        y_vals =[]
        for i in range(self.bags):
            curr = self.learners[i]
            y_vals.append(curr.query(points))
        return np.mean(y_vals, axis =0)


if __name__ == "__main__":
    print("This is a Bag Learner\n")
