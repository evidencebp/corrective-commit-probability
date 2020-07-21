import os
import pandas as pd

from analysis_configuration import lang_name
from configuration import DATA_PATH, ANALYZED_YEAR
from repo_utils import get_valid_repos
from cochange_analysis import cochange_analysis, build_repo_per_year_df, cochange_analysis_by_value\
    , cochange_with_control

def coupling_ccp_cochange(repo_file_quality_per_year
                           , repo_file_coupling_per_year):
    """
        Note that repo_file_quality_per_year uses bug hit ratio and not ccp.
        For change analysis it doesn't matter.
    :param repo_file_quality_per_year:
    :return:
    """
    key = 'repo_name'

    repo_file_quality_per_year_df = build_repo_per_year_df(repo_file_quality_per_year
                                                           , key=key)
    repo_file_coupling_per_year_df = build_repo_per_year_df(repo_file_coupling_per_year
                                                         , key=key)
    per_year_df = pd.merge(repo_file_quality_per_year_df
                           , repo_file_coupling_per_year_df
                           , on=[key, 'year'])
    repos = get_valid_repos()
    per_year_df = pd.merge(per_year_df
                           , repos
                           , on=[key])

    cochange_analysis(per_year_df
                      , first_metric='corrective_commits_ratio'
                      , second_metric='avg_capped_files'
                      , first_the_higher_the_better=False
                      , second_the_higher_the_better=False
                      , first_sig_threshold=0.1
                      , second_sig_threshold=1
                      , key=key
                      )

    cochange_with_control(per_year_df
                          , first_metric='corrective_commits_ratio'
                          , second_metric='avg_capped_files'
                          , first_the_higher_the_better=False
                          , second_the_higher_the_better=False
                          , first_sig_threshold=0.1
                          , second_sig_threshold=1
                          , key=key
                          )

def run_coupling_ccp_cochange():
    coupling_ccp_cochange(repo_file_quality_per_year=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                       , repo_file_coupling_per_year=os.path.join(DATA_PATH, 'coupling_by_repo.csv'))


if __name__ == '__main__':
    run_coupling_ccp_cochange()
