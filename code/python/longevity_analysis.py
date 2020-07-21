import os
import pandas as pd

from analysis_configuration import EARLIEST_ANALYZED_YEAR
from configuration import DATA_PATH, ANALYZED_YEAR
from feature_pair_analysis import pretty_print, pair_analysis_with_controls, pair_analysis_by_language\
    , pair_analysis_by_dev_num_group
from repo_utils import get_valid_repos

def analyze_longevity(repo_properties_file
                       , longlivity_file
                       , only_new=False):

    # Remove forks and invalid CCP
    repos = pd.read_csv(repo_properties_file)
    longlivity = pd.read_csv(longlivity_file)

    df = pd.merge(repos, longlivity, on='repo_name', how='left')
    df = df[(df.fork == False) & (df.y2018_ccp > 0) & (df.y2018_ccp < 1)]
    df.fillna(0)

    df['start_year'] = df.start_time.map(lambda x: int(x[6:10]))
    df['age'] = ANALYZED_YEAR - df.start_year

    df['age_group'] = pd.cut(df.start_year, [0
        , EARLIEST_ANALYZED_YEAR - 1
        , df[df.start_year >= EARLIEST_ANALYZED_YEAR].start_year.quantile(0.25)
        , df[df.start_year >= EARLIEST_ANALYZED_YEAR].start_year.quantile(0.75)
        , float("inf")], labels=['prehistory', "old", "medium", "young"])

    df['dev_num_group'] = pd.cut(df.commiters, [0
        , df.commiters.quantile(0.25)
        , df.commiters.quantile(0.75), float("inf")],
                                 labels=['few', 'intermediate', 'numerous'])

    if only_new:
        df = df[df.start_year.isin( ['2017', '2018'])]




    q10 = df.y2018_ccp.quantile(0.1)
    df['quality_group'] = df.apply(lambda x: 'Others' if x.y2018_ccp > q10 else 'Top 10', axis=1)

    df['positive_days_from_2018_end'] = df.days_from_2018_end.map(lambda x: x if x > 0 else 0)
    df['after_2018_end'] = df.days_from_2018_end.map(lambda x: 1 if x > 0 else 0)
    df['positive_days_from_june'] = df.days_from_2019_june.map(lambda x: x if x > 0 else 0)
    df['after_june'] = df.days_from_2019_june.map(lambda x: 1 if x > 0 else 0)
    df['positive_days_from_2019_end'] = df.days_from_2019_end.map(lambda x: x if x > 0 else 0)
    df['after_2019_end'] = df.days_from_2019_end.map(lambda x: 1 if x > 0 else 0)

    g = df.groupby(['quality_group'], as_index=False).agg(
        {'repo_name': 'count'
            , 'positive_days_from_2018_end': 'mean'
            , 'after_2018_end': 'mean'
            , 'positive_days_from_june': 'mean'
            , 'after_june': 'mean'
            , 'positive_days_from_2019_end': 'mean'
            , 'after_2019_end': 'mean'
         })

    print(g)

    print("increase in probability of after 2018 prob")
    print((g[g.quality_group =='Top 10'].iloc[0].after_2018_end-g[g.quality_group =='Others'].iloc[0].after_2018_end)
          /g[g.quality_group =='Others'].iloc[0].after_2018_end)

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


    print("increase in probability of after 2019 prob")
    print((g[g.quality_group =='Top 10'].iloc[0].after_2019_end-g[g.quality_group =='Others'].iloc[0].after_2019_end)
          /g[g.quality_group =='Others'].iloc[0].after_2019_end)

    print("increase in of after 2019 days")
    print((g[g.quality_group =='Top 10'].iloc[0].positive_days_from_2019_end
           -g[g.quality_group =='Others'].iloc[0].positive_days_from_2019_end)
          )

    if only_new:
        pretty_print(pair_analysis_by_dev_num_group(df
                                                    , 'quality_group'
                                                    , 'after_2019_end'
                                                    ))
        pretty_print(pair_analysis_by_language(df
                                           , 'quality_group'
                                           , 'after_2019_end'
                                           ))
    else:

        pretty_print(pair_analysis_with_controls(df
                  , 'quality_group'
                  , 'after_2019_end'
                  , metrics=None))


    return df

def run_analyze_longevity():

     analyze_longevity(repo_properties_file=os.path.join(DATA_PATH, 'repos_full_2018.csv')
                       , longlivity_file=os.path.join(DATA_PATH, 'longevity_2018.csv')
                        , only_new=True)

     return analyze_longevity(repo_properties_file=os.path.join(DATA_PATH, 'repos_full_2018.csv')
                       , longlivity_file=os.path.join(DATA_PATH, 'longevity_2018.csv'))

if __name__ == '__main__':
    df = run_analyze_longevity()
