# mklink /D %HOMEDRIVE%%HOMEPATH%\anaconda  C:\ProgramData\Anaconda3

HOME = 'C:/Idan/GitHub/in-work/ccp2018/'
DATA_PATH = HOME + 'data/'
FIGURES_PATH = HOME + 'figures/'
SCRIPTS_PATH = HOME + 'code/queries'

LANG_CODE_PATH = "C:/Idan/GitHub/in-work/lang"
LANG_DATA_PATH = 'C:/Idan/GitHub/in-work/lang/data/'

ANALYSIS_UTIL_PATH = 'C:/Idan/GitHub/analysis_utils/'

import sys
sys.path.append(ANALYSIS_UTIL_PATH)
sys.path.append(LANG_CODE_PATH)

# Important files constants
REPOSITORIES_PROPERTIES = 'repos_corrective_properties.csv'
REPOSITORIES_GIT_PROPERTIES = 'active_2019_atleast_200_gitprop_no_dominante.csv'
REPOSITORIES_FILE = 'repos_full.csv'

# Fill here your credentials.
# The credential are used to extract repository properties from GitHub
GITHUB_USER = ''
GITHUB_PASSWORD = ''


ANALYZED_YEAR = 2019
