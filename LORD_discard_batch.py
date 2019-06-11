import numpy as np


class LORD_discard_proc_batch:
    def __init__(self, alpha0, numhyp, tau, gamma_vec_exponent):
        self.alpha0 = alpha0 
        self.tau = tau

        tmp = range(1, 10000)
        self.gamma_vec = np.true_divide(np.ones(len(tmp)),
                np.power(tmp, gamma_vec_exponent))
        self.gamma_vec = self.gamma_vec / np.float(sum(self.gamma_vec))

        self.w0 = tau * self.alpha0 / 2 
        self.alpha = np.zeros(numhyp + 1) 
        self.alpha[0:2] = [0, self.gamma_vec[0] * self.w0]


    def run_fdr(self, pvec):
        numhyp = len(pvec)
        last_rej = []
        rej = np.zeros(numhyp + 1)
        testers = np.zeros(numhyp + 1)
      

        for k in range(0, numhyp):
            
            # Get rejection indicators
            this_alpha = self.alpha[k + 1]
            rej[k + 1] = (int)(pvec[k] < this_alpha)
            testers[k + 1] = (int)(pvec[k] <= self.tau)


            # Check first rejection
            if (rej[k + 1] >= 1):
                last_rej = np.append(last_rej, k+1).astype(int)

            # Update alpha_t
            last_rej_rela = np.array([int(sum(testers[1:(int)(lr)+1])) for lr in last_rej])
            zero_gam = self.gamma_vec[int(sum(testers[1:k+2]))]    

            if len(last_rej) > 0:
                if last_rej[0]<= (k+1):
                    first_gam = self.gamma_vec[int(sum(testers[1:k+2]))- (last_rej_rela[0])]
                else:
                    first_gam = 0
                if len(last_rej) >= 2:
                    sum_gam = self.gamma_vec[int(sum(testers[1:k+2])) * np.ones(len(last_rej)-1, dtype=int) - (last_rej_rela[1:])]
                    indic = np.asarray(last_rej)<=(k+1)
                    sum_gam = sum(np.multiply(sum_gam, indic[1:]))
                else:
                    sum_gam = 0
                next_alpha = zero_gam * self.w0 + (self.tau * self.alpha0 - self.w0) * first_gam + self.tau * self.alpha0 * sum_gam
            else:
                next_alpha = zero_gam * self.w0
            if k < numhyp - 1:
                self.alpha[k + 2] = min(next_alpha, self.tau)


        self.alpha = self.alpha[1:]
        rej = rej[1:] 
        return rej

