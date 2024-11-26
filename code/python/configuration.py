
import sys

ANALYSIS_PATH = 'c:/src/analysis_utils'
sys.path.append(ANALYSIS_PATH)

BASE_PATH = r'/Users/idan/src/in-work/ccp-journal/'
DATA_PATH = BASE_PATH + r'data/'
FIGURES_PATH = BASE_PATH + r'figures/'
PERFORMANCE_PATH = BASE_PATH + r'performance/'
MODELS_PATH = BASE_PATH + r'models/'

# repo_name,year,min_commit_time,max_commit_time,min_commit,max_commit,commits,non_merge_commits,corrective_commits
# ,corrective_rate,ccp,refactor_mle,avg_coupling_size,avg_coupling_code_size,avg_coupling_size_capped
# ,avg_coupling_code_size_capped,avg_coupling_size_cut,avg_coupling_code_size_cut,authors,Author_email
# ,same_day_duration_avg,files_edited,files_created,files_created_ccp,tests_presence,multiline_message_ratio
# ,message_length_avg,same_date_duration_avg,same_date_commits,commit_period,commit_days,commits_per_day
# ,commit_weeks,commit_months,commit_days_of_week,commit_hours,commit_day_density,survival_avg,above_year_prob
# ,commits_per_developer,involved_developers,involved_developers_commits,commits_per_involved_developer
# ,developer_capped_commits,capped_commits_per_developer,involved_developers_capped_commits
# ,capped_commits_per_involved_developer,stars,detection_efficiency,avg_file_size,capped_avg_file_size
# ,avg_code_file_size,capped_avg_code_file_size

CONCEPT = 'ccp'
ADMINISTRATIVE_FEATURES = ['repo_name',  'year','author_email', 'Author_email', 'names', 'author_email_domain',]
COMPLEX_FEATURES =['min_commit_time', 'max_commit_time','min_commit','max_commit','detection_efficiency','language',]

NON_CORE_FEATURES = ['above_year_prob', 'commit_day_density', 'commit_days', 'commit_days_of_week', 'commit_hours'
, 'commit_months', 'commit_period', 'commit_weeks', 'commits', 'commits_per_day'
, 'files_created', 'files_created_ccp', 'files_edited'
, 'message_length_avg', 'multiline_message_ratio', 'non_merge_commits',
'refactor_mle', 'same_date_commits', 'same_date_duration_avg', 'same_day_duration_avg', 'survival_avg'
, 'corrective_multiline_message_ratio' ,'corrective_message_length_avg', 'non_corrective_multiline_message_ratio'
, 'non_corrective_message_length_avg'
                     ]
NON_PREDICTIVE_FEATURES = set([CONCEPT, 'corrective_rate', 'corrective_commits'] + ADMINISTRATIVE_FEATURES + COMPLEX_FEATURES
                              + NON_CORE_FEATURES
                              )
NUMERIC_NULL = -1
TEST_SIZE = 0.2
RANDOM_STATE = 37


CONCEPT = 'high_quality'
DATASET = 'repo_properties.csv'
