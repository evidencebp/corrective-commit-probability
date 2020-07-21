import os
import pandas as pd

from configuration import DATA_PATH, ANALYZED_YEAR
from repo_utils import get_valid_repos

def churn_analysis(churn_file):
    df = get_valid_repos()
    churn = pd.read_csv(churn_file)
    churn = churn[churn.year == ANALYZED_YEAR-1]

    df = pd.merge(df, churn, on='repo_name')

    g = df.groupby('quality_group', as_index=False).agg(
        {'continuing_developers_ratio' : 'mean'})
    print("Churn by quality group")
    print(g)
    print("Lift", round(g[g.quality_group == 'Top 10'].iloc[0].continuing_developers_ratio
                        / g[g.quality_group == 'Others'].iloc[0].continuing_developers_ratio -1.0, 2))

    return df


def onboarding_analysis(onboarding_file):
    df = get_valid_repos()
    churn = pd.read_csv(onboarding_file)
    churn = churn[churn.year == ANALYZED_YEAR]

    df = pd.merge(df, churn, on='repo_name')
    g = df.groupby('quality_group', as_index=False).agg(
        {'comming_involved_developers_ratio' : 'mean'})
    print("Onboarding by quality group")
    print(g)
    print("Lift", round(g[g.quality_group == 'Top 10'].iloc[0].comming_involved_developers_ratio
                        / g[g.quality_group == 'Others'].iloc[0].comming_involved_developers_ratio -1.0, 2))

    return df

def run_churn_analysis():

    churn_analysis(churn_file=os.path.join(DATA_PATH
                            , 'invovled_developers_churn.csv'))

    return onboarding_analysis(onboarding_file=os.path.join(DATA_PATH
                            , 'developer_on_boarding.csv'))

if __name__ == '__main__':
    df = run_churn_analysis()

