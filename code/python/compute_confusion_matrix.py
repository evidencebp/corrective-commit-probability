import os
import pandas as pd

from configuration import LANG_DATA_PATH
from confusion_matrix import ConfusionMatrix
from commit_type_model import classifiy_commits_df

TEST_FILE = 'commits_updated5.csv'
VALIDATION_FILE = 'model_validation_samples.csv'

def print_confusion_matrix(labels_file
                           , classifier
                           , concept
                           , count
                           , title=None
                           , Sampling=None):
    df = pd.read_csv(labels_file
                        , encoding = "ISO-8859-1")
    # In case that some sampling methods are used,
    if  Sampling:
        df = df[df.Sampling == Sampling]
    df = classifiy_commits_df(df)
    bug_g = df.groupby([classifier, concept], as_index=False).agg({count: 'count'})
    bug_cm = ConfusionMatrix(g_df=bug_g
                             , classifier=classifier
                             , concept=concept, count=count)
    bug_cm.to_latex(title)

    return bug_cm

def print_cm_stat(cm
                  , digits=1):
    print(r"\begin{itemize}")
    print(r"    \item Accuracy(model is correct):"
          , round(100*cm.accuracy(), digits), r"\%")
    print(r"    \item Precision (ratio of hits that are indeed positives):"
          , round(100*cm.precision(), digits), r"\%")
    print(r"    \item Precision lift '($\frac{precision}{positive\ rate}-1$)':"
          , round(100*cm.precision_lift(), digits), r"\%")
    print(r"    \item Hit rate(ratio of commits identified by model as corrective):"
          , round(100*cm.hit_rate(), digits), r"\%")
    print(r"    \item Positive rate(real corrective commit rate):"
          , round(100*cm.positive_rate(), digits), r"\%")
    print(r"    \item Recall(positives that were also hits):"
          , round(100*cm.recall(), digits), r"\%")
    print(r"    \item Fpr(False Positive Rate, negatives that are hits by mistake):"
          , round(100*cm.fpr(), digits),r"\%")
    print(r"\end{itemize}")


def print_ccp_on_test():
    return print_confusion_matrix(os.path.join(LANG_DATA_PATH, TEST_FILE)
                           , 'corrective_pred'
                           , 'Is_Corrective'
                           , 'commit'
                           , r"\label{tab:test-cm} Confusion matrix of model on test data set"
                           , 'Random')


def print_ccp_on_validation():
    return print_confusion_matrix(os.path.join(LANG_DATA_PATH, VALIDATION_FILE)
                           , 'corrective_pred'
                           , 'Is_Corrective'
                           , 'commit'
                           , r"\label{tab:MLE-validation-cm} Confusion matrix of model on validation data set")


def run_compute_confusion_matrix():
    print("************* TEST *************")
    print()
    bugs_cm = print_ccp_on_test()
    print()
    print_cm_stat(bugs_cm)

    print("************* Validation *************")
    print()
    bugs_cm = print_ccp_on_validation()
    print()
    print_cm_stat(bugs_cm)

if __name__ == '__main__':
    run_compute_confusion_matrix()