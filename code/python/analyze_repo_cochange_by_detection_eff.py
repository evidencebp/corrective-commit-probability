from os.path import join
import pandas as pd

from configuration import DATA_PATH
from cochange_analysis import cochange_analysis, the_lower_the_better, the_higher_the_better, cochange_to_df\
    , cochange_analysis_by_value, cochange_by_value_to_df
from feature_pair_analysis import pair_analysis, pair_analysis_by_value


def cochange_by_detection():

    keys = ['repo_name']

    #repo_name,year,min_commit_time,max_commit_time,min_commit,max_commit,commits,non_merge_commits,corrective_commits
    # ,corrective_rate,ccp,refactor_mle,avg_coupling_size,avg_coupling_code_size,avg_coupling_size_capped
    # ,avg_coupling_code_size_capped,avg_coupling_size_cut,avg_coupling_code_size_cut,authors,Author_email
    # ,same_day_duration_avg,files_edited,files_created,files_created_ccp,tests_presence,multiline_message_ratio
    # ,message_length_avg,same_date_duration_avg,same_date_commits,commit_period,commit_days,commits_per_day
    # ,commit_weeks,commit_months,commit_days_of_week,commit_hours,commit_day_density,survival_avg,above_year_prob
    # ,commits_per_developer,involved_developers,involved_developers_commits,commits_per_involved_developer
    # ,developer_capped_commits,capped_commits_per_developer,involved_developers_capped_commits
    # ,capped_commits_per_involved_developer,stars,detection_efficiency,avg_file_size,capped_avg_file_size
    # ,avg_code_file_size,capped_avg_code_file_size

    metric_per_year_df = pd.read_csv(join(DATA_PATH
                                          , 'repo_properties_per_year.csv'))
    metrics_dict = {'ccp' : the_lower_the_better
                    , 'avg_coupling_size_capped': the_lower_the_better
                    , 'involved_developers_capped_commits': the_higher_the_better # TODO - check metric computation
                    , 'onboarding_prob': the_higher_the_better
                    , 'retention_prob': the_higher_the_better
                    , 'prev_touch_ago': the_lower_the_better
                    #, 'capped_avg_code_file_size': the_lower_the_better
                    }
    stats = cochange_analysis(metric_per_year_df
                                , metrics_dict
                                , keys
                                , control_variables=['detection_efficiency']
                                , min_cnt_column='commits'
                                , min_cnt_threshold=200
                              )
    print(stats)

    cochange_to_df(stats
                   , outputfile=join(DATA_PATH
                         , 'ccp_chochange_def_eff_control.csv')
                   , lead_column='metric')

    fixed_variable = 'detection_efficiency'
    grouped_stats = cochange_analysis_by_value(metric_per_year_df
                         , metrics_dict
                         , fixed_variable=fixed_variable
                         , fixed_values=None
                         , keys=keys
                         , control_variables=[]
                         )
    lead_column = 'metric'
    grouped_stats_df = cochange_by_value_to_df(grouped_stats
                            , fixed_variable
                            , outputfile=join(DATA_PATH
                            , 'ccp_chochange_by_def_eff.csv')
                            , lead_column=lead_column
                            )
    grouped_stats_df = grouped_stats_df.sort_values([lead_column, fixed_variable])
    print(grouped_stats_df)

def feture_pairs():
    concept = 'ccp'
    fixed_variable = 'detection_efficiency'
    metrics_dict = {'ccp' : the_lower_the_better
                    , 'avg_coupling_size_capped': the_lower_the_better
                    , 'involved_developers_capped_commits': the_higher_the_better # TODO - check metric computation
                    , 'capped_avg_code_file_size': the_lower_the_better
                    }

    df = pd.read_csv(join(DATA_PATH
                                          , 'repo_properties.csv'))
    for i in metrics_dict.keys():

        stats = pair_analysis(df
                       , first_metric=i
                       , second_metric=concept
                       , metrics=None)
        print(i)
        print(stats)
        stats = pair_analysis_by_value(df
                           , i
                           , concept
                           , fixed_variable=fixed_variable
                           , fixed_values=None
                           )
        print(i, "controled")
        print(stats)


if __name__ == '__main__':
    cochange_by_detection()
    feture_pairs()
