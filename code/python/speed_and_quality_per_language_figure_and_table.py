"""
Langauge speed and CCP - table and figure
"""


import pandas as pd
#import matplotlib.pyplot as plt
import math
import os
#import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import plotly.io as pio

from analysis_configuration import language_extensions, lang_name, lang_extension, lang_by_extension
from configuration import DATA_PATH, FIGURES_PATH
from feature_pair_analysis import pair_analysis_by_bins_to_file
from plots import scatter
from repo_utils import get_valid_repos

DOMINANT_RATE = 0.8

def file_length_per_language(major_extensions_file
                              , commits_per_user_file
                              , image_file):

    ext = pd.read_csv(major_extensions_file)

    dominant = ext[ext.major_extension_ratio > DOMINANT_RATE]

    trep = get_valid_repos()

    major = pd.merge(trep, dominant, left_on='repo_name', right_on='repo_name')

    users_per_project = pd.read_csv(commits_per_user_file)
    users_per_project = users_per_project[users_per_project.year == 2019]
    trepu = pd.merge(major,users_per_project,on='repo_name')

    trepu['commit_per_user'] = trepu.apply(
        lambda x: x.y2019_commits/x.users if x.users > 0 else None, axis=1)
    trepu['commit_per_user_above_11'] = trepu.apply(
        lambda x: x.users_above_11_commits/x.users_above_11 if x.users_above_11 > 0 else None, axis=1)

    trepu['commit_per_user_cap'] = trepu.apply(
        lambda x: x.users_capped_commit/x.users if x.users > 0 else None, axis=1)
    trepu['commit_per_user_above_11_cap'] = trepu.apply(
        lambda x: x.commits_above_11_500_cap/x.users_above_11 if x.users_above_11 > 0 else None, axis=1)




    agg_lang = trepu[trepu.major_extension.isin(language_extensions)].groupby('major_extension'
                        , as_index=False).agg({'repo_name' : 'count'
                                                , 'y2019_ccp' : {'mean', 'std'}
                                                , 'commit_per_user_above_11_cap': {'mean', 'std'}}
                                              )

    agg_lang.columns = agg_lang.columns.droplevel()
    agg_lang.columns = [u'langauge', u'projects', u'ccp_mean', u'ccp_std', u'speed_mean' , u'speed_std']


    agg_lang_quality = trepu[trepu.major_extension.isin(language_extensions)].groupby(
        ['major_extension', 'quality_group']
                        , as_index=False).agg({'repo_name' : 'count'
                                                , 'commit_per_user_above_11_cap': {'mean', 'std'}}
                                              )
    agg_lang_quality.columns = agg_lang_quality.columns.droplevel()

    """
    agg_lang_quality = agg_lang_quality.rename(columns={
        'major_extension' : u'langauge'
        , 'std': u'speed_std'
        , 'mean': u'speed_mean'
        , 'count': u'projects'
    })
    """
    agg_lang_quality.columns = [u'langauge', u'quality_group', u'projects', u'speed_mean', u'speed_std']

    all_speed_mean = []
    all_speed_std = []

    top_speed_mean = []
    top_speed_std = []
    other_speed_mean = []
    other_speed_std = []
    ccp_mean = []
    ccp_std = []
    for i in language_extensions:
        top_speed_mean.append(
            round(agg_lang_quality[(agg_lang_quality.langauge == i)
                                   & (agg_lang_quality.quality_group == 'Top 10')].iloc[0].speed_mean))
        top_speed_std.append(round(agg_lang_quality[(agg_lang_quality.langauge == i)
                                   & (agg_lang_quality.quality_group == 'Top 10')].iloc[0].speed_std/
                                   math.sqrt(agg_lang_quality[(agg_lang_quality.langauge == i)
                                   & (agg_lang_quality.quality_group == 'Top 10')].iloc[0].projects)))
        other_speed_mean.append(
            round(agg_lang_quality[(agg_lang_quality.langauge == i)
                                   & (agg_lang_quality.quality_group == 'Others')].iloc[0].speed_mean))
        other_speed_std.append(round(agg_lang_quality[(agg_lang_quality.langauge == i)
                                   & (agg_lang_quality.quality_group == 'Others')].iloc[0].speed_std/
                                     math.sqrt(agg_lang_quality[(agg_lang_quality.langauge == i)
                                   & (agg_lang_quality.quality_group == 'Others')].iloc[0].projects)))
        ccp_mean.append(round(100*agg_lang[(agg_lang.langauge == i)].iloc[0].ccp_mean))
        ccp_std.append(100*round(agg_lang[(agg_lang.langauge == i)].iloc[0].ccp_std/
                                 math.sqrt(agg_lang[(agg_lang.langauge == i)].iloc[0].projects)))
        all_speed_mean.append(round(agg_lang[(agg_lang.langauge == i)].iloc[0].speed_mean))
        all_speed_std.append(round(agg_lang[(agg_lang.langauge == i)].iloc[0].speed_std/
                                   math.sqrt(agg_lang[(agg_lang.langauge == i)].iloc[0].projects)))


    trace0 = go.Bar(
        x=lang_name,
        y=all_speed_mean,
        name='Speed',
        error_y=dict(
            type='data',
            array=all_speed_std,
            visible=True
        )
    )
    trace1 = go.Bar(
        x=lang_name,
        y=top_speed_mean,
        name='Top Speed',
        error_y=dict(
            type='data',
            array=top_speed_std,
            visible=True
        )
    )



    trace2 = go.Bar(
        x=lang_name,
        y=other_speed_mean,
        name='Other Speed',
        error_y=dict(
            type='data',
            array=other_speed_std,
            visible=True
        )
    )

    trace3 = go.Bar(
        x=lang_name,
        y=ccp_mean,
        name='CCP',
        error_y=dict(
            type='data',
            array=ccp_std,
            visible=True
        )
    )
    data = [trace0, trace1, trace2, trace3]

    layout = go.Layout(
            barmode='group',
        title='Speed and CCP per language',
        xaxis=dict(
            title='Language',
            titlefont=dict(
                family='Courier New, monospace',
                size=24,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Commit per developer, CCP',
            titlefont=dict(
                family='Courier New, monospace',
                size=24,
                color='#7f7f7f'
            )
        )
    )

    fig = go.Figure(data=data, layout=layout)
    plot(fig,
        image = 'png', image_filename=image_file,
                 output_type='file')


    print(r"\begin{tabular}{| l| l| l| l| l| l|}")
    print(r"   \hline ")
    Title = r" Metric & Projects & CCP & Speed & Top Speed & Others Speed  \\ \hline"
    print(Title)
    for i in agg_lang.sort_values('ccp_mean').langauge.tolist():
        Line = str(lang_by_extension(i))

        Line = Line + " & " + str(agg_lang[(agg_lang.langauge == i)].iloc[0].projects)

        Line = Line + " & " + str(round(1*agg_lang[(agg_lang.langauge == i)].iloc[0].ccp_mean, 2))
        Line = Line + " $\pm$ " + str(round(1*agg_lang[(agg_lang.langauge == i)].iloc[0].ccp_std/
                                   math.sqrt(agg_lang[(agg_lang.langauge == i)].iloc[0].projects),3))

        Line = Line + " & " + str(int(agg_lang[(agg_lang.langauge == i)].iloc[0].speed_mean))
        Line = Line + " $\pm$ " + str(int(agg_lang[(agg_lang.langauge == i)].iloc[0].speed_std/
                                   math.sqrt(agg_lang[(agg_lang.langauge == i)].iloc[0].projects)))


        Line = Line + " & " + str(int(agg_lang_quality[(agg_lang_quality.langauge == i)
                                   & (agg_lang_quality.quality_group == 'Top 10')].iloc[0].speed_mean))
        Line = Line + " $\pm$ " + str(int(agg_lang_quality[(agg_lang_quality.langauge == i)
                                   & (agg_lang_quality.quality_group == 'Top 10')].iloc[0].speed_std/
                                   math.sqrt(agg_lang_quality[(agg_lang_quality.langauge == i)
                                   & (agg_lang_quality.quality_group == 'Top 10')].iloc[0].projects)))
        Line = Line + " & " + str(int(agg_lang_quality[(agg_lang_quality.langauge == i)
                                   & (agg_lang_quality.quality_group == 'Others')].iloc[0].speed_mean))
        Line = Line + " $\pm$ " + str(int(agg_lang_quality[(agg_lang_quality.langauge == i)
                                   & (agg_lang_quality.quality_group == 'Others')].iloc[0].speed_std/
                                   math.sqrt(agg_lang_quality[(agg_lang_quality.langauge == i)
                                   & (agg_lang_quality.quality_group == 'Others')].iloc[0].projects)))


        Line = Line + r" \\ \hline"
        print(Line)

    scatter(trepu
            , first_metric='y2019_ccp'
            , second_metric='commit_per_user_above_11_cap'
            , output_file=os.path.join(FIGURES_PATH, r'ccp_vs_speed_scatter.html')
            , mode='markers'
            , opacity=0.9)

    pair_analysis_by_bins_to_file(trepu
                                  , 'y2019_ccp'
                                  , 'commit_per_user_above_11_cap'
                                  , output_file=os.path.join(DATA_PATH, 'ccp_vs_speed_bins.csv')
                                  , bins=10
                                  )



def run_file_length_per_language():
    file_length_per_language(major_extensions_file=os.path.join(DATA_PATH, 'repo_programming_file_size_with_major_extension99.csv')
                                  , commits_per_user_file=os.path.join(DATA_PATH, 'project_user_contribution_stats.csv')
                                  , image_file=os.path.join(FIGURES_PATH, 'speed_per_quality_and_ccp_per_lang.png'))



if __name__ == '__main__':
    run_file_length_per_language()