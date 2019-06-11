# Import Python libraries
import numpy as np
from datetime import datetime
np.set_printoptions(precision = 4)
import os
import scipy.optimize as optim
from scipy.stats import norm
from scipy.stats import bernoulli

# Import FDR procedures
from AlphaInvest_batch import *
from LOND_batch import *
from LORD_batch import *
from LORD_discard_batch import *
from LORD_async_batch import *

from SAFFRON_batch import *
from SAFFRON_discard_batch import *
from SAFFRON_async_batch import *
from SAFFRON_async_discard_batch import *

from Storey_batch import *
from Storey_discard_batch import *

# Import utilities
from generatePvalue import *
from toimport import *
from generateHPY import *
  
################ Running entire framework  ####################

def run_single(NUMRUN, NUMHYP, NUMDRAWS, muN, muA, pi, alpha0, FDR, sigma = 1, lbd = 0.5, tau = 0.5, verbose = False, TimeString = False, rndseed = 0, startfac = 0.5):
    # model choice 1: Gaussian mixture; 2: Beta alternatives
    
    if rndseed == 0:
        TimeString = True

    if TimeString:
        time_str = datetime.today().strftime("%m%d%y_%H%M")
    else:
        time_str = '0'

    ##------------ Generate hypotheses -------------## 

    Hypo = get_hyp(pi, NUMHYP)
    Hypo = Hypo.astype(int)
    num_alt = np.sum(Hypo)
       
    ##------------ Set file and dirnames -----------##
    dir_name = './dat'   
    filename = 'MN%.1f_MA%.1f_Si%.1f_FDR%d_NH%d_PM%.2f_NR%d_lbd%.4f_tau%.4f_%s' % (muN, muA, sigma, FDR, NUMHYP, pi, NUMRUN, lbd, tau, time_str)
    
    ##------------ Initialize result vectors and mats ------------- ##
    pval_mat = np.zeros([NUMHYP, NUMRUN])
    rej_mat = np.zeros([NUMHYP, NUMRUN])
    falrej_vec = np.zeros(NUMRUN)
    correj_vec = np.zeros(NUMRUN)
    totrej_vec = np.zeros(NUMRUN)
    FDR_mat = np.zeros([NUMHYP, NUMRUN])
    TDR_mat = np.zeros([NUMHYP, NUMRUN])
    falrej_mat = np.zeros([NUMHYP, NUMRUN])
    correj_mat = np.zeros([NUMHYP, NUMRUN])


    ##-------------- Run experiments ------------------## 
    for l in range(NUMRUN):
        # Some random seed
        if (rndseed == 1):
            rndsd = l+50
        else:
            rndsd = None

        # generate p values 
        muA_vec = np.ones(NUMHYP)*muA
        this_exp = rowexp_new_batch(NUMHYP, NUMDRAWS, Hypo, muN, muA_vec)
        this_exp.gauss_two_mix(sigma, rndsd)
        pval_mat[:, l] = this_exp.pvec 

        # Initialize FDR
        if FDR == 1: # AI
            proc = ALPHA_proc_batch(alpha0, NUMHYP)
        elif FDR == 2: # LORD
            proc = LOND_proc_batch(alpha0, NUMHYP)  
        elif FDR == 3: # D-LORD
            proc = LORD_proc_batch(alpha0, NUMHYP)   
        elif FDR == 4: # SAFFRON
            proc = SAFFRON_proc_batch(alpha0, NUMHYP, lbd, 1.6)
        elif FDR == 5: # ADDIS
            proc = SAFFRON_discard_proc_batch(alpha0, NUMHYP, lbd, tau, 1.6)
        elif FDR == 6: # LORD-async
            proc = LORD_async_proc_batch(alpha0, NUMHYP, 1.6, 0.5) 
        elif FDR == 7: # SAFFRON-async
            proc = SAFFRON_async_proc_batch(alpha0, NUMHYP, lbd, 1.6, 0.5)
        elif FDR == 8: # ADDIS-async
            proc = SAFFRON_async_discard_proc_batch(alpha0, NUMHYP, lbd, tau, 1.6, 0.5)
        elif FDR == 9: # D-LORD
            proc = LORD_discard_proc_batch(alpha0, NUMHYP, tau, 1.6) 
        elif FDR == 10: # storey-bh
            proc  = Storey_proc_batch(alpha0, NUMHYP, lbd, 1000)
        elif FDR == 11: # D-storey-bh
            proc = Storey_discard_proc_batch(alpha0, NUMHYP, lbd, tau, 1000)
            
        # Run FDR, get rejection decisions
        rej_mat[:, l] = proc.run_fdr(this_exp.pvec)

        # Save results
        falrej_singlerun = np.array(rej_mat[:,l])*np.array(1-Hypo)
        correj_singlerun = np.array(rej_mat[:,l])*np.array(Hypo)
        totrej_singlerun = np.array(rej_mat[:,l])
        falrej_vec[l] = np.sum(falrej_singlerun)
        correj_vec[l] = np.sum(correj_singlerun)
        totrej_vec[l] = np.sum(totrej_singlerun)
        falrej_mat[:, l] = falrej_singlerun

        FDR_vec = np.zeros(NUMHYP)
        for j in range(NUMHYP):
            time_vec = np.arange(NUMHYP) < (j+1)
            FDR_num = np.sum(falrej_singlerun * time_vec)
            FDR_denom = np.sum(totrej_singlerun * time_vec)
            if FDR_denom > 0:
                FDR_vec[j] = np.true_divide(FDR_num, max(1, FDR_denom))
            else:
                FDR_vec[j] = 0
        FDR_mat[:,l] = FDR_vec
             
    ##-----------------  Compute average quantities we care about -------------##
    TDR_vec = np.true_divide(correj_vec, num_alt)
    FDR_vec = [FDR_mat[NUMHYP - 1][l] for l in range(NUMRUN)]

    print(sum(FDR_vec))
    if verbose == 1:
        print("done with computation")

    ##------------------ Save data ----------------##
    data = np.r_[FDR_mat, rej_mat, falrej_mat, pval_mat, np.expand_dims(TDR_vec, axis=0), np.expand_dims(np.asarray(FDR_vec),axis=0)]
    saveres(dir_name, filename, data)

