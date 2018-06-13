######################################################
#
# SCFpy: A Simple restricted Hartree-Fock code
# written by Pu Du (pudugg@gmail.com)
#
######################################################

from __future__ import print_function, division
import numpy as np

class SCFIterator(object):
    def __init__(self, rhf, tol=1e-5, maxiters=1000):
        self.rhf = rhf
        self.Eold = 0
        self.tol = tol
        self.maxiters = maxiters
        self.converged = False
        self.iterations = 0
        print('{0:5s} {1:25s} {2:25s} {3:25s}'.format('Iter',
                                            'Energy', 'deltaE', 'deltaP'))
        return
    def __iter__(self): return self
    def next(self): return self.__next__()
    def __next__(self):
        self.iterations += 1
        if self.iterations > self.maxiters:
            print('Reached the maximun iterations, SCF iterations converged = ', self.converged)
            raise StopIteration
        deltaP, self.rhf.P = self.rhf.update()
        E = self.rhf.energy
        deltaE = E - self.Eold
        self.printInfo(E, deltaE, deltaP)
        if abs(deltaP) < self.tol:
            self.converged = True
            print('\n')
            print('SCF iterations converged = ', self.converged)
            print('\n')
            raise StopIteration
        self.Eold = E
        return E
    def printInfo(self, E, deltaE, deltaP):
        print(str(self.iterations).ljust(5) + str(E).ljust(25) + \
              str(deltaE).ljust(25) + str(deltaP).ljust(25))
