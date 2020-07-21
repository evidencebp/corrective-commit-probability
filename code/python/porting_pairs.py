import os
import pandas as pd
import re


from analysis_configuration import lang_name
from configuration import DATA_PATH
from repo_utils import get_valid_repos

def build_porting_pairs():
    df = get_valid_repos()
    df['user'] = df.repo_name.map(lambda x: x.split('/')[0])
    df['project'] = df.repo_name.map(lambda x: x.split('/')[1])

    lang =  lang_name+ [i.lower() for i in  lang_name]
    lang = [re.escape(i) for i in lang]
    lang_in_name =df[df.project.str.contains('|'.join(lang))]
    lang_in_name_by_user = lang_in_name.groupby(['user'], as_index=False).agg({'repo_name' : 'count'})
    p = lang_in_name[ lang_in_name.user.isin(
        lang_in_name_by_user[lang_in_name_by_user.repo_name > 1].user.tolist())
        ].sort_values('user')[['repo_name', 'user', 'project', 'language']]
    p.to_csv(os.path.join(DATA_PATH, 'porting_pairs.csv'), index=False)

def analyze_porting_pairs():
    # After manual editing and selecting only suitable pairs
    df = get_valid_repos()
    df['user'] = df.repo_name.map(lambda x: x.split('/')[0])
    df['project'] = df.repo_name.map(lambda x: x.split('/')[1])

    p = pd.read_csv(os.path.join(DATA_PATH, 'porting_pairs.csv'))
    j = pd.merge(p, df[['repo_name', 'y2019_ccp']], on='repo_name')

    pairs = pd.merge(j, j, on='user')
    pairs = pairs[(pairs.project_x != pairs.project_y)]
    pairs['y_ccp_by_x'] = 1.0*pairs.y2019_ccp_y / pairs.y2019_ccp_x

    g = pairs.groupby(['language_x', 'language_y']).agg({'project_x': 'count'
                                                         , 'y_ccp_by_x': {'mean', 'std'}})
    print(g)
    pairs.to_csv(os.path.join(DATA_PATH, 'porting_pairs_ccp.csv'), index=False)


if __name__ == '__main__':
    analyze_porting_pairs()