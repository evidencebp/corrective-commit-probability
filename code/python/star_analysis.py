import pandas as pd
from datetime import datetime

from feature_pair_analysis import pretty_print, pair_analysis_with_controls
from repo_utils import get_valid_repos
from remove_redundant_repositories import check_name_redundency

def do_stars_analysis(trep):

    #trep['active_6_months_later'] = trep.apply(
    #    lambda x: datetime.strptime(x.end_time[:10], '%d/%m/%Y') > datetime(2019,6,1), axis=1)
    trep['active_6_months_later'] = trep.apply(
        lambda x: datetime.strptime(x.end_time[:x.end_time.find(' ')], '%Y-%m-%d') > datetime(2019,6,1), axis=1)
    p99 =trep[(~trep.stargazers_count.isna())].sort_values('stargazers_count').iloc[
        int(0.99*len(trep[(~trep.stargazers_count.isna())]))].stargazers_count
    print("stars p99", p99)

    trep['stargazers_count_c99p'] = trep.stargazers_count.map(lambda x: p99 if x > p99 else x)

    p95 =trep[(~trep.stargazers_count.isna())].sort_values('stargazers_count').iloc[
        int(0.95*len(trep[(~trep.stargazers_count.isna())]))].stargazers_count
    print("stars p95", p95)

    trep['stargazers_count_c95p'] = trep.stargazers_count.map(lambda x: p95 if x > p95 else x)

    trep['capped_stargazers_per_contributors'] = trep.apply(lambda x: 0 if not x.contributors_count else 1.0*x.stargazers_count_c99p/x.contributors_count, axis=1)
    trep['at_least_star'] = trep.apply(lambda x: int(x.stargazers_count > 0), axis=1)

    print("authors 25% quantile", trep.authors.quantile(0.25))
    print("authors 75% quantile", trep.authors.quantile(0.75))
    print("Stars and authors Pearson correlation"
          , trep.corr()['stargazers_count']['authors'])
    trep['authors_group'] = trep.authors.map(
        lambda x: 'Few' if x < trep.authors.quantile(0.25) else 'Numerous' if x > trep.authors.quantile(0.75) else 'Intermediate')
    print(trep.groupby(['authors_group'], as_index=False).agg(
        {'repo_name' : 'count', 'y2018_ccp': 'mean', 'y2017_ccp': 'mean', 'y2016_ccp': 'mean'}))

    g = trep.groupby(['quality_group'], as_index=False).agg({'repo_name' : 'count'
                                                                , 'at_least_star' : 'mean'
                                                                , u'contributors_count' : 'mean'
                                                                , u'stargazers_count' : 'mean'
                                                                , u'stargazers_count_c99p' : 'mean'
                                                                , u'stargazers_count_c95p' : 'mean'
                                                                , u'capped_stargazers_per_contributors' : 'mean'
                                                                , 'active_6_months_later' : 'mean'})

    print("Quality group & Projects & Fraction starred & Stars (capped) & Contributors  & Stars per contributors & Active later\\\\ \\hline")
    for _, i in g.sort_values('quality_group', ascending=False).iterrows():
        print (i.quality_group , " & "
               ,i['repo_name'], " & "
               , round(i['at_least_star'] ,2), " & "
               , round(i.stargazers_count_c99p, 1), " & "
               , round(i.contributors_count, 1), " & ", round(i.capped_stargazers_per_contributors, 1), " & "
               , round(i.active_6_months_later,2) ," \\\\ \\hline")

    print("all quelity differences")
    print(g)

    print( "stars")
    print (trep.groupby('quality_group').agg({'stargazers_count' : 'mean'}))

    top_star_prob = 1.0*len(trep[(trep.quality_group == 'Top 10') & (trep.stargazers_count > 0)])/len(trep[(trep.quality_group == 'Top 10')])
    others_star_prob = 1.0*len(trep[(trep.quality_group == 'Others') & (trep.stargazers_count > 0)])/len(trep[(trep.quality_group == 'Others')])
    print ("top prob to a star", top_star_prob)
    print ("others prob to a star", others_star_prob)
    print ("prob to be stared lift ", top_star_prob/others_star_prob -1)

    print("size and quality")
    quality_size_group = trep.groupby(['authors_group','quality_group'], as_index=False).agg({'repo_name' : 'count'
                                                                #, 'at_least_star' : 'mean'
                                                                , u'contributors_count' : 'mean'
                                                                , u'stargazers_count' : 'mean'
                                                                , u'stargazers_count_c99p' : 'mean'
                                                                #, u'stargazers_count_c95p' : 'mean'
                                                                , u'capped_stargazers_per_contributors' : 'mean'
                                                                #, 'active_6_months_later' : 'mean'
                                                                                })
    print( quality_size_group)

    line = 1
    print("Size & Quality group & Projects &  Stars (capped) & Contributors  & Stars per contributors \\\\ \\hline")
    for _, i in quality_size_group.sort_values(['authors_group','quality_group'], ascending=[False, False]).iterrows():
        print (i['authors_group'], " & "
               ,i['quality_group'], " & "
               ,i['repo_name'], " & "
               , round(i.stargazers_count_c99p, 1), " & "
               , round(i.contributors_count, 1), " & "
               , round(i.capped_stargazers_per_contributors, 1)
               ," \\\\ "
               , "\\hline" if line % 2 == 0 else "\\cline{2-6}")
        line += 1

    pretty_print(pair_analysis_with_controls(trep
                  , 'quality_group'
                  , 'stargazers_count'
                  , metrics=None))

def Linus_rule():
    df = get_valid_repos()
    df = check_name_redundency(df)

    selected_users = ['google', 'facebook', 'apache', 'angular', 'kubernetes', 'tensorflow']
    many_stars_threshhold = df.stargazers_count.quantile(0.95)
    print("many_stars_threshold 95%", many_stars_threshhold)
    df['many_stars'] = df.stargazers_count.map(lambda x: x > many_stars_threshhold)

    for i in selected_users:
        print(i)
        g = df[df.user == i].groupby(['many_stars'], as_index=False).agg(
            {'y2019_ccp': 'mean', 'repo_name': 'count'})
        print(g)
        print("Many stars lift"
              , round(g[g.many_stars].iloc[0].y2019_ccp/ g[~g.many_stars].iloc[0].y2019_ccp -1.0, 2))

    df['selected_users_project'] = df.user.map(lambda x: x in selected_users)
    g = df.groupby(['selected_users_project'], as_index=False).agg(
            {'y2019_ccp': 'mean'
                , 'repo_name': 'count'
                , 'age' : 'mean'
                , 'authors' : 'mean'
                , 'stargazers_count' : 'mean'})
    print(g)
    for i in ['y2019_ccp', 'age', 'authors', 'stargazers_count']:
        print( str(i) +" users"
          , g[g.selected_users_project][i].iloc[0]
          , "others"
          , g[~g.selected_users_project][i].iloc[0]
          , "lift"
          , g[g.selected_users_project][i].iloc[0]/g[~g.selected_users_project][i].iloc[0] -1)

def run_star_analysis():
    trep = get_valid_repos()
    do_stars_analysis(trep)
    Linus_rule()

if __name__ == '__main__':
    #run_star_analysis()
    Linus_rule()