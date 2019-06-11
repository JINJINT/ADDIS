import numpy as np

from scipy.stats import norm
from scipy.stats import bernoulli
from scipy.linalg import toeplitz

class rowexp_new_batch:

    def __init__(self, NUMHYP, numdraws, alt_vec, mu0, mu_alt_vec):
        self.numhyp = NUMHYP
        self.alt_vec = alt_vec
        self.mu0 = mu0
        self.mu_vec = mu0*np.multiply(np.ones(NUMHYP), 1-alt_vec) + np.multiply(alt_vec, mu_alt_vec)
        self.pvec = np.zeros(NUMHYP)
        self.numdraws = numdraws

        '''
        Function drawing p-values: Mixture of two Gaussians
        '''
    def gauss_two_mix(self, sigma = 1, rndsd = 0, batch_size = 1):

        np.random.seed(rndsd)
        Z = np.zeros(self.numhyp)
        Z = self.mu_vec + np.random.randn(self.numhyp)*sigma # draw gaussian acc. to hypothesis, if sigma are all same

        self.pvec = [(1 - norm.cdf(z)) for z in Z]



