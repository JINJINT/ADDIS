# import python packages
import logging, argparse
import numpy as np

# import function files
from computeFDR import*
from plottingresults import*
from toimport import *
from best_para_compute import *
from plot_best_para import *


def main():

    # generate repo for saved data
    if not os.path.exists('./dat'):
        os.makedirs('./dat')
    
    # get common parameters
    muNrange = str2list(args.mu_N, 'float')
    muArange = str2list(args.mu_A, 'float')
    num_hyp = args.num_hyp
    num_runs = args.num_runs
    alpha0 = args.alpha0

    if args.bestpara:
        ## ------- compute the power of ADDIS with varied tau and lbd --------##
        step = args.step
        pi = args.pi

        for muN in muNrange:
            for muA in muArange:

                filename_pre = 'TRADE_OFF_MN%.1f_MA%.1f_NH%d_NR%d_step%.2f_pi%1.f' % (muN, muA, num_hyp, num_runs, step, pi)
                all_filenames = [filename for filename in os.listdir('./dat') if filename.startswith(filename_pre)]

                # Run experiment if data doesn't exist yet
                if all_filenames == []:
                    print("Running experiment for plotting trade off with muN %.2f and muA %.2f with step %.2f and pi %.1f" % (muN, muA, step, pi))
                    best_para(num_runs, num_hyp, muN, muA, alpha0, pi, step)
                else:
                    print("Experiments for plotting trade off with muN %.2f and muA %.2f with step %.2f and pi %.1f are already run" % (muN, muA, step, pi))

                print("Now plotting ...")

                # plot the power of ADDIS versus different tau and lbd
                plot_best(pi, muN, muA, step, num_runs, num_hyp)


    else:    

        ##--------  SET PARAMETERS FOR RUNNING EXPERIMENT %%%%%%%##########

        FDRrange = str2list(args.FDRrange)
        lbd_list = str2list(args.lbd_value, 'float')
        tau_list = str2list(args.tau_value, 'float')
        pirange = str2list(args.pirange, 'float')

        ########%%%%%%%%%%%%%%%%% RUN EXPERIMENT %%%%%%%%########################
        for mu_A in muArange:

            def singlepi(i):
                pi = pirange[i]
                lbd = lbd_list[i]
                tau = tau_list[i]

                # Run single FDR
                for FDR in FDRrange:
                    for mu_N in muNrange:
                        # Prevent from running if data already exists
                        filename_pre = 'MN%.1f_MA%.1f_Si1.0_FDR%d_NH%d_ND%d_PM%.2f_NR%d_lbd%.4f_tau%.4f' % (mu_N, mu_A, FDR, num_hyp, 1, pi, num_runs, lbd, tau)
                        all_filenames = [filename for filename in os.listdir('./dat') if filename.startswith(filename_pre)]

                        # Run experiment if data doesn't exist yet
                        if all_filenames == []:
                            print("Running experiment for FDR procedure %s with muN %.1f and muA %.1f and pi %.1f and lbd %.4f and tau %.4f" % (proc_list[FDR-1], mu_N, mu_A, pi, lbd, tau))
                            run_single(num_runs, num_hyp, 1, mu_N, mu_A, pi, alpha0, FDR, 1, lbd, tau, verbose = False)
                        else:
                            print("Experiments for FDR procedure %s with muN %.1f and muA %.1f and pi %.1f and lbd %.4f and tau %.4f are already run" % (proc_list[FDR-1], mu_N, mu_A, pi, lbd, tau))
                
            with Pool() as p:
                TDR_vec = p.map(singlepi, range(len(pirange)))
                p.close()
                p.join()
                p.terminate()   
                p.restart() 


        # Plot different measures over hypotheses for different FDR
        print("Now plotting ... ")
        plot_results(FDRrange, pirange, muNrange, muArange, 1, num_hyp, num_runs)
            

# proc_list = [1:'Alpha-investing',2:'LOND', 3:'LORD++', 4:'SAFFRON', 5:'ADDIS',
#             6:'LORDasync', 7:'SAFFRONasync', 8:'ADDISasync', 9: 'D-LORD', 10: 'Storey-BH', 11: 'D-Storey-BH']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-runs', type = int, default = 200) # number of independent trials
    parser.add_argument('--num-hyp', type = int, default = 1000) # number of hypotheses
    parser.add_argument('--alpha0', type = float, default = 0.05) # desired FDR bound
    parser.add_argument('--mu-N', type = str, default = "0,-1") # mu_N for gaussian mean tests
    parser.add_argument('--mu-A', type = str, default = "3") # mu_A for gaussian mean tests

    parser.add_argument('--bestpara', action='store_true') # whether to find the best tau and lbd or not
    parser.add_argument('--pi', type = float, default = 0.2) # the value of pi when finding the best tau and lbd
    parser.add_argument('--step', type = float, default = 0.05) # the step size of searching when find the best tau and lbd   

    parser.add_argument('--FDRrange', type = str, default = "5,4,3") # choice of algorithms 
    parser.add_argument('--lbd-value', type = str, default = "0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5") # lbd paired with each pi_A
    parser.add_argument('--tau-value', type = str, default = "0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5") # tau paired with each pi_A
    parser.add_argument('--pirange', type = str, default = '0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9') # range of pi_A
    args = parser.parse_args()
    logging.info(args)
    main()




