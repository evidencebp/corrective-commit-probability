import os
import pandas as pd

from analysis_configuration import lang_name
from configuration import DATA_PATH, ANALYZED_YEAR
from repo_utils import get_valid_repos
from cochange_analysis import cochange_analysis, build_repo_per_year_df, cochange_analysis_by_value
from positives_mle import ccp_estimator

def onboarding_ccp_cochange(repo_file_quality_per_year
                           , repo_file_onboarding_per_year):
    """
        Note that repo_file_quality_per_year uses bug hit ratio and not ccp.
        For change analysis it doesn't matter.
    :param repo_file_quality_per_year:
    :return:
    """
    key = 'repo_name'

    repo_file_quality_per_year_df = build_repo_per_year_df(repo_file_quality_per_year
                                                           , key=key)
    repo_file_onboarding_per_year_df = build_repo_per_year_df(repo_file_onboarding_per_year
                                                         , key=key)
    repo_file_onboarding_per_year_df = repo_file_onboarding_per_year_df[repo_file_onboarding_per_year_df.comming_developers > 9]
    per_year_df = pd.merge(repo_file_quality_per_year_df
                           , repo_file_onboarding_per_year_df
                           , on=[key, 'year'])
    per_year_df['ccp'] = per_year_df.corrective_commits_ratio.map(lambda x: ccp_estimator.estimate_positives(x))

    cochange_analysis(per_year_df
                      , first_metric='ccp'
                      , second_metric='comming_involved_developers_ratio'
                      , first_the_higher_the_better=False
                      , second_the_higher_the_better=True
                      , first_sig_threshold=0.1
                      , second_sig_threshold=0.1
                      , key=key
                      )

def onboarding_ccp_cochange_by_lang(repo_file_quality_per_year
                           , repo_file_onboarding_per_year):
    """
        Note that repo_file_quality_per_year uses bug hit ratio and not ccp.
        For change analysis it doesn't matter.
    :param repo_file_quality_per_year:
    :return:
    """
    key = 'repo_name'
    fixed_variable = 'language'
    control_variables = [fixed_variable]

    repo_file_quality_per_year_df = build_repo_per_year_df(repo_file_quality_per_year
                                                           , key=key
                                                           , control_variables=control_variables)
    repo_file_churn_per_year_df = build_repo_per_year_df(repo_file_onboarding_per_year
                                                         , key=key
                                                         , control_variables=control_variables)
    repo_file_churn_per_year_df = repo_file_churn_per_year_df[(repo_file_churn_per_year_df.comming_developers > 9)
                                                    & (repo_file_churn_per_year_df.language.isin(lang_name))]
    per_year_df = pd.merge(repo_file_quality_per_year_df
                           , repo_file_churn_per_year_df
                           , on=[key, 'year'] + control_variables)
    per_year_df['ccp'] = per_year_df.corrective_commits_ratio.map(lambda x: ccp_estimator.estimate_positives(x))

    cochange_analysis_by_value(per_year_df
                               , first_metric='ccp'
                               , second_metric='comming_involved_developers_ratio'
                               , first_the_higher_the_better=False
                               , second_the_higher_the_better=True
                               , first_sig_threshold=0.1
                               , second_sig_threshold=0.1
                               , fixed_variable=fixed_variable
                               , fixed_values=lang_name
                               , key=key
                               , control_variables=control_variables
                               )


def onboarding_ccp_cochange_by_dev_num_group(repo_file_quality_per_year
                           , repo_file_onboarding_per_year):
    """
        Note that repo_file_quality_per_year uses bug hit ratio and not ccp.
        For change analysis it doesn't matter.
    :param repo_file_quality_per_year:
    :return:
    """
    key = 'repo_name'
    fixed_variable = 'dev_num_group'
    control_variables = [fixed_variable]

    repo_file_quality_per_year_df = build_repo_per_year_df(repo_file_quality_per_year
                                                           , key=key
                                                           , control_variables=control_variables)
    repo_file_churn_per_year_df = build_repo_per_year_df(repo_file_onboarding_per_year
                                                         , key=key
                                                         , control_variables=control_variables)
    repo_file_churn_per_year_df = repo_file_churn_per_year_df[(repo_file_churn_per_year_df.comming_developers > 9)]
    per_year_df = pd.merge(repo_file_quality_per_year_df
                           , repo_file_churn_per_year_df
                           , on=[key, 'year'] + control_variables)
    per_year_df['ccp'] = per_year_df.corrective_commits_ratio.map(lambda x: ccp_estimator.estimate_positives(x))

    cochange_analysis_by_value(per_year_df
                               , first_metric='ccp'
                               , second_metric='comming_involved_developers_ratio'
                               , first_the_higher_the_better=False
                               , second_the_higher_the_better=True
                               , first_sig_threshold=0.1
                               , second_sig_threshold=0.1
                               , fixed_variable=fixed_variable
                               , fixed_values=['small', 'medium', 'large']
                               , key=key
                               , control_variables=control_variables
                               )



def onboarding_ccp_cochange_by_age_group(repo_file_quality_per_year
                           , repo_file_onboarding_per_year):
    """
        Note that repo_file_quality_per_year uses bug hit ratio and not ccp.
        For change analysis it doesn't matter.
    :param repo_file_quality_per_year:
    :return:
    """
    key = 'repo_name'
    fixed_variable = 'age_group'
    control_variables = [fixed_variable]

    repo_file_quality_per_year_df = build_repo_per_year_df(repo_file_quality_per_year
                                                           , key=key
                                                           , control_variables=control_variables)
    repo_file_churn_per_year_df = build_repo_per_year_df(repo_file_onboarding_per_year
                                                         , key=key
                                                         , control_variables=control_variables)
    repo_file_churn_per_year_df = repo_file_churn_per_year_df[(repo_file_churn_per_year_df.comming_developers > 9)]

    per_year_df = pd.merge(repo_file_quality_per_year_df
                           , repo_file_churn_per_year_df
                           , on=[key, 'year'] + control_variables)
    per_year_df['ccp'] = per_year_df.corrective_commits_ratio.map(lambda x: ccp_estimator.estimate_positives(x))

    cochange_analysis_by_value(per_year_df
                               , first_metric='ccp'
                               , second_metric='comming_involved_developers_ratio'
                               , first_the_higher_the_better=False
                               , second_the_higher_the_better=True
                               , first_sig_threshold=0.1
                               , second_sig_threshold=0.1
                               , fixed_variable=fixed_variable
                               , fixed_values=['old', 'medium', 'young']
                               , key=key
                               , control_variables=control_variables
                               )

def run_onboarding_ccp_cochange():

    onboarding_ccp_cochange(repo_file_quality_per_year=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                       , repo_file_onboarding_per_year=os.path.join(DATA_PATH, 'developer_on_boarding.csv'))

    onboarding_ccp_cochange_by_lang(repo_file_quality_per_year=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                       , repo_file_onboarding_per_year=os.path.join(DATA_PATH, 'developer_on_boarding.csv'))

    onboarding_ccp_cochange_by_dev_num_group(repo_file_quality_per_year=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                       , repo_file_onboarding_per_year=os.path.join(DATA_PATH, 'developer_on_boarding.csv'))

    onboarding_ccp_cochange_by_age_group(repo_file_quality_per_year=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                       , repo_file_onboarding_per_year=os.path.join(DATA_PATH, 'developer_on_boarding.csv'))

if __name__ == '__main__':
    run_onboarding_ccp_cochange()
