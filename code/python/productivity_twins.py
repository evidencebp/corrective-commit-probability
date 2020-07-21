import os
import pandas as pd

from configuration import DATA_PATH

def analyze_productivity_twins(twins_file):
    df = pd.read_csv(twins_file)

    df['cap_pairs'] = (df.cap_match + df.cap_mismatch)
    df['cap_match_ratio'] = df.cap_match / (df.cap_pairs)

    # TODO - It seems that fro Kendel we shouldn't use the number of authors
    # It looks like it should be a (author, repo) number of tuples
    # See https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient
    df['cap_kendel'] = (df.cap_match - df.cap_mismatch)/ (df.authors * (df.authors -1)/2)


    df['users_above_11_commits_per_above11_users_pairs'] = (df.match_users_above_11_commits_per_above11_users
                       + df.mismatch_users_above_11_commits_per_above11_users)
    df['users_above_11_commits_per_above11_users_match_ratio'] = (
            df.match_users_above_11_commits_per_above11_users / df.users_above_11_commits_per_above11_users_pairs)

    df['users_above_11_commits_per_above11_users_kendel'] = (
        df.match_users_above_11_commits_per_above11_users - df.mismatch_users_above_11_commits_per_above11_users
        )/ (df.authors * (df.authors -1)/2)

    print(df)

    return df

def run_analyze_productivity_twins():
    return analyze_productivity_twins(twins_file=os.path.join(DATA_PATH
                                                              , 'productivity_twins.csv'))

if __name__ == '__main__':
    df = run_analyze_productivity_twins()



