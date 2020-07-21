import os
import pandas as pd

from analysis_configuration import lang_name
from configuration import DATA_PATH, ANALYZED_YEAR
from cochange_analysis import cochange_analysis, build_repo_per_year_df, cochange_analysis_by_value
from positives_mle import ccp_estimator
from repo_utils import get_valid_repos

def churn_ccp_cochange(repo_file_quality_per_year
                           , repo_file_churn_per_year):
    """
        Note that repo_file_quality_per_year uses bug hit ratio and not ccp.
        For change analysis it doesn't matter.
    :param repo_file_quality_per_year:
    :return:
    """
    key = 'repo_name'

    repo_file_quality_per_year_df = build_repo_per_year_df(repo_file_quality_per_year
                                                           , key=key)
    repo_file_churn_per_year_df = build_repo_per_year_df(repo_file_churn_per_year
                                                         , key=key)
    repo_file_churn_per_year_df = repo_file_churn_per_year_df[repo_file_churn_per_year_df.base_year_developers > 9]
    per_year_df = pd.merge(repo_file_quality_per_year_df
                           , repo_file_churn_per_year_df
                           , on=[key, 'year'])

    per_year_df['ccp'] = per_year_df.corrective_commits_ratio.map(lambda x: ccp_estimator.estimate_positives(x))

    cochange_analysis(per_year_df
                      , first_metric='ccp'
                      , second_metric='continuing_developers_ratio'
                      , first_the_higher_the_better=False
                      , second_the_higher_the_better=True
                      , first_sig_threshold=0.1
                      , second_sig_threshold=0.1
                      , key=key
                      )


def churn_ccp_cochange_by_lang(repo_file_quality_per_year
                           , repo_file_churn_per_year):
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
    repo_file_churn_per_year_df = build_repo_per_year_df(repo_file_churn_per_year
                                                         , key=key
                                                         , control_variables=control_variables)
    repo_file_churn_per_year_df = repo_file_churn_per_year_df[(repo_file_churn_per_year_df.base_year_developers > 9)
                                                    & (repo_file_churn_per_year_df.language.isin(lang_name))]
    per_year_df = pd.merge(repo_file_quality_per_year_df
                           , repo_file_churn_per_year_df
                           , on=[key, 'year'] + control_variables)

    per_year_df['ccp'] = per_year_df.corrective_commits_ratio.map(lambda x: ccp_estimator.estimate_positives(x))

    cochange_analysis_by_value(per_year_df
                               , first_metric='ccp'
                               , second_metric='continuing_developers_ratio'
                               , first_the_higher_the_better=False
                               , second_the_higher_the_better=True
                               , first_sig_threshold=0.1
                               , second_sig_threshold=0.1
                               , fixed_variable='language'
                               , fixed_values=lang_name
                               , key=key
                               , control_variables=control_variables
                               )


def churn_ccp_cochange_by_dev_num_group(repo_file_quality_per_year
                           , repo_file_churn_per_year):
    """
        Note that repo_file_quality_per_year uses bug hit ratio and not ccp.
        For change analysis it doesn't matter.
    :param repo_file_quality_per_year:
    :return:
    """
    key = 'repo_name'
    control_variables = ['dev_num_group']
    #import pdb; pdb.set_trace()
    repo_file_quality_per_year_df = build_repo_per_year_df(repo_file_quality_per_year
                                                           , key=key
                                                           , control_variables=control_variables)
    repo_file_churn_per_year_df = build_repo_per_year_df(repo_file_churn_per_year
                                                         , key=key
                                                         , control_variables=control_variables)
    repo_file_churn_per_year_df = repo_file_churn_per_year_df[(repo_file_churn_per_year_df.base_year_developers > 9)]
    per_year_df = pd.merge(repo_file_quality_per_year_df
                           , repo_file_churn_per_year_df
                           , on=[key, 'year'] + control_variables)

    per_year_df['ccp'] = per_year_df.corrective_commits_ratio.map(lambda x: ccp_estimator.estimate_positives(x))

    cochange_analysis_by_value(per_year_df
                               , first_metric='ccp'
                               , second_metric='continuing_developers_ratio'
                               , first_the_higher_the_better=False
                               , second_the_higher_the_better=True
                               , first_sig_threshold=0.1
                               , second_sig_threshold=0.1
                               , fixed_variable='dev_num_group'
                               , fixed_values=['small', 'medium', 'large']
                               , key=key
                               , control_variables=control_variables
                               )

def churn_ccp_cochange_by_age(repo_file_quality_per_year
                           , repo_file_churn_per_year):
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
    repo_file_churn_per_year_df = build_repo_per_year_df(repo_file_churn_per_year
                                                         , key=key
                                                         , control_variables=control_variables)
    repo_file_churn_per_year_df = repo_file_churn_per_year_df[(repo_file_churn_per_year_df.base_year_developers > 9)]
    per_year_df = pd.merge(repo_file_quality_per_year_df
                           , repo_file_churn_per_year_df
                           , on=[key, 'year'] + control_variables)
    per_year_df['ccp'] = per_year_df.corrective_commits_ratio.map(lambda x: ccp_estimator.estimate_positives(x))

    cochange_analysis_by_value(per_year_df
                               , first_metric='ccp'
                               , second_metric='continuing_developers_ratio'
                               , first_the_higher_the_better=False
                               , second_the_higher_the_better=True
                               , first_sig_threshold=0.1
                               , second_sig_threshold=0.1
                               , fixed_variable='age_group'
                               , fixed_values=['old', 'medium', 'young']
                               , key=key
                               , control_variables=control_variables
                               )


def run_churn_ccp_cochange():


    churn_ccp_cochange(repo_file_quality_per_year=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                       , repo_file_churn_per_year=os.path.join(DATA_PATH, 'invovled_developers_churn.csv'))

    churn_ccp_cochange_by_lang(repo_file_quality_per_year=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                       , repo_file_churn_per_year=os.path.join(DATA_PATH, 'invovled_developers_churn.csv'))

    churn_ccp_cochange_by_age(repo_file_quality_per_year=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                              , repo_file_churn_per_year=os.path.join(DATA_PATH, 'invovled_developers_churn.csv'))

    churn_ccp_cochange_by_dev_num_group(repo_file_quality_per_year=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                              , repo_file_churn_per_year=os.path.join(DATA_PATH, 'invovled_developers_churn.csv'))

if __name__ == '__main__':
    run_churn_ccp_cochange()
