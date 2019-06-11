This repository contains code of ADDIS algorithm, an adaptive and discarding algorithm for online FDR control. 
It also contains code for reproducing all the figures in the corresponding paper which is available at https://arxiv.org/abs/1905.11465

--------------------------- Common gaudiance --------------------

The main file is main.py. The experiments vary depending on the following passed arguments:

#--------------- common parameters 
--num-runs - number of independent trials
--num-hyp - number of hypotheses
--alpha0 - test level
--mu-N - used for gaussian tests as mu_N, where observations under the alternative are N(Z,1), Z~N(mu_N,1)
--mu-A - used for gaussian tests as mu_A, where observations under the alternative are N(Z,1), Z~N(mu_A,1)

#------------------specific parameters for plotting power of ADDIS against different values of tau and lbd with single pi_A
--bestpara - whether to do this kind of ploting or not
--pi - the value of pi_A
--step - the step size of setting different tau and lbd

#------------------specific parameters for plotting power of different algorithms under the same settings
--FDRrange - integers encoding the choice of algorithms and parameters (listed in the comments of main.py)
--pirange - range of pi_A
--tau-value - the list of value of tau paired with the value of pi_A
--lbd-value - the list of value of lbd paired with the value of pi_A

-----------------------------------------------------------------------------------------------------------------------------------------------------------


--------------------------- To reproduce the figures in the paper-------------------
Run the following command in the terminal under the repository of current code repository
Plots saved as .pdf files in the folder "plots", data saved as .dat files in the folder "dat"

Note that the plots may look different than the ones in the paper because the observations are randomly generated

#------- Figure 1
python main.py 

#------- Figure 3
python main.py --bestpara --mu-N "-1"

#------- Figure 4
python main.py --FDRrange "5,4,3,2,1" --mu-N " -0.5,-1,-1.5"
python main.py --FDRrange "5,4,3,2,1" --mu-N "0" --mu-A "3,4"

#------- Figure 5 (a, d)
python main.py --FDRrange "9,3"  

#------- Figure 5 (b, f)
python main.py --FDRrange "8,7,6"

#------- Figure 5 (c, e)
python main.py --FDRrange "11,10"
 
--------------------------------------------------------

This code borrowed substantial parts from Tijana Zrnic's code available at: https://github.com/tijana-zrnic/SAFFRONcode
If you spot any issues or bugs, please contact me at jinjint(at)andrew(dot)cmu(dot)edu

