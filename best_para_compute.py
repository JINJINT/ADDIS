# Import Python libraries
import numpy as np
from datetime import datetime
np.set_printoptions(precision = 4)
import os
import scipy.optimize as optim
from scipy.stats import norm
from scipy.stats import bernoulli

# import FDR methods
from SAFFRON_discard_batch import *

# Import utilities
from generatePvalue import *
from toimport import *
from generateHPY import *

from pathos.multiprocessing import ProcessingPool as Pool
 
################ Study the influence of hyper-parameters on power  ####################

def best_para(NUMRUN, NUMHYP, muN, muA, alpha0, pi, step = 0.1, rndseed = 0):
    # compute power of ADDIS with vaired tau and lbd with single pi   
    
    dir_name = './dat'
    filename = 'TRADE_OFF_MN%.1f_MA%.1f_NH%d_NR%d_step%.2f_pi%.1f' % (muN, muA, NUMHYP, NUMRUN, step, pi)

    lbd_list = np.arange(step, 1, step)
    tau_list = np.arange(step, 1, step)

    TDR_avg = np.zeros([len(lbd_list),len(tau_list)])
    TDR_std = np.zeros([len(lbd_list),len(tau_list)])

    for i, tau in enumerate(tau_list):
        for j, lbd in enumerate(lbd_list):        
            
            TDR_vec = np.zeros(NUMRUN)  
            
            def single(l):

                # Some random seed
                if (rndseed == 1):
                    rndsd = l+50
                else:
                    rndsd = None
                            
                Hypo = get_hyp(pi, NUMHYP)
                Hypo = Hypo.astype(int)
                num_alt = np.sum(Hypo)

                muA_vec = np.ones(NUMHYP)*muA
                this_exp = rowexp_new_batch(NUMHYP, 1, Hypo, muN, muA_vec)
                this_exp.gauss_two_mix(1, rndsd)

                proc = SAFFRON_discard_proc_batch(alpha0, NUMHYP, lbd, tau, 1.6)
                rej = proc.run_fdr(this_exp.pvec)

                #%%%%%%%%%%  Save results %%%%%%%%%%%%%%
                correj_singlerun = np.array(rej * np.array(Hypo))
                TDR = np.true_divide(np.sum(correj_singlerun), num_alt)
                FDR = np.true_divide(np.sum(correj_singlerun), num_alt)

                return TDR

            with Pool() as p:
                TDR_vec = p.map(single, range(NUMRUN))
                p.close()
                p.join()
                p.terminate()   
                p.restart()      

            TDR_avg[i,j] = np.average(TDR_vec) 
            TDR_std[i,j] = np.true_divide(np.std(TDR_vec), np.sqrt(NUMRUN)) 
            print("finished the calculation for computing the power with mu_N %.2f and mu_A %.2f, and lbd %.3f and tau %.3f " %(muN, muA, lbd, tau))


    data = np.r_[TDR_avg, TDR_std]
    saveres(dir_name, filename, data)








