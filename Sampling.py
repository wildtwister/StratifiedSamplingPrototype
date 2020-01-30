import random
import pprint

StrataDict = dict()
tuple_counter = 0


def generate_tuple():
    randon_names = ["Mary", "James", "Gary", "Suzy", "Nick"]
    new_tuple = {"key": random.choice(randon_names), "value": random.randrange(0, 20)/2}
    return new_tuple


def search_for_key(cur_tuple, strata_dict):
    for key in strata_dict.keys():
        if key == cur_tuple['key']:
            return True
    return False


def initialize_stratum():
    stratum = dict()
    stratum['mean'] = 0.0
    stratum['variance'] = 0.0
    stratum['proportion'] = 0.0
    stratum['error'] = 0.0
    stratum['gamma'] = 0.0
    stratum['tuples'] = []
    return stratum


def compute_mean_proportion_variance_gamma(numOfTuples, strata_dict):
    total_gamma = 0
    for stratum in strata_dict.values():
        min_value = 21
        max_value = -1
        stratum_val_sum = 0
        for cur_tuple in stratum['tuples']:
            stratum_val_sum += cur_tuple['value']
            if cur_tuple['value'] > max_value:
                max_value = cur_tuple['value']

            if cur_tuple['value'] < min_value:
                min_value = cur_tuple['value']

        stratum['mean'] = round(stratum_val_sum/len(stratum['tuples']), 2)
        stratum['variance'] = round(max_value - min_value, 2)
        stratum['proportion'] = round(len(stratum['tuples'])/numOfTuples, 2)
        stratum['gamma'] =  0 if stratum['mean']==0 else round(stratum['variance']/stratum['mean'], 2)  # gamma for weight 1
        total_gamma += stratum['gamma']
    print("Total gamma is : ", total_gamma)


# Main Function
for x in range(0, 10):
    cur_tuple = generate_tuple()
    tuple_counter += 1

    if not search_for_key(cur_tuple, StrataDict):
        StrataDict[cur_tuple['key']] = initialize_stratum()

    StrataDict[cur_tuple['key']]['tuples'].append(cur_tuple)


compute_mean_proportion_variance_gamma(tuple_counter, StrataDict)
pprint.PrettyPrinter().pprint(StrataDict)


