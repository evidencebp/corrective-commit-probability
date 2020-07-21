import os
import pandas as pd
from analysis_configuration import EARLIEST_ANALYZED_YEAR, GITHUB_START_YEAR

from configuration import FIGURES_PATH
from decile_analysis import plot_deciles
from repo_utils import get_valid_repos

def plot_dev_num():
    df = get_valid_repos()

    cutting_points = [0, 1] \
                     + [int(df.authors.quantile(i*0.1)) for i in range(1,10)] \
                     + [int(df.authors.quantile(0.99))]\
                     + [float("inf")]
    df['dev_num_sets'] = pd.cut(df.authors
                                    , cutting_points
                                )
    df = df.sort_values('dev_num_sets')
    plot_deciles(df
                 , grouping_column='dev_num_sets'
                 , metric_column='y2019_ccp'
                 , title="Number of Developers vs. CCP"
                 , xaxis_title= "Developers (single, deciles and 99%)"
                 , output_file=os.path.join(FIGURES_PATH, 'ccp_by_dev_num_boxplot.png'))


if __name__ == '__main__':
    plot_dev_num()
