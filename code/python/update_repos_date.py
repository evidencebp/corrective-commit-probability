import os
import pandas as pd

from configuration import DATA_PATH, REPOSITORIES_FILE
from repo_utils import compute_repo_ccp


def unify_date_format(date_str):
    if r"/"in date_str:
        # change 12/12/2018 to 2019-11-27
        day = date_str[0:date_str.find('/')]
        month = date_str[date_str.find('/') + 1:date_str.find('/', date_str.find('/') + 1)]
        year = date_str[date_str.find('/', date_str.find('/') + 1)+1:date_str.find('/', date_str.find('/') + 1)+5]
        # '%Y-%m-%d'
        new_date = year + '-' + month + '-' + day + date_str[date_str.find('/', date_str.find('/') + 1)+5:]
        return new_date
    else:
        return date_str


def update_repos_date(repos_file
                      , dates_file
                      , output_file):
    """
        The repo files is computed in a given date.
        In order to analyze the longlivety of the repos we might be interested in returning
        later and see which repositories are still active.
        In this case we excrate from big query new end dtate and update the repo file.
    :param repos_file:
    :param dates_file:
    :param output_file:
    :return:
    """
    #import pdb; pdb.set_trace()
    repo_df = pd.read_csv(repos_file)
    repo_df = repo_df.rename(columns= {'end_time' : 'prev_end_time'})

    dates_df = pd.read_csv(dates_file)
    dates_df = dates_df[['repo_name', 'end_time']]
    dates_df.columns = ['repo_name', 'updated_end_time']

    updated = pd.merge(repo_df, dates_df, on='repo_name', how='left')

    updated['ununified_end_time'] = updated.apply(
        lambda x: x.updated_end_time if  not pd.isnull(x.updated_end_time) else x.prev_end_time
        , axis=1)
    updated['end_time'] = updated.ununified_end_time.map(unify_date_format)
    updated = updated.drop(columns=['prev_end_time', 'updated_end_time', 'ununified_end_time'])
    updated.to_csv(output_file, index=False)


if __name__ == '__main__':

    output_file = os.path.join(DATA_PATH, 'repos_full_updated.csv')
    update_repos_date(os.path.join(DATA_PATH, REPOSITORIES_FILE)
                      , os.path.join(DATA_PATH, 'repositiory_start_end_dates.csv')
                      , output_file)
    compute_repo_ccp(output_file)

    """
    update_repos_date(os.path.join(DATA_PATH, 'prev_repos_full.csv')
                      , os.path.join(DATA_PATH, 'repositiory_start_end_dates.csv')
                      , os.path.join(DATA_PATH, 'repos_full_updated2.csv'))
    """
