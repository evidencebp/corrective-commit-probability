from math import sqrt
import os
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

from configuration import DATA_PATH, FIGURES_PATH




def get_quality_figure(data_file
                       , image_file
                       , title):
    
    terms = ['low_quality', 'technical_debt', 'code_smell', 'swearing', 'algorithm', 'function']

    df = pd.read_csv(data_file)

    term_mean = []
    term_std_err = []
    no_term_mean = []
    no_term_std_err = []

    for i in terms:
        term_mean.append(df[i + '_avg'].iloc[0])
        term_std_err.append(df[i + '_std'].iloc[0] /sqrt(df[i + '_cnt'].iloc[0]))
        no_term_mean.append(df['not_' + i + '_avg'].iloc[0])
        no_term_std_err.append(df['not_' +i + '_std'].iloc[0] /sqrt(df[i + '_cnt'].iloc[0]))

    terms_display = [i.replace("_", " ") for i in terms]
    trace1 = go.Bar(
        x=terms_display,
        y=term_mean,
        name='Terms CCP',
        error_y=dict(
            type='data',
            array=term_std_err,
            visible=True
        )
    )

    trace2 = go.Bar(
        x=terms_display,
        y=no_term_mean,
        name='No Terms CCP',
        error_y=dict(
            type='data',
            array=no_term_std_err,
            visible=True
        )
    )



    data = [trace1, trace2]
    #layout = go.Layout(
    #    barmode='group'
    #)


    layout = go.Layout(
            barmode='group',
        title=title,
        xaxis=dict(
            title='Term',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Avgerage CCP',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    """
    plot(fig,
        image = 'png', image_filename=image_file,
                 output_type='file')
    """
    fig.show()
    fig.write_image(image_file)

    return fig


def run_quality_figures():
    file_fig = get_quality_figure(data_file=os.path.join(DATA_PATH
                                                        , 'ccp_by_quality_terms.csv')
                                  , image_file=os.path.join(FIGURES_PATH
                                                        , 'ccp_by_quality_terms.png')
                                  , title="Avg. CCP per term appearance (by file)")
    repo_fig = get_quality_figure(data_file=os.path.join(DATA_PATH
                                                        , 'ccp_by_quality_terms_by_repo.csv')
                                    ,image_file = os.path.join(FIGURES_PATH
                                                              , 'ccp_by_quality_terms_by_repo.png')
                                    , title="Avg. CCP per term appearance (by project)")


if __name__ == '__main__':
    df = run_quality_figures()
