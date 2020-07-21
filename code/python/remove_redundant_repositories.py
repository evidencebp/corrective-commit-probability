import os
import pandas as pd

from configuration import DATA_PATH


def remove_dominated_repositories(dominated_file
                                   , repositories_file
                                   , output_file):
    dominated = pd.read_csv(dominated_file)
    repos = pd.read_csv(repositories_file)

    repos = repos[~repos.repo_name.isin(dominated.repo_name.to_list())]

    if output_file is not None:
        repos.to_csv(output_file, index=False)

    return repos

def remove_redundency_by_name(df):
    df['user'] = df.repo_name.map(lambda x: x.split('/')[0])
    df['project'] = df.repo_name.map(lambda x: x.split('/')[1])

    users = df.groupby(['user'], as_index=False).agg({'repo_name': 'nunique'})
    users = users.rename(columns={'repo_name' : 'repos_per_user' })
    joint = pd.merge(df, users, on='user')
    joint = joint[['repo_name', 'user', 'project', 'repos_per_user']]

    dominating = joint

    dominating = dominating.rename(columns={'repo_name' : 'dominating_repo_name'
                                       , 'user' : 'dominating_user'
                                       , 'repos_per_user' : 'dominating_repos_per_user'})
    dominated = joint
    dominated = dominated.rename(columns={'repo_name' : 'dominated_repo_name'
                                       , 'user' : 'dominated_user'
                                       , 'repos_per_user' : 'dominated_repos_per_user'})

    domination = pd.merge(dominating, dominated, on='project')

    domination = domination[((domination.dominating_repos_per_user > domination.dominated_repos_per_user) &
                             (domination.dominating_repo_name != domination.dominated_repo_name))
                            | ((domination.dominating_repos_per_user == domination.dominated_repos_per_user) &
                               (domination.dominating_repo_name > domination.dominated_repo_name))]
    dominated_repos = domination.dominated_repo_name.unique()

    df = df[~df.repo_name.isin(dominated_repos)]

    return df

def check_name_redundency(df):
    df['user'] = df.repo_name.map(lambda x: x.split('/')[0])
    df['project'] = df.repo_name.map(lambda x: x.split('/')[1])

    g_project = df[df.fork == False].groupby(['project'], as_index=False).agg({'repo_name': 'nunique'})

    print("duplicated project names")
    print(g_project[g_project.repo_name > 1])

    return df

def run_remove_redundency():
    df = remove_dominated_repositories(os.path.join(DATA_PATH, "dominated_repos.csv")
                                    , os.path.join(DATA_PATH, "active_2019_atleast_200_gitprop.csv")
                                    , os.path.join(DATA_PATH, "active_2019_atleast_200_gitprop_no_dominante.csv"))
    df = remove_redundency_by_name(df)
    df.to_csv(os.path.join(DATA_PATH, "repos_2019.csv"), index=False)

if __name__ == '__main__':
    run_remove_redundency()