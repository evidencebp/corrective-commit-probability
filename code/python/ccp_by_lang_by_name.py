"""
Exlporation
"""
import numpy as np
import os
import pandas as pd

from analysis_configuration import language_extensions
from configuration import DATA_PATH
from positives_mle import ccp_estimator

def analyze_ccp_by_lang_by_name(input_file):
    df = pd.read_csv(input_file)
    base_names = ['/main.', '/login.', '/setup.', '/status.', '/install.', '/database.'
        , '/parser.', '/log.', '/help.', '/format.', '/configuration.', '/db.', '/time.', '/io.', '/stats.']

    df['ccp'] = df.corrective_hit_rate.map(ccp_estimator.estimate_positives)
    print("Specific languages CCP")
    print(df[df.extension.isin(language_extensions)].ccp.describe())

    #print(df[(df.base_name.isin(base_names))
    #         & (df.extension.isin(language_extensions))].sort_values(['base_name', 'extension']))
    df = df[(df.base_name.isin(base_names))
            & (df.extension.isin(language_extensions))]

    df['ccp'] = df.corrective_hit_rate.map(ccp_estimator.estimate_positives)
    print("specific names CCP")
    print(df.ccp.describe())

    g = df.groupby('extension').agg(Mean=('ccp', 'mean'), Std=('ccp', 'std'))
    print("CCP per language on similar files")
    print(g)
   # print(g[g.extension.isin(language_extensions)].sort_values('ccp'))

    g = df.groupby('base_name').agg(Mean=('ccp', 'mean'), Std=('ccp', 'std'))
    print("CCP per base_name")
    print(g.sort_values('base_name'))


    return df

def ccp_on_test(input_file):
    print("CCP per language on test files")
    df = pd.read_csv(input_file)
    df = df[(df.extension.isin(language_extensions))]
    df['ccp'] = df.corrective_hit_rate.map(ccp_estimator.estimate_positives)

    print("Tests CCP")
    print(df.ccp.describe())

    print(df.sort_values(['ccp']))

    return df

def run_ccp_on_tests():
    return ccp_on_test(input_file=os.path.join(DATA_PATH, 'ccp_by_language_on_tests.csv'))

def run_analyze_ccp_by_lang_by_name():
    return analyze_ccp_by_lang_by_name(input_file=os.path.join(DATA_PATH, 'ccp_by_basename.csv'))


if __name__ == '__main__':
    df = run_analyze_ccp_by_lang_by_name()
    df = run_ccp_on_tests()