"""
CDF of CCP per language figure
"""
import os
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot, plot

from analysis_configuration import DOMINANT_RATE, lang_name, lang_extension
from configuration import DATA_PATH, FIGURES_PATH
from repo_utils import get_valid_repos


LIMIT = 0.33



def ccp_cdf_per_language(major_extensions_file
                         , image_file):

    ext = pd.read_csv(major_extensions_file)
    dominant = ext[ext.major_extension_ratio > DOMINANT_RATE]
    print("Number of repositories with a dominant extension above"
          , DOMINANT_RATE
          , " is "
          , len(dominant))

    trep = get_valid_repos()

    major = pd.merge(trep, dominant, left_on='repo_name', right_on='repo_name')

    trepu = major

    cdfs = {}
    traces = []
    for i in lang_name:
        cdf = trepu[trepu.major_extension == lang_extension[i]].y2019_ccp.value_counts(normalize=True).sort_index().cumsum()
        cdf = pd.DataFrame(cdf)
        cdf = cdf.reset_index()
        cdf.columns = ['ccp', 'cdf']
        cdf = cdf[cdf.ccp < LIMIT]
        cdfs[i] = cdf
        traces.append(go.Scatter(
                            x=cdfs[i].ccp,
                            y=cdfs[i].cdf,
                            mode='lines',
                            name=i
                        ))

    layout = go.Layout(
        title='CDF of CCP for common languages',
        xaxis=dict(
            title='CCP',
            titlefont=dict(
                family='Courier New, monospace',
                size=24,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='CDF of projects CCP',
            titlefont=dict(
                family='Courier New, monospace',
                size=24,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=traces
                    , layout=layout)

    plot(fig
         , image='png'
         , image_filename=image_file
         , output_type='file'
         , image_width=800, image_height=400
         )

    #plot(fig)
    fig.write_image(image_file)





def run_ccp_cdf_per_language():

    ccp_cdf_per_language(major_extensions_file=os.path.join(DATA_PATH, 'repo_programming_file_size_with_major_extension99.csv')
                         , image_file=os.path.join(FIGURES_PATH, 'ccp_per_lang.png'))


if __name__ == '__main__':
    run_ccp_cdf_per_language()