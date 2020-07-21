import os
import pandas as pd

from configuration import DATA_PATH
from repo_utils import get_non_fork_repos

def English_hit_rate_analysis():

    # TODO - the value was set using manual examination. Update in case of need.
    positive_quantile= 0.04

    df = get_non_fork_repos()
    df['English_hit_rate'] = 1.0*df.English_hits/df.commits

    print("Negative ccp English median", df[df.y2019_ccp < 0].English_hit_rate.quantile(0.5))
    print("Valid ccp English median", df[(df.y2019_ccp > 0) & (df.y2019_ccp <  1)].English_hit_rate.quantile(0.5))
    print("The matching quantile for psotives is "
            , positive_quantile
            , df[df.y2019_ccp > 0].English_hit_rate.quantile(positive_quantile))

def length_analysis(negative_ccp_file):
    df = pd.read_csv(negative_ccp_file)

    print("median diffrerences")
    print("Negative ccp message length median", df.message_length.quantile(0.5))
    print("Random sample length is ", 229.0 / df.message_length.quantile(0.5), "larger")

    print("Negative ccp message length 90 quantile", df.message_length.quantile(0.9))
    print("Random sample length is ", 742.0 / df.message_length.quantile(0.9), "larger")

def run_English_analysis():
    English_hit_rate_analysis()
    length_analysis(os.path.join(DATA_PATH, 'negative_ccp_commit_samples.csv'))

if __name__ == '__main__':
    run_English_analysis()
