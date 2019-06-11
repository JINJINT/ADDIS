### Import Python libraries
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


def plot_results(FDRrange, pirange, muNrange, muArange, sigma, NUMHYP, num_runs):

    plot_dirname = './plots'

    for mu_A in muArange:

        legends_list = np.array(proc_list).take([t-1 for t in FDRrange])
        label_list =[FDRlegend for FDRlegend in legends_list]
        FDRstr = list2str(FDRrange)

        for n, mu_N in enumerate(muNrange):
            ind = 0
            TDR_av = []
            TDR_std = []
            FDR_av = []
            FDR_std = []
            for FDR in FDRrange: 
                filename_pre = 'MN%.1f_MA%.1f_Si%.1f_FDR%d_NH%d' % (mu_N, mu_A, sigma, FDR, NUMHYP)
                all_filenames = [filename for filename in os.listdir('./dat') if filename.startswith(filename_pre)]

                if all_filenames == []:
                    print("No file found!")
                    print(filename_pre)
                    sys.exit()

                # Get different pis
                pos_PM_start = [all_filenames[i].index('PM') for i in range(len(all_filenames))]
                pos_PM_end = [all_filenames[i].index('_NR') for i in range(len(all_filenames))]
                PM_vec = [float(all_filenames[i][pos_PM_start[i] + 2:pos_PM_end[i]]) for i in range(len(all_filenames))]

                order = np.argsort(PM_vec)
                PM_list = sorted(set(np.array(PM_vec)[order]))

                # Initialize result matrices
                TDR_av.append(np.zeros([1, len(PM_list)]))
                TDR_std.append(np.zeros([1, len(PM_list)]))
                FDR_av.append(np.zeros([1, len(PM_list)]))
                FDR_std.append(np.zeros([1, len(PM_list)]))
                TDR_vec = np.zeros(len(PM_list))
                FDR_vec = np.zeros(len(PM_list))
                TDR_vec_std = np.zeros(len(PM_list))
                FDR_vec_std = np.zeros(len(PM_list))

                # Merge everything with the same NA and NH
                for k, PM in enumerate(PM_list):
                    indices = np.where(np.array(PM_vec) == PM)[0]
                    result_mat = []
                    # Load resultmats and append
                    for j, idx in enumerate(indices):
                        result_mat_cache = np.loadtxt('./dat/%s' % all_filenames[idx])
                        result_mat_cache = result_mat_cache[-2:,0:num_runs]
                        if (j == 0):
                            result_mat = result_mat_cache
                        else:
                            result_mat = np.c_[result_mat, result_mat_cache]

                    # Get first vector for TDR
                    TDR_vec[k] = np.average(result_mat[0])
                    TDR_vec_std[k] = np.true_divide(np.std(result_mat[0]),np.sqrt(num_runs))
                    # FDR
                    FDR_vec[k] = np.average(result_mat[1])
                    FDR_vec_std[k] = np.true_divide(np.std(result_mat[1]), np.sqrt(num_runs))
                TDR_av[ind] = [TDR_vec[k] for k in range(len(PM_list))]
                TDR_std[ind] = [TDR_vec_std[k] for k in range(len(PM_list))]
                FDR_av[ind] = [FDR_vec[k] for k in range(len(PM_list))]
                FDR_std[ind] = [FDR_vec_std[k] for k in range(len(PM_list))]
                ind = ind + 1

            # -------- PLOT ---------------
            xs = PM_list
            x_label = '$\pi_A$'


            ##### TDR/FDR vs pi #####

            filename = 'PowFDRvsPI_FDR%s_MN%.1f_MA%.1f_Si%.1f_NH%d' %  (FDRstr, mu_N, mu_A, sigma, NUMHYP)
            plot_errors_mat_both(xs, TDR_av, FDR_av, TDR_std, FDR_std, label_list, plot_dirname, filename, x_label, 'FDR / Power')



