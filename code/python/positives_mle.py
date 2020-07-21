
class PositivesMLE(object):
    def __init__(self
                 , recall
                 , fpr):
        self.recall = recall
        self.fpr = fpr

    def range_low_bound(self):
        """
            Looking for the hit_rate range for which pr is a probability, in [0,1]
            Solving for f(x)=0
            getting x = Fpr
        :return:
        """
        return self.fpr

    def range_high_bound(self):
        """
            Looking for the hit_rate range for which pr is a probability, in [0,1]
            Solving for f(x) = 1
            getting x = recall
        :return:
        """
        return self.recall

    def is_in_range(self,
                     hit_rate):
        return (hit_rate <= self.range_high_bound()
                and hit_rate >= self.range_low_bound())

    def estimate_positives(self
                            , hit_rate):
        """
            Use the formula
            pr = (hr − Fpr)/(recall − Fpr)
            which is
            f(x) = (x-Fpr)/(recall -Fpr)
            See paper for details
        :param self:
        :param hit_rate:
        :return:
        """
        return (hit_rate-self.fpr)/(self.recall -self.fpr)

    def get_formula(self):
        return ("f(x)="
                + str(round(1/(self.recall -self.fpr),3)) + "*x "
                + str(round(-self.fpr/(self.recall -self.fpr),3)))


# Values are taken from the languistic model performance on the test set
ccp_estimator = PositivesMLE(0.84
                     , 0.042)
#print("ccp", ccp_estimator.get_formula())
refactor_estimator = PositivesMLE(0.61
                     , 0.02)

#print("rfactor", refactor_estimator.get_formula())
