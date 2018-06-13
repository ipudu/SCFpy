######################################################
#
# SCFpy: A Simple restricted Hartree-Fock code
# written by Pu Du (pudugg@gmail.com)
#
######################################################

from __future__ import print_function, division

import numpy as np
from .iterator import SCFIterator

class rhf(object):
    """
    class of restricted Hartree-Fock method.
    """
    def __init__(self,Nelec,enuc,s,t,v,e2):
        self.Nelec = Nelec
        self.enuc = self.nuclear_repulsion(enuc)
        self.T = self.kinetic(t)
        self.V = self.potential(v)
        self.S = self.overlap(s)
        ###################################################
        #symmetric orthogonalization P.143 (3.166 - 3.167)
        ###################################################
        s, U = np.linalg.eig(self.S)
        s_mhalf = np.diag(s**(-0.5))
        S_mhalf = np.dot(U, np.dot(s_mhalf, U.T))
        self.X = S_mhalf
        ###################################################
        #set up a guess density matrix
        ###################################################
        self.P = np.zeros((len(self.T),len(self.T)))
        self.twoe = self.twoe_integrals(e2)
        self.energies = []
        self.energy = 0
        self.converged = False

    def converge(self, iterator=SCFIterator, **kwargs):
        converger = iterator(self, **kwargs)
        for en in converger:
            self.energies.append(en)
        self.converged = converger.converged
        return self.energies

    def update(self):
        self.energy = self.enuc
        Hcore = self.T + self.V
        #print 'Hcore = \n', Hcore
        P = self.P
        #print "P = \n", P
        ###################################################
        #make Fock matrix P.141 3.154
        ###################################################
        F=self.fock(Hcore, P)
        #print 'F= \n', F
        ###################################################
        #F' matrix P.145 (3.177)
        ###################################################
        F_prime = np.dot(self.X.T, np.dot(F,self.X))
        #print "F_prime = \n", F_prime
        ###################################################
        #eigenvalue problem of F' P.145 (3.178)
        ###################################################
        E, C_prime = np.linalg.eigh(F_prime)
        C = np.dot(self.X, C_prime)
        #print "E = \n", E
        #print "C_prime = \n", C_prime
        ###################################################
        #calculate the energy p.149 (3.183)
        ###################################################
        self.energy = self.energy + 0.5 * np.sum(P* (Hcore + F))
        #self.energy = self.energy + self.get_energy(P,Hcore,F)
        #EN = self.currentenergy(P,Hcore,F,2)
        #print 0.5 * np.sum(P* (Hcore + F))
        #print self.energy
        ###################################################
        #Form a new density matrix P from C p.139 (3.178)
        ###################################################
        #print C
        Pold, P = self.density(C,P,self.Nelec)
        P = 0.5 * P + 0.5 * Pold
        #print "Pold = \n", Pold
        #print "P = \n", P
        ###################################################
        #standard deviation of density matrix p.149
        ###################################################
        deltaP = self.delta(P, Pold)
        return deltaP, P

    def nuclear_repulsion(self, enuc):
        with open(enuc, 'r') as f:
            e = float(f.read())
        return e

    def kinetic(self, t):
        Traw = np.loadtxt(t)
        #dim = int(np.sqrt(len(Traw)))
        dim = int(Traw[-1][0])
        T = np.zeros((dim, dim))
        for e in Traw:
            T[int(e[0])-1][int(e[1])-1] = e[2]
        return T

    def potential(self, v):
        V = self.kinetic(v)
        return V

    def overlap(self, s):
        S = self.kinetic(s)
        return S

    def twoe_integrals(self, e2):
        ERIraw = np.genfromtxt(e2,dtype=None)
        twoe = {self.eint(row[0],row[1],row[2],row[3]) : row[4] for row in ERIraw}
        return twoe

    def eint(self,a,b,c,d):
        if a > b: ab = a*(a+1)/2 + b
        else: ab = b*(b+1)/2 + a
        if c > d: cd = c*(c+1)/2 + d
        else: cd = d*(d+1)/2 + c
        if ab > cd: abcd = ab*(ab+1)/2 + cd
        else: abcd = cd*(cd+1)/2 + ab
        return abcd

    def tei(self,a,b,c,d):
        return self.twoe.get(self.eint(a,b,c,d),0.0)

    def fock(self, Hcore, P):
        dim = len(Hcore)
        F = np.empty((dim, dim))
        for i in range(0, dim):
            for j in range(0, dim):
                F[i,j] = Hcore[i,j]
                for k in range(0, dim):
                    for l in range(0, dim):
                        F[i,j] = F[i,j] + P[k,l]*(self.tei(i+1,j+1,k+1,l+1) - \
                                 0.5e0*self.tei(i+1,k+1,j+1,l+1))
        return F
    def density(self,C,P,Nelec):
        dim = len(P)
        Pold = np.zeros((dim,dim))
        for mu in range(0,dim):
            for nu in range(0,dim):
                Pold[mu,nu] = P[mu,nu]
                P[mu,nu] = 0.0e0
                for m in range(0,Nelec//2):
                    P[mu,nu] = P[mu,nu] + 2*C[mu,m]*C[nu,m]
        return Pold, P

    def currentenergy(self,P,Hcore,F,dim):
      EN = 0.0e0
      for mu in range(0,dim):
        for nu in range(0,dim):
          EN = EN + 0.5*P[mu,nu]*(Hcore[mu,nu] + F[mu,nu])
      #print 'Energy = ', EN
      return EN

    def delta(self,P,Pold):
      DELTA = 0.0e0
      dim = len(P)
      for i in range(0,dim):
        for j in range(0,dim):
          DELTA = DELTA+((P[i,j]-Pold[i,j])**2)
      DELTA = (DELTA/4)**(0.5)
      return DELTA
