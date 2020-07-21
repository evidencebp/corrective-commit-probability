from repo_utils import get_valid_repos

def developer_num_analysis():
    trep = get_valid_repos()


    print("Authors & ccp correlation" , trep.corr()['authors']['y2019_ccp'])
    print("CCP for the first num of developers")
    print(trep.groupby(['authors'], as_index=False).agg({'repo_name' : 'count', 'y2019_ccp' : 'mean'})[:20])
    print(trep.authors.describe())
    q25 = trep.authors.quantile(0.25)
    print("q25", q25)
    print(trep[(trep.authors < q25)].agg({'repo_name' : 'count', 'y2019_ccp' : 'mean'}))

    q75 = trep.authors.quantile(0.75)
    print("q75", q75)
    print(trep[(trep.authors> q25) & (trep.authors < q75)].agg({'repo_name' : 'count', 'y2019_ccp' : 'mean'}))

    print("above q50")
    print(trep[(trep.authors > q75)].agg({'repo_name' : 'count', 'y2019_ccp' : 'mean'}))

    q99 = trep.authors.quantile(0.99)
    print("q99", q99)
    print(trep[(trep.authors > q99)].agg({'repo_name' : 'count', 'y2019_ccp' : 'mean'}))



if __name__ == '__main__':
    developer_num_analysis()
