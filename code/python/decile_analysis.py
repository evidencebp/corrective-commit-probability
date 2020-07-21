from math import log10
from numpy import inf
import os
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

from analysis_configuration import KILOBYTE, lang_name
from configuration import DATA_PATH, ANALYZED_YEAR, FIGURES_PATH
from feature_pair_analysis import bin_metric_by_quantiles
from repo_utils import get_valid_repos


metrics = ['capped_avg_file', 'avg_capped_files', 'Commit_Per_Involved_User_Cappped', 'age'
    , 'repo_all_commits', 'authors', 'stargazers_count'
    , 'repo_all_commits_log10', 'authors_log10', 'stargazers_count_log10'
    , 'continuing_developers_ratio', 'churn', 'Onboarding', 'package_avg']


def decile_analysis(major_extensions_file
                    , coupling_file
                    , commits_per_user_file
                    , churn_file
                    , onboarding_file
                    , reuse_file
                    , output_file):

    repos = get_valid_repos()

    repos = repos.rename(columns={'commits' : 'repo_all_commits'})

    bin_metric_by_quantiles(repos
                            , 'y2019_ccp'
                            , 'y2019_ccp_10bins'
                            , bins=10
                            )
    # File length
    rep_size = pd.read_csv(major_extensions_file)
    df = pd.merge(repos,rep_size,on='repo_name', how='left')
    df['Capped_Length_KB']  = df.capped_avg_file/ KILOBYTE

    # Coupling
    coupling_size = pd.read_csv(coupling_file)
    coupling_size = coupling_size[coupling_size.year == ANALYZED_YEAR]
    df = pd.merge(df, coupling_size, on='repo_name', how='left')
    df['Commit_Size_Capped'] = df['avg_capped_files']

    users_per_project = pd.read_csv(commits_per_user_file)
    users_per_project = users_per_project[users_per_project.year == ANALYZED_YEAR]
        
    df = pd.merge(df, users_per_project, on='repo_name', how='left')

    df['commit_per_user'] = df.apply(
        lambda x: x.y2019_commits/x.users if x.users > 0 else None, axis=1)
    df['commit_per_user_above_11'] = df.apply(
        lambda x: x.users_above_11_commits/x.users_above_11 if x.users_above_11 > 0 else None, axis=1)

    df['commit_per_user_cap'] = df.apply(
        lambda x: x.users_capped_commit/x.users if x.users > 0 else None, axis=1)
    df['Commit_Per_Involved_User_Cappped'] = df.apply(
        lambda x: x.commits_above_11_500_cap/x.users_above_11 if x.users_above_11 > 0 else None, axis=1)

    # print(df.groupby(['y2019_ccp_10bins']).agg({'Commit_Per_Involved_User_Cappped' : 'mean', 'repo_name' : 'count'}).sort_index())

    df['repo_all_commits_log10']= df.repo_all_commits.map(lambda x: log10(x) if x> 0 else x)
    df['authors_log10']= df.authors.map(lambda x: log10(x) if x> 0 else x)
    df['stargazers_count_log10']= df.stargazers_count.map(lambda x: log10(x) if x> 0 else x)

    churn = pd.read_csv(churn_file)
    churn = churn[churn.year == ANALYZED_YEAR-1]

    df = pd.merge(df, churn, on='repo_name', how='left')
    df['churn'] = 1.0 - df['continuing_developers_ratio']

    onboarding = pd.read_csv(onboarding_file)
    onboarding = onboarding[onboarding.year == ANALYZED_YEAR]
    df = pd.merge(df, onboarding, on='repo_name', how='left')
    df['Onboarding'] = df.comming_involved_developers_ratio

    reuse = pd.read_csv(reuse_file)
    df = pd.merge(df, reuse, on='repo_name', how='left')

    aggregations = {i : 'mean' for i in metrics}
    aggregations['repo_name'] = 'count'
    g = df.groupby('y2019_ccp_10bins', as_index=False).agg(aggregations)


    g.to_csv(output_file)

    plot_all_metrics(df
                     , grouping_column='y2019_ccp_10bins')

    plot_by_ccp_all_metrics(df
                            , grouping_columns = ['Capped_Length_KB', 'Commit_Size_Capped', 'package_avg'])
    #plot_ccp_by_length_per_lang(df)

    return df

def plot_all_metrics(df
                 , grouping_column):

    df = df.sort_values(grouping_column)

    for metric_column in metrics:
        plot_deciles(df
                     , grouping_column=grouping_column
                     , metric_column=metric_column
                     , title=" CCP groups vs. " + metric_column.replace("_", " ")
                     , xaxis_title="CCP groups"
                     , output_file=os.path.join(FIGURES_PATH, metric_column + '.png'))


def plot_by_ccp_all_metrics(df
                 , grouping_columns
                 , title=None
                 , output_file=None
                 , metric_column='y2019_ccp'):

    title_per_graph = not title

    for grouping_column in grouping_columns:
        deciles_colomn = grouping_column +'_deciles'
        bin_metric_by_quantiles(df
                                , grouping_column
                                , deciles_colomn
                                , bins=10
                                , top_val=inf
                                )
        if title_per_graph:
            title = deciles_colomn.replace("_", " ") + " vs. CCP"
        if not output_file:
            group_output_file = os.path.join(FIGURES_PATH
                                                , 'ccp_by_{grouping_column}.png'.format(grouping_column=grouping_column))
        df = df.sort_values(grouping_column)
        plot_deciles(df
                     , grouping_column=deciles_colomn
                     , metric_column='y2019_ccp'
                     , title=title.replace("_", " ")
                     , xaxis_title=deciles_colomn.replace("_", " ")
                     , output_file=group_output_file)

def plot_ccp_by_length_per_lang(df):
    for i in lang_name:
        cur_df = df.copy()
        cur_df = cur_df[cur_df.language == i]
        plot_by_ccp_all_metrics(cur_df
                            ,grouping_columns=['Capped_Length_KB']
                            , title="ccp_by_len_per_{lang}".format(lang=i)
                            , output_file= os.path.join(FIGURES_PATH
                                                , 'ccp_by_len_per_{lang}.png'.format(lang=i)))

def plot_deciles(df
                 , grouping_column
                 , metric_column
                 , title
                 , xaxis_title
                 , output_file):

    #print("in plot")
    #print(df.groupby([grouping_column]).agg({metric_column : 'mean', 'repo_name' : 'count'}))
    fig = go.Figure()
    item = 0;
    for cur_group in df[grouping_column].unique():
        color = 'blue' # 'rgb(' +str(20*item +1) + ',' + str(100 + 10*item) +',' + str(254 - 15*item) + ')'
        if str(cur_group).find(',') > 0:
            name = '<=' + str(cur_group)[str(cur_group).find(',')+1:-1]
        else:
            name = str(cur_group)
        trace = go.Box(
            y=df[df[grouping_column] == cur_group][metric_column].tolist(),
            name=name,
            marker=dict(
                color=color,
            ),
            boxpoints=False,
            boxmean=True
        )
        fig.add_trace(trace)
        item += 1

    fig.update_layout(
        title=title.replace("_", " "),
        xaxis_title=xaxis_title.replace("_", " "),
        yaxis_title=metric_column.replace("_", " "),
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="black"
        )
    )
    fig.update_layout(showlegend=False)

    fig.show()
    fig.write_image(output_file)


def plot_longevity(repo_properties_file
                   , longevity_file):
    """
    Longevity is on 2018 porjects, which are in a different file and therfore get a different function.
    """
    repos = pd.read_csv(repo_properties_file)
    longevity = pd.read_csv(longevity_file)

    df = pd.merge(repos, longevity, on='repo_name', how='left')
    df = df[(df.fork == False) & (df.y2018_ccp > 0) & (df.y2018_ccp < 1)]

    df['after_2019_end'] = df.days_from_2019_end.map(lambda x: 1 if x > 0 else 0)
    grouping_column = 'y2018_ccp_10bins'

    repos_2019 = get_valid_repos()
    bins = 10
    cuts = [0.0] + [repos_2019['y2019_ccp'].quantile((1.0/bins)*i) for i in range(1, bins)] + [1.0]

    df[grouping_column] = pd.cut(df['y2018_ccp'], cuts)

    """
    bin_metric_by_quantiles(df
                            , 'y2018_ccp'
                            , grouping_column
                            , bins=10
                            )
    """
    df = df.sort_values(grouping_column)
    plot_deciles(df=df
                 , grouping_column=grouping_column
                 , metric_column='after_2019_end'
                 , title='Longevity by CCP'
                 , xaxis_title='CCP deciles'
                 , output_file=os.path.join(FIGURES_PATH,'longevity.png'))

def run_plot_longevity():
    plot_longevity(repo_properties_file=os.path.join(DATA_PATH, 'repos_full_2018.csv')
                   , longevity_file=os.path.join(DATA_PATH, 'longevity_2018.csv'))
def run_decile_analysis():
        return decile_analysis(major_extensions_file=
                               os.path.join(DATA_PATH
                                            , 'repo_programming_file_size_with_major_extension99.csv')
                               , coupling_file=os.path.join(DATA_PATH
                                                        , 'coupling_by_repo.csv')
                               , commits_per_user_file=os.path.join(DATA_PATH
                                                                    , 'project_user_contribution_stats.csv')
                               , churn_file=os.path.join(DATA_PATH
                                    , 'invovled_developers_churn.csv')
                               , onboarding_file = os.path.join(DATA_PATH
                                       , 'developer_on_boarding.csv')
                               , reuse_file = os.path.join(DATA_PATH
                                       , 'imports_per_repo.csv')
                               , output_file=os.path.join(DATA_PATH, 'decile_bins.csv'))

if __name__ == '__main__':
    df = run_decile_analysis()
    #run_plot_longevity()