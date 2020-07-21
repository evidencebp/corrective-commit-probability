
from compute_confusion_matrix import run_compute_confusion_matrix
from describe_repositories import run_describe_repos
from bootstrap_figure_plotly impport run_bootstrap_figure
from bootstrap_models import run_bootstrap_models
from English_analysis import run_English_analysis
from build_repo_ccp_dist import build_repo_ccp_dist
from star_analysis import run_star_analysis
from longevity_analysis import run_analyze_longevity
from ccp_paer_lang_cdf_figure import run_ccp_cdf_per_language
from lang_ccp_anova import run_compute_lang_anova
from length_per_lang_figure import run_length_per_lang_figure
from file_size_analysis import run_file_size_analysis
from speed_consistency import run_speed_consistency
from speed_and_quality_per_language_figure_and_table import run_file_length_per_language
from churn_analysis import run_churn_analysis
from churn_ccp_cochange import run_churn_ccp_cochange
from onboarding_ccp_cochange import run_onboarding_ccp_cochange

def main():
    """
        Runs all computations
        Note the some part should be done manually or in Big Query so they are described in comments.
    """

    """ The code and analysis here dependes and the langaue model and it performance.
        Take the model performance from the lang repository
        Update the positive_mle ccp_estimator to the model recall and fpr
    """
    # Run linguistic_model_performance in the lang repository to update the predictions

    # Get CM performance description
    run_compute_confusion_matrix()

    # Comnputaions for the MLE validations
    run_bootstrap_models()
    run_bootstrap_figure()

     """
        1. Run active_repos_at_year.sql in BigQuery to generate all project with a minimal number of commits
        Output into ccp.active_repos2019, that will be downloaded to a local file active_atleast_100_2019.csv
        2. Use extract_project_properties to identify forks (to filter out) and store in active_2019_atleast_100_fork.csv
        3. Use extract_project_propertties to get other properties for non ofrks (split form the previous step to 
        reduce quota) and save at active_2019_atleast_100_gitprop.csv
        4. Upload active_2019_atleast_200_gitprop.csv to BigQuery
        5. Run identify_redundant_repositories.sql in BigQuery to find non fork duplicated repositories, 
        download joint_commits.csv
        6. Run remove_redundent_repositories to remove redundency by commits and by name, get repos_2019
        7. Upload repos_2019 to BigQuery
        8. Run create_repos_commits in BigQuery
        9. Generate bq_corrective using the commit_model_type (in lang rerpository). Make sure to maark in the 
        comment the current commit_model_type commit hash so tracing the versions will be easy.
        10. Run bq_corrective on BigQuery
        11. Run repo_properties on BigQuery
        12. Run repo_utils.py to generate repos_full
        13. Upload repos_full to Bigquery
        14. Run create_repos_view on BigQuery
    """

    # Get number of repositories
    run_describe_repos()

    # Negative CCP analysis
    # run get_negative_ccp_commit_samples on BigQuery and downloand negative_ccp_commit_samples.csv
    run_English_analysis()

    build_repo_ccp_dist()

    run_star_analysis()

    # Longlivity analysis.
    # Note that it is done on 2018 repositories, not 2019.
    # Upload repos_full_2018.csv to BigQuery
    # File is taken from https://github.com/evidencebp/Which-Refactoring-Reduces-Bug-Rate (repos_full.csv)
    # Run at BigQuery compute_longevity.sql
    # Download the output as longlivity_2018
    run_analyze_longlivity()

    # File and programming language
    # run compute_repo_extension
    # It will built tables
    # repo_programming_file_size_99     (downlaod as a file to data folder)
    # repo_programming_file_size_by_extension_99 (downlaod as a file to data folder)
    # repo_programming_file_size_with_major_extension99 (downlaod as a file to data folder)
    run_ccp_cdf_per_language()
    run_compute_lang_anova()

    # Length
    run_length_per_lang_figure()
    run_file_size_analysis()

    # Run productivity_twins.sql on bigquery
    run_speed_consistency()
    run_file_length_per_language()

    # Churn
    # On bigquery run churn.sql and download invovled_developers_churn.csv, developer_on_boarding.ccp
    run_churn_analysis()
    run_churn_ccp_cochange()

    run_onboarding_ccp_cochange()

    # Age
    # Run repo_age.sql at BigQuery and get ccp_by_age.csv
    # TODO - run analyze_file_by_lang