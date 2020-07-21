"""
Analyze file size with respect to quality.
"""
import os
import pandas as pd

from analysis_configuration import  DOMINANT_RATE, lang_name, lang_extension
from configuration import DATA_PATH, FIGURES_PATH
from feature_pair_analysis import pretty_print, pair_analysis_by_dev_num_group, pair_analysis_by_age_group\
    , pair_analysis_by_bins_to_file
from plots import scatter
from repo_utils import get_valid_repos


from analysis_configuration import KILOBYTE

def file_size_analysis(major_extensions_file):

    trep = get_valid_repos()

    rep_size = pd.read_csv(major_extensions_file)
    print( 'avg file mean', rep_size.avg_size.mean()/KILOBYTE)
    print( 'std file mean', rep_size.std_size.mean()/KILOBYTE)
    print( 'avg capped file mean', rep_size.capped_avg_file.mean()/KILOBYTE)
    print( 'std capped file mean', rep_size.capped_std_file.mean()/KILOBYTE)
    print( 'avg capped file mean', rep_size.capped_avg_file.mean()/KILOBYTE)
    print( 'std capped file mean/avg capped file mean', rep_size.capped_std_file.mean()/rep_size.capped_avg_file.mean())

    treps = pd.merge(trep,rep_size,on='repo_name')
    print( rep_size.capped_avg_file.describe())


    size_25_q = rep_size.capped_avg_file.quantile(0.25)
    print("size 25 quantile", size_25_q, "in kb", size_25_q/KILOBYTE)
    size_75_q = rep_size.capped_avg_file.quantile(0.75)
    print("size 75 quantile", size_75_q, "in kb", size_75_q/KILOBYTE)

    treps['size_group'] = treps.apply(lambda x: 'Lower 25' if x.capped_avg_file < size_25_q
        else  "top 25" if x.capped_avg_file > size_75_q else "Middle", axis=1)

    print( 'top 10 prob', 1.0*len(treps[treps.quality_group == 'Top 10'])/len(treps))
    top_10_in_l25 = 1.0*len(treps[(treps.quality_group == 'Top 10')
                                                   & (treps.size_group =='Lower 25')])/len(treps[treps.size_group =='Lower 25'])
    print( 'top 10 prob in lower 25', top_10_in_l25)
    top_10_in_t25 = 1.0*len(treps[(treps.quality_group == 'Top 10')
                                                 & (treps.size_group =='top 25')])/len(treps[treps.size_group =='top 25'])
    print( 'top 10 prob in top 25', top_10_in_t25)
    print("short files lift ", top_10_in_l25/top_10_in_t25 -1 )

    group_by_size = treps.groupby(['size_group'], as_index=False).agg({'y2019_ccp' : 'mean'})
    print(group_by_size)

    print( "all files")
    print( treps.groupby('quality_group').agg(
        {'capped_avg_file' : 'mean', 'avg_size' : 'mean', 'files' : 'sum', 'repo_name' :'count'}))

    for i in lang_name:
        print( i, " files")
        print( treps[(treps.major_extension_ratio > DOMINANT_RATE) & (treps.major_extension == lang_extension[i])].groupby('quality_group').agg(
            {'capped_avg_file' : 'mean', 'avg_size' : 'mean', 'files' : 'sum', 'repo_name':'count'}))

    print("Size controled by developer groups")
    pretty_print(pair_analysis_by_dev_num_group(treps
                  , 'size_group'
                  , 'y2019_ccp'))

    print("Size controled by project age")
    pretty_print(pair_analysis_by_age_group(treps
                  , 'size_group'
                  , 'y2019_ccp'))

    scatter(treps
            , first_metric='y2019_ccp'
            , second_metric='capped_avg_file'
            , output_file=os.path.join(FIGURES_PATH, r'ccp_vs_length_scatter.html')
            , mode='markers'
            , opacity=0.9)
    pair_analysis_by_bins_to_file(treps
                                  , 'y2019_ccp'
                                  , 'capped_avg_file'
                                  , output_file=os.path.join(DATA_PATH, 'ccp_vs_length_bins.csv')
                                  , bins=10
                                  )


    return treps

def run_file_size_analysis():
        return file_size_analysis(major_extensions_file=os.path.join(DATA_PATH, 'repo_programming_file_size_with_major_extension99.csv'))

if __name__ == '__main__':
    df = run_file_size_analysis()