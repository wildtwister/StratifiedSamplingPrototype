#
#   Stratified Sampling in Python
#   Based on "Random Sampling for Group-By Queries" paper
#   by Nguyen et al
#   author: Panagiotis Savvaidis
#
#   Implementing Single Aggregate - Single GroupBy Algorithm
#
#   Tuples Generated: <name, value> using random builtin Python library (normal Distribution)
#   Tuples grouped by "name"
#
#
#


import random
import pprint
import math

StrataDict = dict()
tuple_counter = 0
M = 100
suzyIsNotGone = True


def generate_tuple(name=None):
    randon_names = ["Mary", "James", "Gary", "Suzy", "Nick", "Bella", "Ricky"]
    if name is None:
        new_tuple = {"key": random.choice(randon_names), "value": random.randrange(0, 20)/2}
    else:
        new_tuple = {"key": name, "value": random.randrange(0, 20)/2}

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
    stratum['Si'] = 0.0
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

        # gamma for weight 1
        # stratum['gamma'] = 0 if stratum['mean'] == 0 else round(stratum['variance']/stratum['mean'], 2)

        # gamma for weight equal to the proportion
        stratum['gamma'] = 0 if stratum['mean'] == 0 else round(math.sqrt(stratum['proportion'])*stratum['variance']/stratum['mean'], 2)

        total_gamma += stratum['gamma']

    print("Total gamma is : ", total_gamma)
    return total_gamma


def compute_sample_size(strata_dict, total_gamma):
    # Rules:
    # 1. At least 1 sample per stratum
    # 2. No more Samples than M
    max_sample_size = -1
    max_s_key = ''
    total_samples_assigned = 0

    # for each stratum, we compare the rounded
    for s_key, stratum in strata_dict.items():
        stratum['Si'] = round(M*stratum['gamma']/total_gamma)
        if stratum['Si'] == 0:
            stratum['Si'] += 1
        total_samples_assigned += stratum['Si']
        if stratum['Si'] > max_sample_size:
            max_s_key = s_key

    # The biggest sample
    # gains samples
    # if total samples assigned are less than the memory budget
    # and
    # loses samples
    # if total samples assigned are more than the memory budget
    if total_samples_assigned != M:
        difference = M - total_samples_assigned
        strata_dict[max_s_key]['Si'] += difference


def strata_pretty_print():
    pprint.PrettyPrinter().pprint(StrataDict)


def strata_sample_print():
    for s_key, stratum in StrataDict.items():
        print('For Stratum ' + s_key + '\n\tgamma is ', stratum['gamma'], '\n\tproportion is ', stratum['proportion'], ' \n\tsample size is ', stratum['Si'], '\n')


def generate_biased_tuple():
    if x < 200:
        cur_tuple = generate_tuple("Nick")
    elif x < 500:
        cur_tuple = generate_tuple("Mary")
    else:
        cur_tuple = generate_tuple()
    return cur_tuple


# Main Function

# generating 1000 tuples
for x in range(0, 1000):

    cur_tuple = generate_tuple()
    # there is also a generate_biased_tuple() method
    # that can be tuned by the user

    tuple_counter += 1

    # making buckets for tuples
    if not search_for_key(cur_tuple, StrataDict):
        StrataDict[cur_tuple['key']] = initialize_stratum()

    StrataDict[cur_tuple['key']]['tuples'].append(cur_tuple)


total_gamma = compute_mean_proportion_variance_gamma(tuple_counter, StrataDict)
compute_sample_size(StrataDict, total_gamma)
strata_sample_print()

