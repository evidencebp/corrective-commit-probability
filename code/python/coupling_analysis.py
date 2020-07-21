"""
Analyze file size with respect to quality.
"""
import os
import pandas as pd

import configuration
from analysis_configuration import DOMINANT_RATE, lang_name, lang_extension
from configuration import DATA_PATH, ANALYZED_YEAR, FIGURES_PATH
from feature_pair_analysis import pair_analysis_by_bins_to_file
from file_size_analysis import run_file_size_analysis
from plots import scatter
from repo_utils import get_valid_repos


def coupling_analysis(coupling_file):
    trep = get_valid_repos()

    coupling_size = pd.read_csv(coupling_file)
    coupling_size = coupling_size[coupling_size.year == ANALYZED_YEAR]

    treps = pd.merge(trep, coupling_size, on='repo_name')
    print(treps.avg_capped_files.describe())

    coupling_25_q = treps.avg_capped_files.quantile(0.25)
    print("coupling 25 quantile", coupling_25_q)
    coupling_75_q = treps.avg_capped_files.quantile(0.75)
    print("coupling 75 quantile", coupling_75_q)
 
    treps['coupling_group'] = treps.apply(lambda x: 'Lower 25' if x.avg_capped_files < coupling_25_q
    else "top 25" if x.avg_capped_files > coupling_75_q else "Middle", axis=1)

    print('top 10 prob', 1.0 * len(treps[treps.quality_group == 'Top 10']) / len(treps))
    top_10_in_l25 = 1.0 * len(treps[(treps.quality_group == 'Top 10')
                                    & (treps.coupling_group == 'Lower 25')]) / len(
        treps[treps.coupling_group == 'Lower 25'])
    print('top 10 prob in lower 25', top_10_in_l25)
    top_10_in_t25 = 1.0 * len(treps[(treps.quality_group == 'Top 10')
                                    & (treps.coupling_group == 'top 25')]) / len(
        treps[treps.coupling_group == 'top 25'])
    print('top 10 prob in top 25', top_10_in_t25)
    print("short files lift ", top_10_in_l25 / top_10_in_t25 - 1)

    print("CCP in 4 top deciles"
          ,  round(treps[treps.avg_capped_files > 8.156].y2019_ccp.mean(),2))
    group_by_size = treps.groupby(['coupling_group'], as_index=False).agg({'y2019_ccp': 'mean'})
    print(group_by_size)

    size_df = run_file_size_analysis()
    joint = pd.merge(treps, size_df, on='repo_name')

    both_l25 = len(joint[(joint.coupling_group == 'Lower 25') & (joint.size_group == 'Lower 25')])
    top_10_in_both_l25 = 1.0 * len(joint[(joint.quality_group_x == 'Top 10')
                                         & (joint.coupling_group == 'Lower 25')
                                         & (joint.size_group == 'Lower 25')
                                         ]) / both_l25

    print('top 10 prob in lower 25 in coupling and size', top_10_in_both_l25)

    print('both lower 25', both_l25, "ratio", both_l25 / len(joint))
    print("both lower 25 CCP",
          joint[(joint.coupling_group == 'Lower 25') & (joint.size_group == 'Lower 25')].y2019_ccp_x.mean())

    return treps


"""
    scatter(treps
            , first_metric='y2019_ccp'
            , second_metric='avg_capped_files'
            , output_file=os.path.join(FIGURES_PATH, r'ccp_vs_coupling_scatter.html')
            , mode='markers'
            , opacity=0.9)
    pair_analysis_by_bins_to_file(treps
                                  , 'y2019_ccp'
                                  , 'avg_capped_files'
                                  , output_file=os.path.join(DATA_PATH, 'ccp_vs_coupling_bins.csv')
                                  , bins=10
                                  )
    return treps
"""


def run_coupling_analysis():
    return coupling_analysis(coupling_file=os.path.join(DATA_PATH
                                                        , 'coupling_by_repo.csv'))


if __name__ == '__main__':
    df = run_coupling_analysis()