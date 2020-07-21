import os
import pandas as pd

from configuration import DATA_PATH
from remove_redundant_repositories import remove_dominated_repositories, remove_redundency_by_name
from repo_utils import get_valid_repos


def analyze_longlivity_2017(repo_properties_file
                            , longlivity_file
                            , activity_file
                            , only_new=False):


    # Remove forks and invalid CCP
    repos = pd.read_csv(repo_properties_file)
    repos = repos[(repos.ccp > 0) & (repos.ccp < 1)]
    repos = repos[['repo_name', 'year', 'commits', 'authors',
       'hits', 'hit_ratio', 'ccp', 'fork']] # removing 'start_time', 'end_time'

    #repos = repos[repos.commits > 500] # TODO remove?
    activity_df = pd.read_csv(activity_file)
    repos = pd.merge(repos, activity_df, on='repo_name')

    longlivity = pd.read_csv(longlivity_file)


    df = pd.merge(repos, longlivity, on='repo_name', how='left')
    #df = df[(df.fork == False) & (df.y2018_ccp > 0) & (df.y2018_ccp < 1)]
    df = df.fillna(0)

    if only_new:
        df['start_year'] = df.start_time.map(lambda x: x[:4])
        df = df[df.start_year.isin( ['2017', '2016'])]

    #repos2019 =_get_valid_repos()
    q10 = df.ccp.quantile(0.1)
    #q10 = 0.06 # TODO - remove?
    df['quality_group'] = df.apply(lambda x: 'Others' if x.ccp > q10 else 'Top 10', axis=1)

    df['positive_days_from_2018_end'] = df.days_from_2018_end.map(lambda x: x if x > 0 else 0)
    df['after_2018_end'] = df.days_from_2018_end.map(lambda x: 1 if x > 0 else 0)
    df['positive_days_from_june'] = df.days_from_2019_june.map(lambda x: x if x > 0 else 0)
    df['after_june'] = df.days_from_2019_june.map(lambda x: 1 if x > 0 else 0)
    df['positive_days_from_2019_end'] = df.days_from_2019_end.map(lambda x: x if x > 0 else 0)
    df['after_2019_end'] = df.days_from_2019_end.map(lambda x: 1 if x > 0 else 0)

    g = df.groupby(['quality_group'], as_index=False).agg(
        {'repo_name': 'count'
            #, 'positive_days_from_2018_end': 'mean'
            , 'after_2018_end': 'mean'
            #, 'positive_days_from_june': 'mean'
            #, 'after_june': 'mean'
            #, 'positive_days_from_2019_end': 'mean'
            , 'after_2019_end': 'mean'
         })

    print(g)

    print("increase in probability of after 2018 prob")
    print((g[g.quality_group =='Top 10'].iloc[0].after_2018_end-g[g.quality_group =='Others'].iloc[0].after_2018_end)
          /g[g.quality_group =='Others'].iloc[0].after_2018_end)

    """
    print("increase in of after 2018 days")
    print((g[g.quality_group =='Top 10'].iloc[0].positive_days_from_2018_end
           -g[g.quality_group =='Others'].iloc[0].positive_days_from_2018_end)
          )

    print("increase in probability of after June 2019 prob")
    print((g[g.quality_group =='Top 10'].iloc[0].after_june-g[g.quality_group =='Others'].iloc[0].after_june)
          /g[g.quality_group =='Others'].iloc[0].after_june)

    print("increase in of after June 2019 days")
    print((g[g.quality_group =='Top 10'].iloc[0].positive_days_from_june
           -g[g.quality_group =='Others'].iloc[0].positive_days_from_june)
          )
    """

    print("increase in probability of after 2019 prob")
    print((g[g.quality_group =='Top 10'].iloc[0].after_2019_end-g[g.quality_group =='Others'].iloc[0].after_2019_end)
          /g[g.quality_group =='Others'].iloc[0].after_2019_end)

    """
    print("increase in of after 2019 days")
    print((g[g.quality_group =='Top 10'].iloc[0].positive_days_from_2019_end
           -g[g.quality_group =='Others'].iloc[0].positive_days_from_2019_end)
          )
    """
    return df

def run_analyze_longlivity_2017():
    repo_properties_file =os.path.join(DATA_PATH, 'not_redundant_repos_2017.csv')
    longlivity_file =os.path.join(DATA_PATH, 'longevity_2017.csv')
    activity_file = os.path.join(DATA_PATH, 'active_2017_200.csv')

    print("Analyze new 2017 projects")
    analyze_longlivity_2017(repo_properties_file=repo_properties_file
                                , longlivity_file=longlivity_file
                                , activity_file=activity_file
                                , only_new=True)


    print("Analyze all 2017 projects")
    df = analyze_longlivity_2017(repo_properties_file=repo_properties_file
                                , longlivity_file=longlivity_file
                                , activity_file=activity_file
                                , only_new=False)


    return df


def remove_redundant_repos(repositories_file
                           , repo_fork_file
                           , dominated_file
                           , not_redundant_file):

    import pdb; pdb.set_trace()
    not_dominated = remove_dominated_repositories(dominated_file
                               , repositories_file
                               , output_file=None)

    not_forks = pd.read_csv(repo_fork_file)
    not_forks = pd.merge(not_dominated, not_forks, on='repo_name')
    not_forks = not_forks[not_forks.fork ==  False]

    not_redundant = remove_redundency_by_name(not_forks)
    if not_redundant_file is not None:
        not_redundant.to_csv(not_redundant_file, index=False)

    return not_redundant

def run_remove_redundant_forks():

    repositories_file =os.path.join(DATA_PATH, 'repos_properties_2017.csv')
    repo_fork_file =os.path.join(DATA_PATH, 'repos_2017_fork.csv')
    dominated_file =os.path.join(DATA_PATH, 'dominated_repos_2017.csv')
    not_redundant_file =os.path.join(DATA_PATH, 'not_redundant_repos_2017.csv')

    return remove_redundant_repos(repositories_file
                           , repo_fork_file
                           , dominated_file
                           , not_redundant_file)

if __name__ == '__main__':
    df = run_analyze_longlivity_2017()
    #df = run_remove_redundant_forks()