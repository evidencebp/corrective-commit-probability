import pandas as pd
import os
from configuration import DATA_PATH, REPOSITORIES_FILE

def analyze_language_identification_difference():

    not_exactly_programming_languge = ['HTML', 'TeX', 'TSQL', 'Makefile', 'Vim script', 'Rich Text Format', 'CSS']
    df = pd.read_csv(os.path.join(DATA_PATH, REPOSITORIES_FILE))
    in_range_identification = len(df[(df.y2019_ccp > 0)
                                     & (df.y2019_ccp < 1)
                                     & (df.language.isna())])/len(df[(df.y2019_ccp > 0) & (df.y2019_ccp < 1)])
    bellow_range_identification = len(df[(df.y2019_ccp < 0) & (df.language.isna())])/len(df[(df.y2019_ccp < 0)])


    print("in_range_identification", in_range_identification)
    print("bellow_range_identification", bellow_range_identification)
    print("below over in", bellow_range_identification/in_range_identification)

    in_range_not_exactly = len(df[(df.y2019_ccp > 0)
                                     & (df.y2019_ccp < 1)
                                     & (df.language.isin(not_exactly_programming_languge))])/len(df[(df.y2019_ccp > 0)
                                                                                                    & (df.y2019_ccp < 1)])
    bellow_range_not_exactly = len(df[(df.y2019_ccp < 0) & (df.language.isin(not_exactly_programming_languge))])/len(df[(df.y2019_ccp < 0)])


    print("in_range_not_exactly", in_range_not_exactly)
    print("bellow_range_not_exactly", bellow_range_not_exactly)
    print("below over in", bellow_range_not_exactly/in_range_not_exactly)

    return df

if __name__ == '__main__':
    df = analyze_language_identification_difference()
