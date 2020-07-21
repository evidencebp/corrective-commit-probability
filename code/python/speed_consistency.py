import os
import pandas as pd

import configuration

from analysis_configuration import lang_name, EARLIEST_ANALYZED_YEAR
from cochange_analysis import cochange_analysis, build_repo_per_year_df, cochange_analysis_by_value
from configuration import DATA_PATH, ANALYZED_YEAR
from confusion_matrix import ConfusionMatrix
from repo_utils import get_valid_repos


def speed_consistency(commits_per_user_file):

    trep = get_valid_repos()

    users_per_project = pd.read_csv(commits_per_user_file)
    users_per_project = users_per_project[users_per_project.repo_name.isin(trep.repo_name.unique())]

    users_per_project_cur = users_per_project[users_per_project.year == ANALYZED_YEAR].copy()
    users_per_project_cur = users_per_project_cur.rename(columns={
        'users' : 'cur_users'
        , 'commits': 'cur_commits'
        , 'users_above_11' : 'cur_users_above_11'
        , 'users_above_11_commits_per_above11_users': 'cur_users_above_11_commits_per_above11_users'
        , 'users_capped_commit': 'cur_users_capped_commit'
        , 'users_above_11_500_cap_per_above11_users': 'cur_users_above_11_500_cap_per_above11_users'
    })
    # commit_per_user
    users_per_project_cur['cur_commit_per_user'] = users_per_project_cur.cur_commits/users_per_project_cur.cur_users
    # users_capped_commit_per_user
    users_per_project_cur['cur_users_capped_commit_per_user'] = users_per_project_cur.cur_users_capped_commit/users_per_project_cur.cur_users

    users_per_project_prev = users_per_project[users_per_project.year == (ANALYZED_YEAR-1)].copy()
    users_per_project_prev = users_per_project_prev.rename(columns={
        'users' : 'prev_users'
        , 'commits': 'prev_commits'
        , 'users_above_11' : 'prev_users_above_11'
        , 'users_above_11_commits_per_above11_users': 'prev_users_above_11_commits_per_above11_users'
        , 'users_capped_commit': 'prev_users_capped_commit'
        , 'users_above_11_500_cap_per_above11_users': 'prev_users_above_11_500_cap_per_above11_users'
    })
    # commit_per_user
    users_per_project_prev['prev_commit_per_user'] = users_per_project_prev.prev_commits/users_per_project_prev.prev_users
    # users_capped_commit_per_user
    users_per_project_prev['prev_users_capped_commit_per_user'] = (users_per_project_prev.prev_users_capped_commit/
                                                                  users_per_project_prev.prev_users)

    upp_adjacent = pd.merge(users_per_project_cur, users_per_project_prev, on='repo_name')

    print("Users Pearson", upp_adjacent.corr()['cur_users']['prev_users'])
    print("Users above 11 Pearson", upp_adjacent.corr()['cur_users_above_11']['prev_users_above_11'])
    print("Commits Pearson", upp_adjacent.corr()['cur_commits']['prev_commits'])
    print("Capped commits Pearson", upp_adjacent.corr()['cur_users_capped_commit']['prev_users_capped_commit'])
    print("Commits per user Pearson", upp_adjacent.corr()['cur_commit_per_user']['prev_commit_per_user'])
    print("Commits per user above 11 Pearson"
          , upp_adjacent.corr()['cur_users_above_11_commits_per_above11_users']['prev_users_above_11_commits_per_above11_users'])
    print("Capped commits per user Pearson"
          , upp_adjacent.corr()['cur_users_capped_commit_per_user']['prev_users_capped_commit_per_user'])


    print("Capped commits, above 11 Pearson"
          , upp_adjacent.corr()['cur_users_above_11_500_cap_per_above11_users']['prev_users_above_11_500_cap_per_above11_users'])


    return upp_adjacent

def quality_and_speed(commits_per_user_file):

    trep = get_valid_repos()
    trep = trep[['repo_name', 'quality_group']]
    users_per_project = pd.read_csv(commits_per_user_file)
    users_per_project = pd.merge(users_per_project, trep, on='repo_name')

    users_per_project_cur = users_per_project[users_per_project.year == ANALYZED_YEAR].copy()
    # commit_per_user
    users_per_project_cur['commit_per_user'] = users_per_project_cur.commits/users_per_project_cur.users
    # users_capped_commit_per_user
    users_per_project_cur['users_capped_commit_per_user'] = users_per_project_cur.users_capped_commit/users_per_project_cur.users

    g = users_per_project_cur.groupby(['quality_group']
                        , as_index=False).agg({'repo_name' : 'count'
                                                , 'commit_per_user': 'mean'
                                                , 'users_above_11_commits_per_above11_users': 'mean'
                                                , 'users_capped_commit_per_user' : 'mean'
                                                , 'users_above_11_500_cap_per_above11_users': 'mean'
                                               }
                                              )

    print("quality and speed")
    print(g)
    print("Commit per user top 10 lift"
        , (g[g.quality_group == 'Top 10'].iloc[0].commit_per_user
          / g[g.quality_group == 'Others'].iloc[0].commit_per_user) -1
    )

    print("Capped commit per user above 11 top 10 lift"
        ,  (g[g.quality_group == 'Top 10'].iloc[0].users_above_11_500_cap_per_above11_users
          / g[g.quality_group == 'Others'].iloc[0].users_above_11_500_cap_per_above11_users) -1
    )


    return g

def speed_ccp_cochange(commits_per_user_file):
    """
        Note that repo_file_quality_per_year uses bug hit ratio and not ccp.
        For change analysis it doesn't matter.
    :param repo_file_quality_per_year:
    :return:
    """
    key = 'repo_name'

    trep = get_valid_repos()
    trep = trep[['repo_name']]
    users_per_project = pd.read_csv(commits_per_user_file)
    users_per_project = users_per_project[users_per_project.year > 2014]
    per_year_df = pd.merge(users_per_project, trep, on='repo_name')

    per_year_df = per_year_df[['repo_name', 'year', 'corrective_commits_ratio', 'commits_per_above11_users']]
    per_year_df = per_year_df.dropna()

    cochange_analysis(per_year_df
                      , first_metric='corrective_commits_ratio'
                      , second_metric='commits_per_above11_users'
                      , first_the_higher_the_better=False
                      , second_the_higher_the_better=True
                      , first_sig_threshold=0.1
                      , second_sig_threshold=10
                      , key=key
                      )


def speed_ccp_cochange_by_var(commits_per_user_file
                           , fixed_variable
                           , fixed_values):
    """
        Note that repo_file_quality_per_year uses bug hit ratio and not ccp.
        For change analysis it doesn't matter.
    :param repo_file_quality_per_year:
    :return:
    """
    key = 'repo_name'
    control_variables = [fixed_variable]

    trep = get_valid_repos()
    users_per_project = pd.read_csv(commits_per_user_file)
    users_per_project = users_per_project[users_per_project.year > EARLIEST_ANALYZED_YEAR]
    per_year_df = pd.merge(users_per_project, trep, on='repo_name')


    cochange_analysis_by_value(per_year_df
                               , first_metric='corrective_commits_ratio'
                               , second_metric='commits_per_above11_users'
                               , first_the_higher_the_better=False
                               , second_the_higher_the_better=True
                               , first_sig_threshold=0.1
                               , second_sig_threshold=10
                               , fixed_variable=fixed_variable
                               , fixed_values=fixed_values
                               , key=key
                               , control_variables=control_variables
                               )


def quality_and_speed_over_years(commits_per_user_file):

    print("over the years ccp and speed change")
    trep = get_valid_repos()
    trep = trep[['repo_name']]
    users_per_project = pd.read_csv(commits_per_user_file)
    users_per_project = users_per_project[users_per_project.year > 2014]
    df = pd.merge(users_per_project, trep, on='repo_name')

    df = df[['repo_name', 'year', 'corrective_commits_ratio', 'commits_per_above11_users']]
    df = df.dropna()

    cur_df = df.copy()
    cur_df['prev_year'] = cur_df.year -1
    cur_df = cur_df.rename(columns={'year' : 'cur_year', 'corrective_commits_ratio' : 'cur_corrective_commits_ratio'
        , 'commits_per_above11_users'  : 'cur_commits_per_above11_users'})

    prev_df = df.copy()
    prev_df = prev_df.rename(columns={'year' : 'prev_year', 'corrective_commits_ratio' : 'prev_corrective_commits_ratio'
        , 'commits_per_above11_users'  : 'prev_commits_per_above11_users'})

    two_years = pd.merge(cur_df, prev_df, left_on=['repo_name', 'prev_year'], right_on=['repo_name', 'prev_year'])
    two_years['improved_ccp'] = two_years.cur_corrective_commits_ratio < two_years.prev_corrective_commits_ratio
    two_years['hurt_ccp'] = two_years.cur_corrective_commits_ratio > two_years.prev_corrective_commits_ratio
    two_years['improved_speed'] = two_years.cur_commits_per_above11_users > two_years.prev_commits_per_above11_users

    g = two_years.groupby(['improved_ccp', 'improved_speed'], as_index=False).agg({'repo_name': 'count'})
    print(g)

    cm = ConfusionMatrix(g_df=g
                             , classifier='improved_ccp'
                             , concept='improved_speed', count='repo_name')

    print(cm.summarize())
    print("speed & ccp improvement match", cm.accuracy())
    print("speed improvement given ccp improvement", cm.precision())
    print("ccp improvement given speed improvement", cm.tp()/(cm.fn() + cm.tp()))

    two_years['sig_improved_ccp'] = two_years.cur_corrective_commits_ratio < two_years.prev_corrective_commits_ratio - 0.1
    two_years['sig_improved_speed'] = two_years.cur_commits_per_above11_users > two_years.prev_commits_per_above11_users + 10

    g = two_years.groupby(['sig_improved_ccp', 'sig_improved_speed'], as_index=False).agg({'repo_name': 'count'})
    print(g)

    cm = ConfusionMatrix(g_df=g
                             , classifier='sig_improved_ccp'
                             , concept='sig_improved_speed', count='repo_name')
    print(cm.summarize())

    g = two_years.groupby(['sig_improved_ccp', 'improved_speed'], as_index=False).agg({'repo_name': 'count'})
    print(g)

    print(cm.summarize())
    print()
    print("speed & ccp improvement match", cm.accuracy())
    print("speed improvement given ccp improvement", cm.precision(), "lift", cm.precision_lift())
    print("ccp improvement given speed improvement",  cm.recall(), "lift", cm.recall()/cm.hit_rate() - 1)
    print()

    g = two_years.groupby(['sig_improved_speed', 'hurt_ccp'], as_index=False).agg({'repo_name': 'count'})
    cm = ConfusionMatrix(g_df=g
                             , classifier='sig_improved_speed'
                             , concept='hurt_ccp', count='repo_name')

    print(cm.summarize())
    print()
    print("ccp hurt given significant speed improvement", cm.precision(), "lift", cm.precision_lift())
    print()


def run_speed_consistency():
    quality_and_speed(commits_per_user_file=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv'))
    quality_and_speed_over_years(commits_per_user_file=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv'))
    return speed_consistency(commits_per_user_file=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv'))



if __name__ == '__main__':
    df = run_speed_consistency()
    speed_ccp_cochange(commits_per_user_file=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv'))

    speed_ccp_cochange_by_var(commits_per_user_file=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                              , fixed_variable='language'
                              , fixed_values=lang_name
                              )

    speed_ccp_cochange_by_var(commits_per_user_file=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                              , fixed_variable='dev_num_group'
                              , fixed_values=["few", "intermediate", "numerous"]
                              )

    speed_ccp_cochange_by_var(commits_per_user_file=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                              , fixed_variable='age_group'
                              , fixed_values=['old', 'medium', 'young']
                              )