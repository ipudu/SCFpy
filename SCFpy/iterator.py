import numpy as np

class SCFIterator(object):
    def __init__(self, rhf, tol=1e-5, maxiters=100):
        self.rhf = rhf
        self.Eold = 0
        self.tol = tol
        self.maxiters = maxiters
        self.converged = False
        self.iterations = 0
        return
    def __iter__(self): return self
    def next(self): return self.__next__()
    def __next__(self):
        self.iterations += 1
        if self.iterations > self.maxiters:
            raise StopIteration
        deltaP, self.rhf.P = self.rhf.update()
        E = self.rhf.energy
        if abs(deltaP) < self.tol:
            self.converged = True
            raise StopIteration
        self.Eold = E
        return E
