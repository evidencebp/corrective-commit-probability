import os
import pandas as pd
import plotly
import plotly.graph_objects as go

from analysis_configuration import EARLIEST_ANALYZED_YEAR
from configuration import FIGURES_PATH
from repo_utils import get_valid_repos

df = get_valid_repos()


def repos_by_lang():
    g_by_lang = df.groupby(['language'], as_index=False).agg({'repo_name' : 'nunique'
                                                              , 'commits' : 'mean' })
    g_by_lang = g_by_lang[g_by_lang.repo_name > 9]
    g_by_lang = g_by_lang.sort_values(['repo_name', 'language'], ascending=[True, True])

    graphs = [
        go.Bar(x=g_by_lang['language'], y=g_by_lang['repo_name'], name='repos')
        , go.Bar(x=g_by_lang['language'], y=g_by_lang['commits'], name='commits')
    ]

    fig = go.Figure(data=graphs)
    fig.update_layout(
        title=go.layout.Title(
            text="Repositories by language",
            xref="paper",
            x=0
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="Language",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text="Number of repositories",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        )
        )
    fig.write_html(os.path.join(FIGURES_PATH, r'repo_by_lang.html')
                   , auto_open=True)

def scatter(df
            , first_metric
            , second_metric
            , output_file
            , mode='markers'
            , opacity=0.9):
    fig = go.Figure(go.Scatter(x=df[first_metric]
                               , y=df[second_metric]
                               , mode=mode
                               , opacity=opacity))
    fig.write_html(output_file
                   , auto_open=True)


def ccp_vs_stars_scatter():
    scatter(df
            , first_metric='y2019_ccp'
            , second_metric='stargazers_count'
            , output_file=os.path.join(FIGURES_PATH, r'ccp19_vs_stars_scatter.html')
            , mode='markers'
            , opacity=0.9)

def ccp_19_vs_18_scatter():
    scatter(df
            , first_metric='y2019_ccp'
            , second_metric='y2018_ccp'
            , output_file=os.path.join(FIGURES_PATH, r'ccp19_vs_ccp18_scatter.html')
            , mode='markers'
            , opacity=0.9)

def start_year_vs_ccp_scatter():
    scatter(df[df.start_year >= EARLIEST_ANALYZED_YEAR]
            , first_metric='start_year'
            , second_metric='y2019_ccp'
            , output_file=os.path.join(FIGURES_PATH, r'start_year_vs_ccp_scatter.html')
            , mode='markers'
            , opacity=0.9)


def ccp_vs_authors_scatter():
    scatter(df
            , first_metric='y2019_ccp'
            , second_metric='authors'
            , output_file=os.path.join(FIGURES_PATH, r'ccp_vs_authors_scatter.html')
            , mode='markers'
            , opacity=0.9)


def run_plots():

    ccp_19_vs_18_scatter()
    ccp_vs_stars_scatter()
    start_year_vs_ccp_scatter()
    ccp_vs_authors_scatter()

    return df

if __name__ == '__main__':
    #df = run_plots()
    start_year_vs_ccp_scatter()
