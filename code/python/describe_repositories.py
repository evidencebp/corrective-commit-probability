import os
import pandas as pd

from configuration import DATA_PATH, REPOSITORIES_FILE
from repo_utils import get_valid_repos, get_non_fork_repos

def describe_repos(repos_file
                   , bq_propeties_file
                   , git_propeties_file):

    print("################## Describing repositories ##################")
    df = pd.read_csv(bq_propeties_file)
    df = df[df.commit2019 > 199]
    print("Large active repositories"
          ,  '{:,}'.format(df.repo_name.nunique()))

    git_repos = pd.read_csv(git_propeties_file)
    git_repos = pd.merge(git_repos, df, on='repo_name')

    print("BQ Large non fork repositories"
          ,'{:,}'.format(git_repos[~git_repos.fork].repo_name.nunique()))

    repos  = pd.read_csv(repos_file)
    print("Large no reduendent repositories"
          ,'{:,}'.format(repos[~repos.fork].repo_name.nunique()))

    trep = get_valid_repos()
    print("Valid non reduendent repositories"
          , '{:,}'.format( trep.repo_name.nunique()))

def run_describe_repos():
    describe_repos(repos_file=os.path.join(DATA_PATH, REPOSITORIES_FILE)
                   , bq_propeties_file=os.path.join(DATA_PATH,"active_atleast_100_2019.csv")
                   , git_propeties_file=os.path.join(DATA_PATH,"active_2019_atleast_100_gitprop.csv"))

if __name__ == '__main__':
    run_describe_repos()