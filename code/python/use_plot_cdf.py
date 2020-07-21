
import configuration
from plot_cdf import plot_cdf, plot_cdf_by_column
from repo_utils import get_valid_repos

def plot_ccp_pdf():
    df = get_valid_repos()

    plot_cdf_by_column(df
             , column_name='y2019_ccp'
             , title='CDF of CCP'
             , output_file='c:/tmp/ccp_by_dev_num_group_cdf.png'
             , subsets_column='dev_num_group')


    plot_cdf_by_column(df
             , column_name='y2019_ccp'
             , title='CDF of CCP'
             , output_file='c:/tmp/ccp_by_age_group_cdf.png'
             , subsets_column='age_group')


if __name__ == '__main__':
    df = plot_ccp_pdf()
