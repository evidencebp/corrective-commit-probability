"""
File length per langauge generation
"""

import os
from math import sqrt
import pandas as pd


from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import plotly.io as pio

from analysis_configuration import  DOMINANT_RATE, lang_name, lang_extension, language_extensions
from configuration import DATA_PATH, FIGURES_PATH
from repo_utils import get_valid_repos

def length_per_lang_figure(major_extensions_file
                               , image_file):

    ext = pd.read_csv(major_extensions_file)
    dominant = ext[ext.major_extension_ratio > DOMINANT_RATE]
    trep = get_valid_repos()


    main = pd.merge(trep, dominant, on='repo_name')

    agg = main.groupby(['major_extension', 'quality_group']
                 , as_index=False).agg(
                {'major_capped_avg_file' : {'mean', 'std'}
                 , 'repo_name' : 'count'})

    agg.columns = [u'langauge', u'quality_group', u'size_std', u'size_mean', u'projects']

    print(agg)

    top_size_mean = []
    top_size_std_err = []
    other_size_mean = []
    other_size_std_err = []
    for i in language_extensions:
        top_size_mean.append(
            round(agg[(agg.langauge == i)
                                   & (agg.quality_group == 'Top 10')].iloc[0].size_mean))
        top_size_std_err.append(round(agg[(agg.langauge == i)
                                   & (agg.quality_group == 'Top 10')].iloc[0].size_std/
                                      sqrt(agg[(agg.langauge == i)
                                          & (agg.quality_group == 'Top 10')].iloc[0].projects)
                                      ))
        other_size_mean.append(
            round(agg[(agg.langauge == i)
                                   & (agg.quality_group == 'Others')].iloc[0].size_mean))
        other_size_std_err.append(round(agg[(agg.langauge == i)
                                   & (agg.quality_group == 'Others')].iloc[0].size_std/
                                        sqrt(agg[(agg.langauge == i)
                                   & (agg.quality_group == 'Others')].iloc[0].projects)))



    trace1 = go.Bar(
        x=lang_name,
        y=top_size_mean,
        name='Top Length',
        error_y=dict(
            type='data',
            array=top_size_std_err,
            visible=True
        )
    )

    trace2 = go.Bar(
        x=lang_name,
        y=other_size_mean,
        name='Other Length',
        error_y=dict(
            type='data',
            array=other_size_std_err,
            visible=True
        )
    )




    data = [trace1, trace2]
    #layout = go.Layout(
    #    barmode='group'
    #)


    layout = go.Layout(
            barmode='group',
        title='File length per language',
        xaxis=dict(
            title='Language',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Avgerage file length',
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
                 output_type='file')


def run_length_per_lang_figure():
        length_per_lang_figure(major_extensions_file=os.path.join(DATA_PATH
                                                                      , 'repo_programming_file_size_with_major_extension99.csv')
                                   , image_file=os.path.join(FIGURES_PATH, 'length_per_lang_figure.png'))

if __name__ == '__main__':
    run_length_per_lang_figure()