import os
import pandas as pd

from analysis_configuration import EARLIEST_ANALYZED_YEAR
from configuration import DATA_PATH
from positives_mle import ccp_estimator
from stability_analysis import analyze_stability

def ccp_stability(repo_file_quality_per_year):

    metric_name = 'ccp'

    metric_per_year_df = pd.read_csv(repo_file_quality_per_year)
    metric_per_year_df[metric_name] =metric_per_year_df['corrective_commits_ratio'].map(ccp_estimator.estimate_positives)

    print(analyze_stability(metric_per_year_df
                      , key='repo_name'
                      , metric_name=metric_name
                      , time_column='year'
                      , minimal_time=EARLIEST_ANALYZED_YEAR
                      , control_variables=[]
                      , min_cnt_column='commits'
                      , min_cnt_threshold=200
                            ))

def run_ccp_stability():
    return ccp_stability(repo_file_quality_per_year = os.path.join(DATA_PATH
                                                            , 'project_user_contribution_stats.csv'))


if __name__ == '__main__':
    run_ccp_stability()