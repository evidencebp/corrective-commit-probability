from github import Github
import os
import pandas as pd
from time import sleep

from configuration import DATA_PATH, GITHUB_USER, GITHUB_PASSWORD

git_interface = Github(GITHUB_USER, GITHUB_PASSWORD)



def extract_projects_properties_quota(projects_list
                                     , properties_file
                                     , git_interface
                                      , just_fork=False):
    """
        Extract repositories properties and mange quota
    :param projects_list:
    :param properties_file:
    :param git_interface:
    :return:
    """

    # Git quota is 5000 but we do 7 calls
    QUOTA_BATCH = 10
    all_df = None

    for i in range(int(len(projects_list) /QUOTA_BATCH)):
         print ("processing batch " + str(i))
         df = extract_projects_properties(projects_list[i: i+QUOTA_BATCH]
                                        , properties_file
                                        , git_interface
                                        , just_fork)
         all_df = pd.concat([all_df, df])
         while git_interface.get_rate_limit().core.remaining < QUOTA_BATCH:
            print ("sleeping")
            sleep(10)

    all_df.to_csv(properties_file + "all")
    return all_df

def extract_projects_properties(projects_list
                                    , properties_file
                                    , git_interface
                                    , just_fork=False):
    """
        Extract reopsitories properties
    :param projects_list:
    :param properties_file:
    :param git_interface:
    :return:
    """

    BATCH_SIZE = 10

    properties_list = []
    current_item = 0

    for project in projects_list:
        current_item += 1
        if current_item % BATCH_SIZE == 0:
            print ("proccesing item # " + str(current_item))
        try:
            repo = git_interface.get_repo(project)
            properties_dict  =  extract_repo_properties(repo
                                                        , just_fork)
            properties_dict['repo_name'] = project
            properties_list.append(properties_dict)

        except:
            print ("error parsing " + project)

    df = pd.DataFrame(properties_list)

    df.to_csv(properties_file, index=False)



    return df



def extract_repo_properties(repo
                            , just_forks=False):
    """
    Extract repository properties
    :param repo:
    :return:
    """
    properties = {}

    properties['fork'] = repo.fork
    if not just_forks:

        try:
            properties['contributors_count'] = len([ i for i in repo.get_contributors()])
        except:
            print ("error reading contributors list")

        properties['language'] = repo.language
        properties['network_count'] = repo.network_count
        properties['open_issues_count']  = repo.open_issues_count
        properties['stargazers_count']  = repo.stargazers_count
        properties['subscribers_count'] = repo.subscribers_count
        properties['watchers_count'] = repo.watchers_count


    return properties

def find_repos_to_query(all_repos_file
                         , queried_repositories_file):
    all_repos_df = pd.read_csv(all_repos_file)
    queried_repositories_df = pd.read_csv(queried_repositories_file)
    queried_repos = queried_repositories_df.repo_name.tolist()
    new = all_repos_df[~all_repos_df.repo_name.isin(queried_repos)].repo_name.tolist()

    return new

def extract_repos_properties(repos_file
                             , properties_file):
    df = pd.read_csv(repos_file)
    projects_list = df.repo_name.tolist()
    extract_projects_properties_quota(projects_list
                                      , properties_file
                                      , git_interface)


"""
extract_repos_properties(repos_file=os.path.join(DATA_PATH
                                                 , 'active_2019_by_dec_200.csv')
                         , properties_file=r"c:/tmp/active_2019_by_dec_200_fork_v3.csv")
"""