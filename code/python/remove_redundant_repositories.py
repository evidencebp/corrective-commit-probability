from os.path import join
import pandas as pd

from configuration import DATA_PATH



def remove_redundency_by_name(df):
    df['user'] = df.repo_name.map(lambda x: x.split('/')[0])
    df['project'] = df.repo_name.map(lambda x: x.split('/')[1])

    users = df.groupby(['user'], as_index=False).agg({'repo_name': 'nunique'})
    users = users.rename(columns={'repo_name': 'repos_per_user' })
    joint = pd.merge(df, users, on='user')
    joint = joint[['repo_name', 'user', 'project', 'repos_per_user', 'stargazers_count']]

    dominating = joint

    dominating = dominating.rename(columns={'repo_name': 'dominating_repo_name'
                                       , 'user': 'dominating_user'
                                       , 'repos_per_user': 'dominating_repos_per_user'
                                       , 'stargazers_count': 'dominating_stargazers_count'})
    dominated = joint
    dominated = dominated.rename(columns={'repo_name' :'dominated_repo_name'
                                       , 'user': 'dominated_user'
                                       , 'repos_per_user': 'dominated_repos_per_user'
                                       , 'stargazers_count': 'dominated_stargazers_count'})

    domination = pd.merge(dominating, dominated, on='project')

    # Remove projects with the same name yet less stars (to filter people copying projects)
    domination = domination[((domination.dominating_stargazers_count > domination.dominated_stargazers_count) &
                             (domination.dominating_repo_name != domination.dominated_repo_name))]
    dominated_repos = domination.dominated_repo_name.unique()

    df = df[~df.repo_name.isin(dominated_repos)]

    # Removing projects of the user with less projects
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

    g_project = df.groupby(['project'], as_index=False).agg({'repo_name': 'nunique'})

    print("duplicated project names")
    print(g_project[g_project.repo_name > 1])

    return df

def run_remove_redundency():
    df = pd.read_csv(join(DATA_PATH, '2020_above_50_10_jan_no_dominated.csv'))
    check_name_redundency(df)
    df = remove_redundency_by_name(df)
    print("Number of repositories ", len(df))
    df.to_csv(join(DATA_PATH, "repos_2020.csv"), index=False)

if __name__ == '__main__':
    run_remove_redundency()