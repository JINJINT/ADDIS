import numpy as np

class Storey_discard_proc_batch:

    def __init__(self, alpha0, numhyp, lbd, tau, choice_size):
        self.alpha0 = alpha0
        self.lbd = lbd
        self.tau = tau
        self.choice_size = choice_size
        self.numhyp = numhyp

    def run_fdr(self, pvec):
        FDP = np.zeros(self.choice_size)
        for t in range(self.choice_size):
            s = self.lbd * t / self.choice_size
            pi_0 = (1 + sum(np.array(np.array(pvec) < self.tau, dtype = int) * np.array(np.array(pvec) > self.tau * self.lbd, dtype = int))) / (self.numhyp * self.tau * (1-self.lbd))
            FDP[t] = self.numhyp * pi_0 * s / max(sum(np.array(pvec) < (s * self.tau)),1)
        index_sets = np.where(FDP < self.alpha0)[0]
        if len(index_sets) > 0:    
            alpha = self.lbd * max(index_sets) / self.choice_size
        else: 
            raiseError(ValueError, "please try bigger choice_size") 
        rej = np.array(np.array(pvec) < alpha, dtype = int)
        return rej




