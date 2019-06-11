import numpy as np
import os

proc_list = ['Alpha-investing','LOND', 'LORD++', 'SAFFRON','ADDIS', 
             'LORDasync', 'SAFFRONasync','ADDISasync', 'D-LORD', 'Storey-BH', 'D-StBH']


def saveres(direc, filename, mat, ext = 'dat', verbose = True):
    filename = "%s.%s" % (filename, ext)
    if not os.path.exists(direc):
        os.makedirs(direc)
    savepath = os.path.join(direc, filename)
    np.savetxt(savepath, mat, fmt='%.3e', delimiter ='\t')
    if verbose:
        print("Saving results to %s" % savepath)
    
def str2list(string, type = 'int'):
    str_arr =  string.split(',')
    if type == 'int':
        str_list = [int(char) for char in str_arr]
    elif type == 'float':
        str_list = [float(char) for char in str_arr]
    return str_list

def list2str(lists):
    string = ''
    for i in lists:
        string = string + str(i)
    return string 

def getCom(seq): 
    combinations = list() 
    for i in range(0,len(seq)): 
        for j in range(0,len(seq)): 
            combinations.append([seq[i],seq[j]]) 
    return combinations
