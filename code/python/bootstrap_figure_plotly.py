"""
Creating bootstrap figure
"""
import datetime
import os
from pandas import DataFrame
import pandas as pd
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import plotly.io as pio

from configuration import DATA_PATH, FIGURES_PATH, LANG_DATA_PATH
from confusion_matrix import ConfusionMatrix
from positives_mle import PositivesMLE

classifier = 'corrective_pred'
concept = 'Is_Corrective'
count = 'commit'
rounds = 10000


def build_differences(labels_file
                      , output_file):

    # Get confusion matrix on all data set
    df = pd.read_csv(labels_file
                        , engine = 'python')
    # In case that some sampling methods are used,
    bug_g = df.groupby([classifier, concept], as_index=False).agg({count: 'count'})
    bug_cm = ConfusionMatrix(g_df=bug_g
                             , classifier=classifier
                             , concept=concept, count=count)

    recall = bug_cm.recall()
    fpr = bug_cm.fpr()
    all_ccp_estimator = PositivesMLE(recall=recall
                                 , fpr=fpr)

    # Use boootstrap to comput CCP and positive rate difference
    results_df =  bootstrap_diff(df
                   , all_ccp_estimator
                   , rounds
                   , len(df))
    results_df.to_csv(output_file, index=False)

    return results_df

def bootstrap_diff(df
                    , ccp_estimator
                    , rounds
                    , sample_size):
    bootstrap_results = []
    for i in range(rounds):
        # Get first model parameters
        s1 = df.sample(sample_size, replace=True)
        bug_g = s1.groupby([classifier, concept], as_index=False).agg({count: 'count'})
        bug_cm = ConfusionMatrix(g_df=bug_g
                                 , classifier=classifier
                                 , concept=concept, count=count)

        positive_rate = bug_cm.positive_rate()
        hit_rate = bug_cm.hit_rate()
        ccp = ccp_estimator.estimate_positives(hit_rate)
        ccp_diff = ccp - positive_rate


        # Find difference in given points
        bootstrap_results.append([positive_rate
                                  , hit_rate
                                  , ccp
                                  , ccp_diff])

        if (i %  100 == 0):
            print( "finished " + str(i) , datetime.datetime.now())

    results_df = pd.DataFrame(bootstrap_results
                                , columns = ['positive_rate'
                                  , 'hit_rate'
                                  , 'ccp'
                                  , 'ccp_diff'])
    return results_df


def plot_bootstrap_figure(bootstrap_df
                          , image_file):

    bootstrap_df['rccp_diff'] = bootstrap_df.ccp_diff.map(lambda x : round(x,2))
    g = bootstrap_df.groupby(['rccp_diff'], as_index=False).agg({'positive_rate' : 'count'})
    g = g.rename(columns={'positive_rate' : 'rounds'})
    g['rccp_prob'] = g.rounds.map(lambda x: 1.0*x/rounds)


    cdf = bootstrap_df.ccp_diff.value_counts(normalize=True).sort_index().cumsum()
    cdf = DataFrame(cdf)
    cdf = cdf.reset_index()
    cdf.columns = ['ccp_diff', 'agg_prob']

    trace0 = go.Scatter(
        x = g.rccp_diff,
        y = g.rccp_prob,
        mode = 'lines',
        name = 'PDF'
    )
    trace1 = go.Scatter(
        x = cdf.ccp_diff,
        y = cdf.agg_prob,
        mode = 'lines',
        name = 'CDF'
    )

    data = [trace0, trace1]
    layout = go.Layout(
        title='CPP MLE vs. positive rate',
        xaxis=dict(
            title='CPP Estimation Minus True Fix Rate',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Probability',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)

    plot(fig,
        image = 'png', image_filename=image_file,
                 output_type='file'
        , image_width=400, image_height=400)
    fig.show()

def bootstrap_bounds(bootstrap_df):
    print(":bootstrap 0.025 quantile", bootstrap_df.ccp_diff.quantile(0.025))
    print(":bootstrap 0.975 quantile", bootstrap_df.ccp_diff.quantile(0.975))

def run_bootstrap_figure():
    #bootstrap_df = build_differences(os.path.join(LANG_DATA_PATH, 'model_validation_samples.csv')
    #    , os.path.join(DATA_PATH, 'bootstrap_diff.csv'))
    bootstrap_df= pd.read_csv(os.path.join(DATA_PATH, 'bootstrap_diff.csv'))
    plot_bootstrap_figure(bootstrap_df
                          , os.path.join(FIGURES_PATH, 'cpp_diff_figure'))
    bootstrap_bounds(bootstrap_df)


if __name__ == '__main__':
    run_bootstrap_figure()
