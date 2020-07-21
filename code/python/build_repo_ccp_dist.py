
"""
Compute the CCP distribution and analyze it.
"""
import os
import pandas as pd

from configuration import DATA_PATH, REPOSITORIES_FILE
from positives_mle import ccp_estimator
from repo_utils import get_valid_repos, get_non_fork_repos

def build_repo_ccp_dist():

    rep = get_non_fork_repos()
    trep = get_valid_repos()
    rep = rep.sort_values(['y2019_hit_rate'], ascending=False)

    trep = trep.sort_values(['y2019_hit_rate'], ascending=False)


    rep.groupby(['y2019_hit_rate_rnd']).agg({'repo_name': 'count'})
    g = rep.groupby(['y2019_hit_rate_rnd']).agg({'repo_name': 'count'})

    num_of_repos = len(rep)
    num_of_repos_in_range = len(trep)
    print()
    print(r"\begin{table}\centering")
    print(r"\caption{\label{tab:CCP-distrib}")
    print(r"CCP distribution in active GitHub projects}")
    print(r"\begin {tabular}{ | c | c | c | c | c |}")
    print(r"\hline")
    print(r"& \multicolumn {2} {c |} {Full data set} & \multicolumn {2} {c |} {CCP $\ in [0, 1]$}\\ ")
    print(r"& \multicolumn {2} {c |} {(", f'{num_of_repos:,}' ,"projects)} &\multicolumn")
    print(r"{2}{c |}{(", f'{num_of_repos_in_range:,}',  r"projects)}\\ \cline {2 - 5}")


    print(r"Percentile &  Hit rate & CCP est. & Hit rate & CCP est.  \\ \hline")
    vals = [1.0*i/10 for i in range(1, 10)]
    vals.append(0.95)
    #vals.append(0.99)

    for i in vals:
       print(str(int(100 * i)) + " & "
        ,str(round(rep.iloc[int(i * len(rep))].y2019_hit_rate, 2))
        ," & " + str(round(rep.iloc[int(i * len(rep))].y2019_ccp, 2))
        , " & " + str(round(trep.iloc[int(i * len(trep))].y2019_hit_rate, 2))
        , " & " + str(round(trep.iloc[int(i * len(trep))].y2019_ccp, 2)) + " \\\\ \hline")

    print(r"\end{tabular}")
    print(r"\end{table}")
    print()

    # For manual verification
    # print (rep.y2019_hit_rate_rnd.value_counts(normalize=True).sort_index().cumsum())
    # print(trep.y2019_hit_rate_rnd.value_counts(normalize=True).sort_index().cumsum())

    print("correlation between years")
    print("commits", trep.corr()[u'y2019_commits'][u'y2018_commits'])
    print("hits", trep.corr()[u'y2019_hits'][u'y2018_hits'])
    print("hit ratio", trep.corr()[u'y2019_hit_rate'][u'y2018_hit_rate'])
    print("ccp", trep.corr()[u'y2019_ccp'][u'y2018_ccp'])

    print()
    y2019_hit_rate_median = trep.iloc[int(len(trep) / 2)].y2019_hit_rate
    #print("y2018_hit_rate_median", y2018_hit_rate_median)
    trep['high_half_2019'] = trep.y2019_hit_rate.map(lambda x: x > y2019_hit_rate_median)
    trep['high_half_2018'] = trep.y2018_hit_rate.map(lambda x: x > y2019_hit_rate_median)
    g = trep.groupby(['high_half_2019', 'high_half_2018'], as_index=False).agg({'repo_name': 'count'})
    g = g.rename(columns={'repo_name': 'cnt'})
    print("stable half", 1.0 * g[((g.high_half_2019 == False) & (g.high_half_2018 == False)) | (
                (g.high_half_2019 == True) & (g.high_half_2018 == True))].cnt.sum() / len(trep))


    y2019_hit_rate_10p = trep.iloc[int(90 * len(trep) / 100)].y2019_hit_rate
    #print("y2018_hit_rate_10p", y2018_hit_rate_10p)
    trep['high_10_2018'] = trep.y2018_hit_rate.map(lambda x: x < y2019_hit_rate_10p)
    trep['high_10_2019'] = trep.y2019_hit_rate.map(lambda x: x < y2019_hit_rate_10p)
    g = trep.groupby(['high_10_2018', 'high_10_2019'], as_index=False).agg({'repo_name': 'count'})
    g = g.rename(columns={'repo_name': 'cnt'})
    print("stable 10", 1.0 * g[((g.high_10_2018 == False) & (g.high_10_2019 == False)) | (
                (g.high_10_2018 == True) & (g.high_10_2019 == True))].cnt.sum() / len(trep))

    print("stay in top", 1.0 * g[((g.high_10_2018 == True) & (g.high_10_2019 == True))].iloc[0].cnt /
          g[g.high_10_2018 == True].cnt.sum())
    print("get to top", 1.0 * g[((g.high_10_2018 == False) & (g.high_10_2019 == True))].iloc[0].cnt /
          g[g.high_10_2018 == False].cnt.sum())

    trep['cpp_abs_diff'] = trep.apply(lambda x: round(abs(x.y2019_ccp - x.y2018_ccp), 2), axis=1)
    trep.cpp_abs_diff.value_counts(normalize=True).sort_index().cumsum()
    print("abs difference mean", trep.cpp_abs_diff.mean())

    print()
    trep['cpp_diff'] = trep.apply(lambda x: round(x.y2019_ccp - x.y2018_ccp, 2), axis=1)
    trep.cpp_diff.value_counts(normalize=True).sort_index().cumsum()
    print("difference mean", trep.cpp_diff.mean())
    print("2018 average ccp ratio", trep.y2018_hits.sum() * 1.0 / trep.y2018_commits.sum())
    print("2019 average ccp ratio", trep.y2019_hits.sum() * 1.0 / trep.y2019_commits.sum())

    print()
    print("CCP ratios")
    y2019_ccp_90p = trep.iloc[int(90 * len(trep) / 100)].y2019_ccp
    y2019_ccp_50p = trep.iloc[int(50 * len(trep) / 100)].y2019_ccp
    y2019_ccp_10p = trep.iloc[int(10 * len(trep) / 100)].y2019_ccp
    print("2019 top 90 CCP ", round(y2019_ccp_90p,2))
    print("2019 top 50 CCP ", round(y2019_ccp_50p,2))
    print("2019 top 10 CCP (worse) ", round(y2019_ccp_10p,2))
    print("2019 top 50 CCP over top 90", round(y2019_ccp_50p/y2019_ccp_90p,2))
    print("2019 top 10 CCP over top 90", round(y2019_ccp_10p/y2019_ccp_90p,2))


    # Updating the file with the CCP values
    #rep.to_csv(repo_file)


if __name__ == '__main__':
    build_repo_ccp_dist()