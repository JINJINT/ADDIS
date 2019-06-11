import numpy as np

class LOND_proc_batch:

    tmp = range(1, 10000)

    def __init__(self, alpha0, numhyp, gamma_vec_exponent = 0):
        self.alpha0 = alpha0
        self.w0 = self.alpha0 /2
        self.numhyp = numhyp
        tmp = range(1, 10000)

        # Compute the discount gamma sequence and make it sum to 1
        if (gamma_vec_exponent == 0):
            self.gamma_vec = np.true_divide(np.log(np.maximum(tmp, np.ones(len(tmp)) * 2)),
            np.multiply(tmp, np.exp(np.sqrt(np.log(np.maximum(np.ones(len(tmp)), tmp)))))) # asymptotically optimal for gaussian
        else:
            self.gamma_vec = np.true_divide(np.ones(len(tmp)),
                                            np.power(tmp, gamma_vec_exponent))
        self.gamma_vec = self.gamma_vec / np.float(sum(self.gamma_vec)) # normalize to sum to 1

        self.alpha = np.zeros(numhyp) # vector of test levels alpha_t at every step
        self.alpha[0] = self.gamma_vec[0]*self.w0


    
    def run_fdr(self, pvec):

        rej = np.zeros(self.numhyp)

        for k in range(0, self.numhyp-1):    
            if pvec[k] < self.alpha[k]: 
                rej[k] = 1
            if k < self.numhyp - 1:
                self.alpha[k+1] = self.alpha0 * self.gamma_vec[k+1] * (max(sum(rej[:k+1]),1))   

        return rej


        
