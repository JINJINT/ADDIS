import numpy as np


class SAFFRON_discard_proc_batch:
    def __init__(self, alpha0, numhyp, lbd, tau, gamma_vec_exponent):
        self.alpha0 = alpha0 
        self.lbd = lbd 
        self.tau = tau

        # Compute the discount gamma sequence and make it sum to 1
        tmp = range(1, 10000)
        self.gamma_vec = np.true_divide(np.ones(len(tmp)),
                np.power(tmp, gamma_vec_exponent))
        self.gamma_vec = self.gamma_vec / np.float(sum(self.gamma_vec))

        self.w0 = tau * (1 - lbd) * self.alpha0/2 
        self.alpha = np.zeros(numhyp + 1) 
        self.alpha[0:2] = [0, tau * self.gamma_vec[0] * self.w0]



    # Computing the number of candidates after each rejection
    def count_candidates(self, last_rej, candidates, timestep):
        ret_val = [];
        for j in range(1,len(last_rej)):
            ret_val = np.append(ret_val, sum(candidates[last_rej[j]+1:timestep + 1]))
        return ret_val.astype(int)

    # Running SAFFRON on pvec
    def run_fdr(self, pvec):
        numhyp = len(pvec)
        last_rej = []
        rej = np.zeros(numhyp + 1 )
        candidates = np.zeros(numhyp + 1 )
        testers = np.zeros(numhyp + 1)

        for k in range(0, numhyp):

            # Get candidate and rejection indicators
            this_alpha = self.alpha[k + 1]
            candidates[k + 1 ] = (pvec[k] < self.tau*self.lbd)
            rej[k + 1 ] = (pvec[k] < this_alpha)
            testers[k + 1] = (pvec[k] < self.tau) 

            # Check first rejection
            if (rej[k + 1 ] == 1):
                last_rej = np.append(last_rej, k + 1 ).astype(int)
            last_rej_rela = np.array([int(sum(testers[1:(int)(lr)+1])) for lr in last_rej])

            candidates_total = sum(candidates[1 : k + 2])
            zero_gam = self.gamma_vec[int(sum(testers[1 : k + 2])) - (int)(candidates_total)]
            # Update alpha_t
            if len(last_rej) > 0:
                if last_rej[0]<= (k+1):
                    candidates_after_first = sum(candidates[last_rej[0]+1 : k + 2])
                    first_gam = self.gamma_vec[int(sum(testers[1 : k + 2])) - (last_rej_rela[0]) - (int)(candidates_after_first)]
                else:
                    first_gam = 0
                if len(last_rej) >= 2:
                    sum_gam = self.gamma_vec[int(sum(testers[1 : k + 2])) * np.ones(len(last_rej)-1, dtype=int) - (last_rej_rela[1:]) - self.count_candidates(last_rej, candidates, k+1)]
                    indic = last_rej<=(k+1)
                    sum_gam = sum(np.multiply(sum_gam, indic[1:]))
                else:
                    sum_gam = 0
                next_alpha = min(self.tau * self.lbd, zero_gam * self.w0 + (self.tau * (1-self.lbd)*self.alpha0 - self.w0) * first_gam + self.tau * (1-self.lbd)*self.alpha0 * sum_gam)
            else:
                next_alpha = min(self.tau * self.lbd, zero_gam * self.w0)
            if k < numhyp - 1:
                testers[k + 2] = (pvec[k + 1] < self.tau)
                self.alpha[k + 2] = next_alpha

        rej = rej[1 :]
        self.alpha = self.alpha[1:]
        return rej



