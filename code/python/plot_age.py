import os
import pandas as pd

from analysis_configuration import EARLIEST_ANALYZED_YEAR, GITHUB_START_YEAR
from configuration import FIGURES_PATH
from decile_analysis import plot_deciles
from repo_utils import get_valid_repos

def plot_age():
    df = get_valid_repos()
    df = df[df.start_year >= GITHUB_START_YEAR]
    plot_deciles(df
                 , grouping_column='age'
                 , metric_column='y2019_ccp'
                 , title="Age vs. CCP"
                 , xaxis_title="Age (years)"
                 , output_file=os.path.join(FIGURES_PATH, 'ccp_by_age_boxplot.png'))


def age_groups_stats():
    
    df = get_valid_repos()
    df = df[df.start_year >= EARLIEST_ANALYZED_YEAR]
    df['age_group'] = pd.cut(df.start_year, [0
        , EARLIEST_ANALYZED_YEAR - 1
        , df[df.start_year >= EARLIEST_ANALYZED_YEAR].start_year.quantile(0.25)
        , df[df.start_year >= EARLIEST_ANALYZED_YEAR].start_year.quantile(0.75)
        , float("inf")])

    g = df.groupby('age_group').agg({'y2019_ccp' : 'mean', 'repo_name' : 'count'})
    g['ratio'] = g['repo_name']/len(df)
    print(g)

if __name__ == '__main__':
    plot_age()
    age_groups_stats()
