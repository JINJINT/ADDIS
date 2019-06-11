import numpy as np
np.set_printoptions(precision = 4)
from generatePvalue import *
from toimport import *
from generateHPY import *
import sys


### Import utilities for plotting
from plotting import*
from generateHPY import*
from toimport import*


def plot_best(pi, muN, muA, step, NUMRUN, NUMHYP):

    plot_dirname = './plots' 

    lbd_list = np.round(np.arange(step, 1, step),2)
    tau_list = np.round(np.arange(step, 1, step),2)[::-1] # reverse the order for better visualization

    # load the emprirical power
    filename_pre = 'TRADE_OFF_MN%.1f_MA%.1f_NH%d_NR%d_step%.2f_pi%.1f' % (muN, muA, NUMHYP, NUMRUN, step, pi)
    all_filenames = [filename for filename in os.listdir('./dat') if filename.startswith(filename_pre)]

    if all_filenames == []:
        print("No file found!")
        print(filename_pre)
        sys.exit()

    result_mat = np.loadtxt('./dat/%s' % all_filenames[0])
    avg_mat = result_mat[:len(tau_list),:]
    avg_mat = avg_mat[::-1] # reverse the order for better visualization

    filenameexp = 'heatmap_tradeoff_MN%.1f_MA%.1f_NH%d_NR%d_step%.2f_pi%.1f' %  (muN, muA, NUMHYP, NUMRUN, step, pi)
   
    # the heatmap of empirical power
    heatmapplot("$\lambda$", "$\\tau$", avg_mat, plot_dirname, filenameexp, lbd_list, tau_list, 0.4, 0.8, "power") 


 