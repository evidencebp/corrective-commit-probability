import scipy.stats as stats
import pandas as pd

import os

from analysis_configuration import DOMINANT_RATE, lang_name, lang_extension
from configuration import DATA_PATH
from repo_utils import get_valid_repos

def compute_lang_anova(major_extensions_file):
    ext = pd.read_csv(major_extensions_file)

    dominant = ext[ext.major_extension_ratio > DOMINANT_RATE]

    trep = get_valid_repos()

    major = pd.merge(trep, dominant, on='repo_name')
    print("projects with a ", DOMINANT_RATE, " dominant extension"
                                             , len(major[major.major_extension_ratio > DOMINANT_RATE]))

    ccp_cpp = major[major.major_extension =='.cpp'].y2019_ccp.tolist()
    ccp_cs = major[major.major_extension =='.cs'].y2019_ccp.tolist()
    ccp_java = major[major.major_extension =='.java'].y2019_ccp.tolist()
    ccp_js = major[major.major_extension =='.js'].y2019_ccp.tolist()
    ccp_php = major[major.major_extension =='.php'].y2019_ccp.tolist()
    ccp_py = major[major.major_extension =='.py'].y2019_ccp.tolist()
    ccp_sh = major[major.major_extension =='.sh'].y2019_ccp.tolist()

    print(stats.f_oneway(ccp_cpp,ccp_cs,ccp_java, ccp_js,ccp_php,ccp_py, ccp_sh))



def run_compute_lang_anova():

    compute_lang_anova(major_extensions_file=os.path.join(DATA_PATH, 'repo_programming_file_size_with_major_extension99.csv'))


if __name__ == '__main__':
    run_compute_lang_anova()