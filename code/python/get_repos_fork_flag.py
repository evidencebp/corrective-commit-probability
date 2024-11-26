"""
 curl -H "Accept: application/vnd.github.mercy-preview+json" https://api.github.com/repos/dipakkr/A-to-Z-Resources-for-Students/topics
{
  "names": [
    "hackathon",
    "students",
    "android",
    "conferences",
    "react",
    "udacity",
    "awesome-list",
    "awesome"
  ]
}
"""

from os.path import join
from github import Github
import pandas as pd
from time import sleep

from cred import GITHUB_TOKEN
from configuration import DATA_PATH
from batch_process import BatchProcessor
from analyze_topics import topics_st_to_set


def get_repo_fork_flag(repo_name
                    , git_interface):
    #pdb.set_trace()
    r = git_interface.get_repo(repo_name)
    return r.fork


git_interface = Github(GITHUB_TOKEN)


def get_fork_flag_of_repo(repo):

    return get_repo_fork_flag(repo['repo_name']
                    , git_interface)

def extract_repo_properties_wrapper(repo):
    return extract_repo_properties(repo['repo_name']
                    , git_interface)

def extract_repo_properties(repo
                            , git_interface):
    """
    Extract repository properties.

    Note that a repository's propeties might not be found due to
    few cases:
    - Reporitory was deleted
    - Repository was renamed
    - Repository was turn private
    - Qouta was used
    - A temporal error in the API

    Due to the last two reasons it is recommended to run the script more
    than once.

    :param repo:
    :return:
    """
    properties = {}

    r = git_interface.get_repo(repo)

    #import pdb; pdb.set_trace()
    properties['forks_count'] = r.forks_count
    properties['language'] = r.language
    properties['network_count'] = r.network_count
    properties['open_issues_count'] = r.open_issues_count
    properties['stargazers_count'] = r.stargazers_count
    properties['subscribers_count'] = r.subscribers_count
    properties['watchers_count'] = r.watchers_count
    # properties['fork'] = r.fork

    return properties


#import pdb; pdb.set_trace()
pause_function = lambda: sleep(10)

def pause_for_quota(min_quota=1000
                    , sleep_duration=60*5):
    while git_interface.get_rate_limit().core.remaining < min_quota:
        sleep(sleep_duration)


def properties_etl(df):

    records = []
    for _, i in df.iterrows():
        try:
            properties = topics_st_to_set(i['output'])
            records.append((i.repo_name
                            , properties['language']
                            , properties['forks_count']
                            , properties['network_count']
                            , properties['open_issues_count']
                            , properties['stargazers_count']
                            , properties['subscribers_count']
                            , properties['watchers_count']
                            ))
        except:
            print("error processing ", i)

    res_df = pd.DataFrame(records, columns=['repo_name', 'language', 'forks_count', 'network_count'
        , 'open_issues_count', 'stargazers_count', 'subscribers_count', 'watchers_count'])

    return res_df

def get_repositories():
    """
    bp_fork = BatchProcessor(input_file=join('/Users/idan/Downloads'
                                    , '2020_above_50_10_jan.csv')
                    , output_file=join(DATA_PATH
                                    , '2020_above_50_fork_10_jan.csv')
                    , prev_file=None
                    #, prev_file=join(DATA_PATH
                    #                , '2020_above_50_nofork.csv')
                    , fetch_function=get_fork_flag_of_repo
                    , keys=['repo_name']
                    , error_file=join(DATA_PATH
                                    , '2020_above_50_errors.csv')
                    , pause_function=pause_for_quota
                    )
    bp_fork.process()

    """
    bp_properties = BatchProcessor(input_file=
                                'C:/src/pylint-intervention/interventions/candidates_detailed_stats_with_recent.csv'
                        , output_file='C:/src/pylint-intervention/interventions/candidates_detailed_stats_prop.csv'

                        , prev_file=None
                        #, prev_file=join(DATA_PATH
                        #                , '2020_above_50_nofork_properties_v3.csv')
                        , fetch_function=extract_repo_properties_wrapper
                        , keys=['repo_name']
                        , error_file='c:/tmp/errors.csv'
                        , pause_function=pause_for_quota
                        )
    bp_properties.process()


def structure_properties_file():
    df = pd.read_csv('C:/src/pylint-intervention/interventions/candidates_detailed_stats_prop.csv')
    structured_df = properties_etl(df)
    structured_df.to_csv('C:/src/pylint-intervention/interventions/candidates_detailed_stats_stars.csv'
                         , index=False)
if __name__ == "__main__":
    #get_repositories()
    structure_properties_file()