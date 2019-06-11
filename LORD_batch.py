import numpy as np

class LORD_proc_batch:

    tmp = range(1, 10000)

    def __init__(self, alpha0, numhyp, gamma_vec_exponent = 0):
        self.alpha0 = alpha0
        self.w0 = self.alpha0 / 2
        tmp = range(1, 10000)

        if (gamma_vec_exponent == 0):
            self.gamma_vec = np.true_divide(np.log(np.maximum(tmp, np.ones(len(tmp)) * 2)),
            np.multiply(tmp, np.exp(np.sqrt(np.log(np.maximum(np.ones(len(tmp)), tmp)))))) # asymptotically optimal for gaussian
        else:
            self.gamma_vec = np.true_divide(np.ones(len(tmp)),
                                            np.power(tmp, gamma_vec_exponent))
        self.gamma_vec = self.gamma_vec / np.float(sum(self.gamma_vec)) # normalize to sum to 1

        self.alpha = np.zeros(numhyp + 1) # vector of test levels alpha_t at every step
        self.alpha[0:2] = [0, self.gamma_vec[0]*self.w0]

    
    def run_fdr(self, pvec):

        numhyp = len(pvec)
        last_rej = []
        
        rej = np.zeros(numhyp + 1)

        for k in range(0, numhyp):    

            # Get rejection indicator
            this_alpha = self.alpha[k + 1]
            rej[k + 1] = (pvec[k] < this_alpha)

            if (rej[k + 1] == 1):
                last_rej = np.append(last_rej, k + 1 ).astype(int)


            if len(last_rej) > 0:
                if last_rej[0] <= (k + 1):
                    first_gam = self.gamma_vec[k + 1 - (last_rej[0])]
                else:
                    first_gam = 0
                if len(last_rej) >= 2:
                    sum_gam = self.gamma_vec[(k + 1) * np.ones(len(last_rej) - 1, dtype=int) - (last_rej[1:])]
                    indic = np.asarray(last_rej) <= (k + 1)
                    sum_gam = sum(np.multiply(sum_gam, indic[1:]))
                else:
                    sum_gam = 0
                next_alpha = self.gamma_vec[k + 1] * self.w0 + (self.alpha0 - self.w0) * first_gam + self.alpha0 * sum_gam
            else:
                next_alpha = self.gamma_vec[k + 1] * self.w0
            if k < numhyp - 1:
                self.alpha[k + 2] = next_alpha

        rej = rej[1:]
        self.alpha = self.alpha[1:]
        return rej
