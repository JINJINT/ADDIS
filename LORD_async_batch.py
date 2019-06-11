# LORD simulation code with NO lag

import numpy as np


class LORD_async_proc_batch:
    def __init__(self, alpha0, numhyp, gamma_vec_exponent, async_param):
        self.alpha0 = alpha0 # FDR level

        # Compute the discount gamma sequence and make it sum to 1
        tmp = range(1, 10000)
        self.gamma_vec = np.true_divide(np.ones(len(tmp)),
                np.power(tmp, gamma_vec_exponent))
        self.gamma_vec = self.gamma_vec / np.float(sum(self.gamma_vec))

        self.w0 = self.alpha0 /2  # initial wealth, startfac = 0.1
        self.alpha = np.zeros(numhyp + 1) # vector of test levels alpha_t at every step
        self.alpha[0:2] = [0, self.gamma_vec[0] * self.w0]
        self.async_param = async_param


    # Running LORD on pvec
    def run_fdr(self, pvec):
        numhyp = len(pvec)
        last_rej = []
        rej = np.zeros(numhyp + 1)
        finish_times = np.zeros(numhyp + 1)
        report = np.zeros(numhyp)

        for k in range(0, numhyp):

            finish_times[k+1] = min(numhyp-1,k + np.random.geometric(self.async_param))
            # Get rejection indicators
            this_alpha = self.alpha[k + 1]
            rej[(int)(finish_times[k+1])] = rej[(int)(finish_times[k+1])] + (int)(pvec[k] < this_alpha)
            report[k] = pvec[k]<this_alpha

            # Check first rejection
            if (rej[k + 1] >= 1):
                for t in range((int)(rej[k+1])):
                    last_rej = np.append(last_rej, k+1).astype(int)


            # Update alpha_t
            last_rej_sorted = np.array(sorted(last_rej))
            if len(last_rej) > 0:
                if last_rej_sorted[0]<= (k+1):
                    first_gam = self.gamma_vec[k + 1 - (last_rej_sorted[0])]
                else:
                    first_gam = 0
                if len(last_rej) >= 2:
                    sum_gam = self.gamma_vec[(k + 1) * np.ones(len(last_rej_sorted)-1, dtype=int) - (last_rej_sorted[1:])]
                    indic = np.asarray(last_rej_sorted)<=(k+1)
                    sum_gam = sum(np.multiply(sum_gam, indic[1:]))
                else:
                    sum_gam = 0
                next_alpha = self.gamma_vec[k+1] * self.w0 + (self.alpha0 - self.w0) * first_gam + self.alpha0 * sum_gam
            else:
                next_alpha = self.gamma_vec[k+1] * self.w0
            if k < numhyp - 1:
                self.alpha[k + 2] = next_alpha



        self.alpha = self.alpha[1:]
        return report

