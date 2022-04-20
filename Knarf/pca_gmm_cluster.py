#!/usr/bin/python3.4

#  gmm_cluster.py  v0.1 E W Fulp  2/21/2022
#
#  the hope is to cluster the profile files...
#  and PCA as a special gift for you, no purchase necessary
#  just pay an addition shipping fee
#
#  ACHTUNG: groups are hard coded
#
#  useage:
#     ./gmm_cluster.py -r "ls*.prf" "cat*.prf"
#

import sys
# import getopt
import argparse
import copy
import glob
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn import decomposition


import os


def generate_pca_data(df, filename):
    scaler = StandardScaler()

    # let's make a copy since we'll mangle the df in the process
    copy_df = df.copy()

    # col_list = ['rate Access Granted', 'rate Invalid Access Level']
    col_list = [col for col in copy_df.columns if 'f' in col]

    # normalize the metrics
    scaled_df = scaler.fit_transform(copy_df[col_list]) # df[col_list].copy()
    # scaled_df = df[col_list].copy()

    pca = PCA(n_components = 2)  # Reduce to k = 2 dimensions
    princ_comp = pca.fit_transform(scaled_df)
    princ_df = pd.DataFrame(data = princ_comp, columns = ['pc_1', 'pc_2'])

    # calculate variance ratios
    variance = pca.explained_variance_ratio_
    var = np.cumsum(np.round(pca.explained_variance_ratio_, decimals = 3)*100)

    copy_df = copy_df.reset_index(drop = True)

    pca_df = princ_df.copy()

    pca_df['group'] = copy_df['group']

    print(pca_df['group'])

    # camp_list = pca_df.camp.unique()

    color_list = "rbgycmkw"

    for camp_value, color in zip(camp_list, color_list):
        camp_indices = pca_df['camp'] == camp_value
        plt.scatter(pca_df.loc[camp_indices, 'pc_1'], pca_df.loc[camp_indices, 'pc_2'], c = color, s = 50);


    plt.legend(camp_list)

    # plt.show()
    plt.save('testing.svg')

    # save to file
    pca_df.to_csv(filename, sep = ' ') # , index = False)


def gmm_cluster_ari(df, num_clusters):
    col_list = [col for col in df.columns if 'f' in col]
    model = GaussianMixture(covariance_type = 'spherical', random_state = 0, n_components = num_clusters).fit(df[col_list])
    labels = model.predict(df[col_list]).tolist()

    df['label'] = labels

    print('GMM %i cluster ARI: %f7'%(num_clusters, adjusted_rand_score(df['group'], labels)))

    cluster_groups = df.groupby('label')

    for group, data in cluster_groups:
        cmd_list = data['cmd'].to_string().split('\n')
        # remove the row number and following spaces, leaving just the campain name
        cmd_list = [str.split(None, 1)[1] for str in cmd_list]
        print('cluster %s:%s \n'%(group, list_to_string(cmd_list)))


def total_instr(row):
    col_list = [col for col in row.columns if 'f' in col]
    return sum(row.loc[col_list])


def list_to_string(lst):
    return '[' + ', '.join(lst) + ']'


def main(argv):

    prog_name = os.path.basename(__file__)
    # get command line arguments
    first_regex = ''
    sec_regex = ''

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', dest = 'regex', nargs = '+', required = True, help = 'regular expressions for each group of experiment files')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    # process every experiment file (defined by regex's) to find all unique instructions
    instr_map = {}  # map of instructions and their index (feature number)
    num_uniq = 0    # used to set the feature number (and array index) of each unique instruction

    # for each regular expression defining a set of experiments
    for regex in args.regex:
        # we'll assume that the experiment files are local, are you local?
        path = './' + regex
        # for exvery file that matches this regex
        for filename in glob.glob(path):
            file = open(filename)
            line = (file.readline()).rstrip()
            while line:
                # remove any empty strings from the line, get second item (the instruction)
                instr = list(filter(None, line.split(' ')))[1]
                # let's make certain the instruction is not already in the map...
                if not instr in instr_map:
                    instr_map[instr] = num_uniq
                    num_uniq += 1
                line = (file.readline()).rstrip()
            file.close()
            # let's make certain every key in the map has a unique value (feature number)
            assert(len(instr_map) == len(set(instr_map.values())))
        # print "instructions", instr_map

    # print(instr_map)
    # now that we have our instruction map (instr -> index) lets determine the feature space per file
    exper = []  # list of all experiment features (list of lists)
    cmd_list = []  # list of the commands
    arg_list = []  # list of the commands args

    # for each regular expression defining a set of experiments
    for regex in args.regex:
        path = './' + regex
        for filename in glob.glob(path):
            cmd_name = filename.split('_')[0][2:] + '_' + filename.split('_')[1][:]
            cmd_arg = filename.split('_')[1][:]
            # initiallize all feaures to zero
            temp = [0]*len(instr_map)
            file = open(filename)
            line = (file.readline()).rstrip()
            while line:
                count = list(filter(None, line.split(' ')))[0]
                instr = list(filter(None, line.split(' ')))[1]
                temp[instr_map[instr]] = count
                line = (file.readline()).rstrip()
            file.close()
            cmd_list.append(cmd_name)
            arg_list.append(cmd_arg)
            exper.append(temp)


    # print("exper", exper)
    # print("cmd_list", cmd_list)
    # print("arg_list", cmd_list)

    # let's figure out what commands are numbers and which are strings
    num_arg_lst = []
    num_args = []
    str_args = []
    for cmd in cmd_list:
        arg_parts = list(filter(None, cmd.split('_')))
        if arg_parts[1].isnumeric():
            num_args.append(arg_parts[1])
        else:
            str_args.append(arg_parts[1])
    
    print('num args used %s'%(num_args))
    print('str args used %s'%(str_args))

    # let's make this a panda dataframe

    df = pd.DataFrame(exper)
    df = df.astype(int)

    df.columns = ['f' + str(i) for i in range(0, len(instr_map))]
    df['cmd'] = cmd_list
    df['arg'] = arg_list

    print('commands are %s '%(df.cmd.unique()))

    # let's add column identifying the groups of commands
    df['group'] = 'none'

    # let's assign 'arg' column based on if the argument was a str or num
    """ 
    df.loc[(df['arg'].isin(num_args)), 'group'] = 'num'
    df.loc[(df['arg'].isin(str_args)), 'group'] = 'str'
    """
    for ind in df.index:
        # print(type(df['arg'][ind]))
        # print(type(df['group'][ind]))
        df['group'][ind] = str(int(df['arg'][ind]) % 4)

    # print(df)

    col_list = [col for col in df.columns if 'f' in col]

    # I suppose we can cluster now...

    # scaler = StandardScaler()
    scaler = MinMaxScaler()
    df[col_list] = scaler.fit_transform(df[col_list])

    print(df)

    cluster_list = np.arange(2, 5) # <-- these are the numbes we are trying to find! >:{}
    models = [GaussianMixture(covariance_type = 'spherical', random_state = 0, n_components = n).fit(df[col_list]) for n in cluster_list]
    scores = [silhouette_score(df[col_list], model.predict(df[col_list]).tolist(), sample_size = 50000) for model in models]

    silhouette_best_clusters = models[scores.index(max(scores))].n_components

    # print('silhoutte scores %s '%(scores))
    for num, score in zip(cluster_list, scores):
        print('(n:%i s:%f)'%(num, score), end = ', ')
    print('\nGMM best number of clusters (silhouette) %i (%f7)'%(silhouette_best_clusters, max(scores)))

    best_clusters = silhouette_best_clusters
    print('best clusters (n = %i) results '%(best_clusters))
    gmm_cluster_ari(df, best_clusters)

    generate_pca_data(df, 'pca_n_2.txt')

    # best_clusters = silhouette_best_clusters
    # best_clusters = 2
    # print('if we demand 2 clusters... ')
    # gmm_cluster_ari(df, best_clusters)

    return


if __name__ == "__main__":
   main(sys.argv[1:])

