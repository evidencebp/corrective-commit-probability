from os.path import join

import json
import pandas as pd

from configuration import DATA_PATH
from df_to_latex_table import df_to_latex_table


def topics_st_to_set(json_str):
    HOLDER = '###HOLDER###'
    json_str = json_str.replace('"', HOLDER)
    json_str = json_str.replace("'", '"')
    json_str = json_str.replace(HOLDER, '"')
    json_str = json_str.replace("None", '""')
    json_str = json_str.replace("False", '"False"')
    json_str = json_str.replace("True", '"True"')
    return json.loads(json_str)


def topics_etl(df):

    records = []
    for _, i in df.iterrows():
        topics = topics_st_to_set(i['output'])
        for j in topics:
            records.append((i['repo_name'], j))

    topics_df = pd.DataFrame(records, columns=['repo_name', 'topic'])

    return topics_df

def bulid_topics_of_repos():
    df = pd.read_csv(join(DATA_PATH
                            , 'repos_2020_topics.csv'))

    topics_df = topics_etl(df)
    topics_df.to_csv(join(DATA_PATH
                            , 'topics_of_repos.csv')
                     , index=False)

def print_topics_table(topics_df):
    topcis_pop = topics_df.groupby(['topic'], as_index=False).agg({'repo_name' : 'count'})
    topics_pop = topcis_pop.sort_values('repo_name', ascending=False)

    topics_of_interest = ['hacktoberfest', 'android', 'linux', 'docker', 'kubernetes', 'machine-learning', 'windows', 'framework', 'security'
        , 'ios', 'database', 'cloud', 'library', 'deep-learning', 'blockchain', 'wordpress', 'bioinformatics', 'devops'
        , 'ui', 'editor', 'microservices', 'bot', 'raspberry-pi', 'minecraft', 'gui', 'audio', 'c-sharp', 'csharp'
        , 'cpp', 'c-plus-plus']

    """
    topics_pop = topics_pop[topics_pop.repo_name > 29]
    print(topics_pop)
    topics_of_interest = topics_pop.topic.unique()
    """

    repos_profile = pd.read_csv(join(DATA_PATH
                            , 'repo_properties.csv'))
    r = []
    for i in topics_of_interest:
        repos = topics_df[topics_df.topic == i].repo_name.unique()
        ccp = repos_profile[repos_profile.repo_name.isin(repos)].ccp.mean()
        r.append((i, ccp, len(repos)))

    repos_df = pd.DataFrame(r, columns=['topic', 'ccp', 'repositories'])
    repos_df = repos_df.sort_values('ccp', ascending=False)

    repos_df.to_csv(join(DATA_PATH
                            , 'topics_ccp.csv')
                     , index=False)

    df_to_latex_table(df=repos_df
                          , caption='\label{tab:topic-ccp} CCP by Topic'
                          )

    print("Number of topics", topics_df.topic.nunique())
    print("Number of labels", len(topics_df))
    print("Avg. Number of labels per repo", 1.0*len(topics_df)/len(repos_profile))

def run_topics():
    #bulid_topics_of_repos()
    topics_df = pd.read_csv(join(DATA_PATH
                            , 'topics_of_repos.csv'))
    print_topics_table(topics_df)


if __name__ == "__main__":
    run_topics()