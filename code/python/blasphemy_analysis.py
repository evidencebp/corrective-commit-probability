import os
import pandas as pd

from analysis_configuration import lang_name, EARLIEST_ANALYZED_YEAR
from configuration import DATA_PATH, ANALYZED_YEAR
from repo_utils import get_valid_repos
from cochange_analysis import cochange_analysis, build_repo_per_year_df, cochange_analysis_by_value
from stability_analysis import analyze_stability

def blasphemy_ccp_cochange(repo_file_quality_per_year
                           , repo_file_blasphemy_per_year):
    """
        Note that repo_file_quality_per_year uses bug hit ratio and not ccp.
        For change analysis it doesn't matter.
    :param repo_file_quality_per_year:
    :return:
    """
    key = 'repo_name'

    repo_file_quality_per_year_df = build_repo_per_year_df(repo_file_quality_per_year
                                                           , key=key)
    repo_file_blasphemy_per_year_df = build_repo_per_year_df(repo_file_blasphemy_per_year
                                                         , key=key)
    per_year_df = pd.merge(repo_file_quality_per_year_df
                           , repo_file_blasphemy_per_year_df
                           , on=[key, 'year'])

    cochange_analysis(per_year_df
                      , first_metric='corrective_commits_ratio'
                      , second_metric='blasphemy_hit_rates'
                      , first_the_higher_the_better=False
                      , second_the_higher_the_better=False
                      , first_sig_threshold=0.1
                      , second_sig_threshold=0.01
                      , key=key
                      )


def blasphemy_ccp_cochange_by_lang(repo_file_quality_per_year
                           , repo_file_blasphemy_per_year):
    """
        Note that repo_file_quality_per_year uses bug hit ratio and not ccp.
        For change analysis it doesn't matter.
    :param repo_file_quality_per_year:
    :return:
    """
    key = 'repo_name'
    control_variables = ['language']
    #import pdb; pdb.set_trace()
    repo_file_quality_per_year_df = build_repo_per_year_df(repo_file_quality_per_year
                                                           , key=key
                                                           , control_variables=control_variables)
    repo_file_blasphemy_per_year_df = build_repo_per_year_df(repo_file_blasphemy_per_year
                                                         , key=key
                                                         , control_variables=control_variables)
    repo_file_blasphemy_per_year_df = repo_file_blasphemy_per_year_df[(repo_file_blasphemy_per_year_df.language.isin(lang_name))]
    per_year_df = pd.merge(repo_file_quality_per_year_df
                           , repo_file_blasphemy_per_year_df
                           , on=[key, 'year'] + control_variables)

    cochange_analysis_by_value(per_year_df
                               , first_metric='corrective_commits_ratio'
                               , second_metric='blasphemy_hit_rates'
                               , first_the_higher_the_better=False
                               , second_the_higher_the_better=False
                               , first_sig_threshold=0.1
                               , second_sig_threshold=0.01
                               , fixed_variable='language'
                               , fixed_values=lang_name
                               , key=key
                               , control_variables=control_variables
                               )


def blasphemy_ccp_cochange_by_dev_num_group(repo_file_quality_per_year
                           , repo_file_blasphemy_per_year):
    """
        Note that repo_file_quality_per_year uses bug hit ratio and not ccp.
        For change analysis it doesn't matter.
    :param repo_file_quality_per_year:
    :return:
    """
    key = 'repo_name'
    control_variables = ['dev_num_group']
    repo_file_quality_per_year_df = build_repo_per_year_df(repo_file_quality_per_year
                                                           , key=key
                                                           , control_variables=control_variables)
    repo_file_blasphemy_per_year_df = build_repo_per_year_df(repo_file_blasphemy_per_year
                                                         , key=key
                                                         , control_variables=control_variables)
    per_year_df = pd.merge(repo_file_quality_per_year_df
                           , repo_file_blasphemy_per_year_df
                           , on=[key, 'year'] + control_variables)

    cochange_analysis_by_value(per_year_df
                               , first_metric='corrective_commits_ratio'
                               , second_metric='blasphemy_hit_rates'
                               , first_the_higher_the_better=False
                               , second_the_higher_the_better=False
                               , first_sig_threshold=0.1
                               , second_sig_threshold=0.01
                               , fixed_variable='dev_num_group'
                               , fixed_values=['small', 'medium', 'large']
                               , key=key
                               , control_variables=control_variables
                               )

def blasphemy_ccp_cochange_by_age(repo_file_quality_per_year
                           , repo_file_blasphemy_per_year):
    """
        Note that repo_file_quality_per_year uses bug hit ratio and not ccp.
        For change analysis it doesn't matter.
    :param repo_file_quality_per_year:
    :return:
    """
    key = 'repo_name'
    control_variables = ['age_group']
    repo_file_quality_per_year_df = build_repo_per_year_df(repo_file_quality_per_year
                                                           , key=key
                                                           , control_variables=control_variables)
    repo_file_blasphemy_per_year_df = build_repo_per_year_df(repo_file_blasphemy_per_year
                                                         , key=key
                                                         , control_variables=control_variables)
    per_year_df = pd.merge(repo_file_quality_per_year_df
                           , repo_file_blasphemy_per_year_df
                           , on=[key, 'year'] + control_variables)

    cochange_analysis_by_value(per_year_df
                               , first_metric='corrective_commits_ratio'
                               , second_metric='blasphemy_hit_rates'
                               , first_the_higher_the_better=False
                               , second_the_higher_the_better=False
                               , first_sig_threshold=0.1
                               , second_sig_threshold=0.01
                               , fixed_variable='age_group'
                               , fixed_values=['old', 'medium', 'young']
                               , key=key
                               , control_variables=control_variables
                               )


def run_blasphemy_ccp_cochange():


    blasphemy_ccp_cochange(repo_file_quality_per_year=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                       , repo_file_blasphemy_per_year=os.path.join(DATA_PATH, 'ccp_by_quality_terms_by_repo_per_year.csv'))

    blasphemy_ccp_cochange_by_lang(repo_file_quality_per_year=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                       , repo_file_blasphemy_per_year=os.path.join(DATA_PATH, 'ccp_by_quality_terms_by_repo_per_year.csv'))

    blasphemy_ccp_cochange_by_age(repo_file_quality_per_year=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                              , repo_file_blasphemy_per_year=os.path.join(DATA_PATH, 'ccp_by_quality_terms_by_repo_per_year.csv'))

    blasphemy_ccp_cochange_by_dev_num_group(repo_file_quality_per_year=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                              , repo_file_blasphemy_per_year=os.path.join(DATA_PATH, 'ccp_by_quality_terms_by_repo_per_year.csv'))

def run_blasphemy_stability():
    key = 'repo_name'
    repo_file_blasphemy_per_year = os.path.join(DATA_PATH, 'ccp_by_quality_terms_by_repo_per_year.csv')
    repo_file_blasphemy_per_year_df = build_repo_per_year_df(repo_file_blasphemy_per_year
                                                         , key=key)

    print(analyze_stability(repo_file_blasphemy_per_year_df
                      , key=key
                      , metric_name='blasphemy_hit_rates'
                      , time_column='year'
                      , minimal_time=EARLIEST_ANALYZED_YEAR
                      , control_variables=[]
                      , min_cnt_column='commits'
                      , min_cnt_threshold=200
                        ))

if __name__ == '__main__':
    run_blasphemy_ccp_cochange()
    run_blasphemy_stability()