This repository contains code of ADDIS algorithm, an adaptive and discarding algorithm for online FDR control. 
It also contains code for reproducing all the figures in the corresponding paper which is available at https://arxiv.org/abs/1905.11465

========================== Common guidance ========================================\n

The main file is main.py. The experiments vary depending on the following passed arguments: \n

----------Common parameters \n
num-runs - number of independent trials \n
num-hyp - number of hypotheses
alpha0 - test level\n
mu-N - used for gaussian tests as mu_N, where observations under the alternative are N(Z,1), Z~N(mu_N,1)\n
mu-A - used for gaussian tests as mu_A, where observations under the alternative are N(Z,1), Z~N(mu_A,1)\n

----------Specific parameters for plotting power of ADDIS against different values of tau and lbd with single pi_A\n
bestpara - whether to do this kind of plotting or not\n
pi - the value of pi_A\n
step - the step size of setting different tau and lbd\n

-----------Specific parameters for plotting power of different algorithms under the same settings\n
FDRrange - integers encoding the choice of algorithms and parameters (listed in the comments of main.py)\n
pirange - range of pi_A
tau-value - the list of value of tau paired with the value of pi_A\n
lbd-value - the list of value of lbd paired with the value of pi_A\n

**************************************************************************************************************************\n

========================== To reproduce the figures in the paper ========================== \n
Run the following command in the terminal under the repository of current code repository.\n

Plots saved as .pdf files in the folder "plots", data saved as .dat files in the folder "dat".\n

Note that the plots may look different than the ones in the paper because the observations are randomly generated.\n

#------- Figure 1\n
python main.py \n

#------- Figure 3\n
python main.py --bestpara --mu-N "-1"\n

#------- Figure 4\n
python main.py --FDRrange "5,4,3,2,1" --mu-N " -0.5,-1,-1.5"\n
python main.py --FDRrange "5,4,3,2,1" --mu-N "0" --mu-A "3,4"\n

#------- Figure 5 (a, d)\n
python main.py --FDRrange "9,3"  \n

#------- Figure 5 (b, f)\n
python main.py --FDRrange "8,7,6"\n

#------- Figure 5 (c, e)\n
python main.py --FDRrange "11,10"\n
 
--------------------------------------------------------

This code borrowed substantial parts from Tijana Zrnic's code available at: https://github.com/tijana-zrnic/SAFFRONcode
If you spot any issues or bugs, please contact me at jinjint(at)andrew(dot)cmu(dot)edu

