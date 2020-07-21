
import os
import pandas as pd

from analysis_configuration import  GITHUB_START_YEAR
from configuration import DATA_PATH, REPOSITORIES_FILE, REPOSITORIES_PROPERTIES, REPOSITORIES_GIT_PROPERTIES\
    , ANALYZED_YEAR
from positives_mle import ccp_estimator


def compute_repo_ccp(repo_file):
    rep = pd.read_csv(repo_file)

    rep['y2016_hit_rate'] = 1.0 * rep.y2016_hits / rep.y2016_commits
    rep['y2017_hit_rate'] = 1.0 * rep.y2017_hits / rep.y2017_commits
    rep['y2018_hit_rate'] = 1.0 * rep.y2018_hits / rep.y2018_commits
    rep['y2019_hit_rate'] = 1.0 * rep.y2019_hits / rep.y2019_commits

    rep['y2016_ccp'] = rep.y2016_hit_rate.map(lambda x: ccp_estimator.estimate_positives(x))
    rep['y2017_ccp'] = rep.y2017_hit_rate.map(lambda x: ccp_estimator.estimate_positives(x))
    rep['y2018_ccp'] = rep.y2018_hit_rate.map(lambda x: ccp_estimator.estimate_positives(x))
    rep['y2019_ccp'] = rep.y2019_hit_rate.map(lambda x: ccp_estimator.estimate_positives(x))
    rep['y2019_hit_rate_rnd'] = rep.y2019_hit_rate.map(lambda x: round(x, 2))

    # extract to repo utils
    trep = rep[rep.fork == False]
    trep = trep[trep.y2019_hit_rate.map(lambda x: ccp_estimator.is_in_range(x))]
    trep = trep.sort_values(['y2019_hit_rate'], ascending=False)
    y2019_hit_rate_10p = trep.iloc[int(90 * len(trep) / 100)].y2019_hit_rate

    rep['quality_group'] = rep.apply(lambda x: 'Others'
            if x.y2019_hit_rate > y2019_hit_rate_10p else 'Top 10', axis=1)

    rep['dev_num_group'] = pd.cut(rep.authors, [0
        , rep.authors.quantile(0.25)
        , rep.authors.quantile(0.75), float("inf")],
                                 labels=["few", "intermediate", "numerous"])

    rep['start_year'] = rep.start_time.map(lambda x: int(x[:4]))
    rep['age'] = ANALYZED_YEAR - rep.start_year

    rep['age_group'] = pd.cut(rep.start_year, [0
        , GITHUB_START_YEAR - 1
        , rep[rep.start_year >= GITHUB_START_YEAR].start_year.quantile(0.25)
        , rep[rep.start_year >= GITHUB_START_YEAR].start_year.quantile(0.75)
        , float("inf")], labels=['prehistory', "old", "medium", "young"])

    rep['y2019_ccp_in_valid_range'] = rep.y2019_hit_rate.map(lambda x: ccp_estimator.is_in_range(x))

    # Updating the file with the CCP values
    rep.to_csv(repo_file
               , index=False)

    return rep

def get_non_fork_repos():
    """
        Returns a data frame of all projects that are not forks and whose CCP is in the valid range
    :return:
    """
    repo_file = os.path.join(DATA_PATH, REPOSITORIES_FILE)
    rep = pd.read_csv(repo_file)
    trep = rep[rep.fork == False]

    return trep


def get_valid_repos():
    """
        Returns a data frame of all projects that are not forks and whose CCP is in the valid range
    :return:
    """
    rep = get_non_fork_repos()
    rep = rep[rep.y2019_hit_rate.map(lambda x: ccp_estimator.is_in_range(x))]

    return rep

def merge_git_and_bq_properties(git_file
                                 , bq_file
                                 , output_file):
    git_df = pd.read_csv(git_file)
    bq_df = pd.read_csv(bq_file)

    joint = pd.merge(git_df, bq_df, on='repo_name')
    joint.to_csv(output_file, index=False)

    return joint

def age_group_dist(repo_file):
    rep = pd.read_csv(repo_file)

    rep['start_year'] = rep.start_time.map(lambda x: int(x[:4]))
    rep['age'] = GITHUB_START_YEAR - rep.start_year

    rep['age_group'] = pd.cut(rep.start_year, [0
        , GITHUB_START_YEAR - 1
        , rep[rep.start_year >= GITHUB_START_YEAR].start_year.quantile(0.25)
        , rep[rep.start_year >= GITHUB_START_YEAR].start_year.quantile(0.75)
        , float("inf")])
    g = rep.groupby('age_group').agg({'repo_name' : 'count'})
    n = len(rep)
    valid = len(rep[rep['start_year'] >= GITHUB_START_YEAR])
    g['prob'] = g['repo_name']/n
    g['valid_prob'] = g['repo_name'] / valid
    print(g)


def run_build_repo():
    merge_git_and_bq_properties(git_file=os.path.join(DATA_PATH, REPOSITORIES_PROPERTIES)
                                , bq_file=os.path.join(DATA_PATH, REPOSITORIES_GIT_PROPERTIES)
                                , output_file=os.path.join(DATA_PATH, REPOSITORIES_FILE))
    return compute_repo_ccp(os.path.join(DATA_PATH, REPOSITORIES_FILE))
if __name__ == '__main__':
    df = run_build_repo()
    age_group_dist(repo_file=os.path.join(DATA_PATH, REPOSITORIES_FILE))