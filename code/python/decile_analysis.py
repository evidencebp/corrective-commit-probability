from os.path import join
import pandas as pd


from configuration import DATA_PATH, NUMERIC_NULL, \
    TEST_SIZE, RANDOM_STATE, FIGURES_PATH, PERFORMANCE_PATH, MODELS_PATH, NON_PREDICTIVE_FEATURES, CONCEPT, DATASET

from plot_deciles import plot_deciles

def run_plots():
    df = pd.read_csv(join(DATA_PATH
                                          , DATASET))

    metric_column = 'ccp'

    grouping_column='tests_presence'
    fig = plot_deciles(df
                       , grouping_column
                       , metric_column
                       , title="{metric} by {group}".format(metric=metric_column
                                                            , group=grouping_column)
                       , xaxis_title="Deciles of {group}".format(group=grouping_column)
                       , output_file=None
                       , top_val=1.0)
    fig.show()

    groups = ['capped_sum_code_file_size',  'prev_touch_ago']
    for grouping_column in groups:
        fig = plot_deciles(df
                         , grouping_column
                         , metric_column
                         , title="{metric} by {group}".format(metric=metric_column
                                                              , group=grouping_column)
                         , xaxis_title="Deciles of {group}".format(group=grouping_column)
                         , output_file=None)
        fig.show()


    metric_column = 'authors'
    groups = ['capped_sum_code_file_size',  'prev_touch_ago']

    for grouping_column in groups:
        fig = plot_deciles(df
                         , grouping_column
                         , metric_column
                         , title="{metric} by {group}".format(metric=metric_column
                                                              , group=grouping_column)
                         , xaxis_title="Deciles of {group}".format(group=grouping_column)
                         , output_file=None)
        fig.show()


    metric_column = 'prev_touch_ago'
    groups = ['tests_presence',  'stars', 'authors']

    for grouping_column in groups:
        fig = plot_deciles(df
                         , grouping_column
                         , metric_column
                         , title="{metric} by {group}".format(metric=metric_column
                                                              , group=grouping_column)
                         , xaxis_title="Deciles of {group}".format(group=grouping_column)
                         , output_file=None)
        fig.show()


if __name__ == "__main__":
    run_plots()