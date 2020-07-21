"""
Using the bootstrap model in order to compare resulting models.
"""
import datetime
import os
import pandas as pd

from configuration import DATA_PATH, LANG_DATA_PATH

probability_bounds = [0, 1]
valid_domain_bounds = [0.042, 0.84]
main_percentiles_bounds = [0.06, 0.39]
points_of_difference = sorted(probability_bounds + valid_domain_bounds + main_percentiles_bounds)


# TODO - compute new predictions using classifier
# TODO - use cm class for computation
def extract_model_parameters(df
                            , concept = 'Is_Corrective'
                            , classifier = 'bq_classification'):
    # positives
    positives = len(df[df[concept]== True])

    # true positives
    true_positives = len(df[(df[concept] == True) & (df[classifier] == True)])
    # Recall = true positives/positives
    recall = 1.0*true_positives/positives

    # negatives
    negatives = len(df[df[concept]== False])

    # false positives
    false_positives = len(df[(df[concept] == False) & (df[classifier] == True)])

    # Fpr = false positives/negatives
    fpr = 1.0*false_positives/negatives

    return recall, fpr

def get_model(recall, fpr):
    f = lambda x: (x-fpr)/(recall -fpr)
    return f

def bootstrap_models(df
                    , rounds
                    , sample_size):
    # Update the values when needed
    # 0,1 - probability bounds
    # fpr, recall - valid domain bounds
    # p10, p90 - main CCP distribution bounds
    bootstrap_results = []
    for i in range(rounds):
        # Get first model parameters
        s1 = df.sample(sample_size, replace=True)
        recall1, fpr1 = extract_model_parameters(s1)
        m1 = get_model(recall1, fpr1)
        # Get second model parameters
        s2 = df.sample(sample_size, replace=True)
        recall2, fpr2 = extract_model_parameters(s2)
        m2 = get_model(recall2, fpr2)

        differences = []
        for i in points_of_difference:
            differences.append(m1(i)-m2(i))

        # Find difference in given points
        bootstrap_results.append(differences)

        if (i %  100 == 0):
            print( "finished " + str(i) , datetime.datetime.now())

    results_df = pd.DataFrame(bootstrap_results
                                , columns = ['col_' + str(i) for i in points_of_difference])
    return results_df


def run_bootstrap_models():
    df = pd.read_csv(os.path.join(LANG_DATA_PATH
                                    , 'model_validation_samples.csv')
                      , engine='python')
    df = df[(df.Comment != 'duplicated') & (df.Is_Corrective.isin([True,False]))]


    sample_size = len(df)
    rounds = 10000
    results_df = bootstrap_models(df
                                    , rounds
                                    , sample_size)

    results_df.to_csv(os.path.join(DATA_PATH
                        ,'models_bootstrap.csv')
                      , index=False)

    for i in results_df.columns:
        print( "0.0 precentile", i, results_df.sort_values(i).iloc[0][i])
        print( "25 precentile", i, results_df.sort_values(i).iloc[int(0.025*rounds)][i])
        print( "97.5 precentile", i, results_df.sort_values(i).iloc[int(0.975*rounds)][i])
        print( "100 precentile", i, results_df.sort_values(i).iloc[rounds-1][i])

    print()
    print("main differences")
    print("Probability bounds - max "
          , max([results_df.sort_values("col_" + str(i)).iloc[rounds-1]["col_" + str(i)] for i in probability_bounds]))
    print("Probability bounds - 95% "
          , max([results_df.sort_values("col_" + str(i)).iloc[int(0.975*rounds)]["col_" + str(i)] for i in probability_bounds] +
                [results_df.sort_values("col_" + str(i)).iloc[int(0.025*rounds)]["col_" + str(i)] for i in probability_bounds]))

    print("Valid domain bounds bounds - max "
          , max([results_df.sort_values("col_" + str(i)).iloc[rounds-1]["col_" + str(i)] for i in valid_domain_bounds]))
    print("Valid domain bounds - 95% "
          , max([results_df.sort_values("col_" + str(i)).iloc[int(0.975*rounds)]["col_" + str(i)] for i in valid_domain_bounds] +
                [results_df.sort_values("col_" + str(i)).iloc[int(0.025*rounds)]["col_" + str(i)] for i in valid_domain_bounds]))

    print("Main percentiles bounds bounds bounds - max "
          , max([results_df.sort_values("col_" + str(i)).iloc[rounds-1]["col_" + str(i)] for i in main_percentiles_bounds]))
    print("Main percentiles bounds - 95% "
          , max([results_df.sort_values("col_" + str(i)).iloc[int(0.975*rounds)]["col_" + str(i)] for i in main_percentiles_bounds] +
                [results_df.sort_values("col_" + str(i)).iloc[int(0.025*rounds)]["col_" + str(i)] for i in main_percentiles_bounds]))


if __name__ == '__main__':
    run_bootstrap_models()