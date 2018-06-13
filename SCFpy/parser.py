######################################################
#
# SCFpy: A Simple restricted Hartree-Fock code
# written by Pu Du (pudugg@gmail.com)
#
######################################################

from __future__ import print_function, division

import os
import re
import subprocess
import numpy as np

class parser(object):
    def __init__(self,nwo):
        self.file = nwo
        self.Nelec = 0
        self.grabInfo()

    def grabInfo(self):
        """
        grab kinetic 1-e integrals
             potential 1-e integrals
             overlap 1-e integrals
             all 2-e integrals
             guess e density matrix
             nuclear replusion energy from nwchem output file
        """
        #for kinetic integrals
        t_start = r'^\s*Begin\skinetic\s1-e\sintegrals$'
        t_end = r'^\s*End\skinetic\s1-e\sintegrals$'
        t_info =r'^.*\d+$'
        t_file = open('t.dat', 'w')
        t_flag = False

        #for potential integrals
        v_start = r'^\s*Begin\spotential\s1-e\sintegrals$'
        v_end = r'^\s*End\spotential\s1-e\sintegrals$'
        v_info =r'^.*\d+$'
        v_file = open('v.dat', 'w')
        v_flag = False

        #for overlap integrals
        s_start = r'^\s*Begin\soverlap\s1-e\sintegrals$'
        s_end = r'^\s*End\soverlap\s1-e\sintegrals$'
        s_info =r'^.*\d+$'
        s_file = open('s.dat', 'w')
        s_flag = False

        #for two electron integrals
        e2_start = r'^\s*Begin\sall\s2-e\sintegrals$'
        e2_end = r'^\s*End\sall\s2-e\sintegrals$'
        e2_info =r'^.*\d+$'
        e2_file = open('e2.dat', 'w')
        e2_flag = False

        #for nulear replustion energy
        enuc_info = r'^.*Nuclear\srepulsion\senergy\s=.+$'
        enuc_file = open('enuc.dat','w')


        with open(self.file, 'r') as f:
            for line in f:
                if re.match(r'^\s*closed\sshells\s*=', line):
                    lineInfo = line.split()
                    self.Nelec = int(lineInfo[3]) * 2
                if re.match(t_start, line):
                    t_flag = True
                if re.match(t_end, line):
                    t_flag = False
                if t_flag is True:
                    if re.match(t_info, line):
                        lineInfo = line.split()
                        t_file.write(lineInfo[1] + '  ' +
                                     lineInfo[4] + '  ' +
                                     lineInfo[7]+'\n')
                if re.match(v_start, line):
                    v_flag = True
                if re.match(v_end, line):
                    v_flag = False
                if v_flag is True:
                    if re.match(v_info, line):
                        lineInfo = line.split()
                        v_file.write(lineInfo[1] + '  ' +
                                     lineInfo[4] + '  ' +
                                     lineInfo[7]+'\n')
                if re.match(s_start, line):
                    s_flag = True
                if re.match(s_end, line):
                    s_flag = False
                if s_flag is True:
                    if re.match(s_info, line):
                        lineInfo = line.split()
                        s_file.write(lineInfo[1] + '  ' +
                                     lineInfo[4] + '  ' +
                                     lineInfo[7]+'\n')
                if re.match(e2_start, line):
                    e2_flag = True
                if re.match(e2_end, line):
                    e2_flag = False
                if e2_flag is True:
                    if re.match(e2_info, line):
                        lineInfo = line.split()
                        e2_file.write(lineInfo[1] + '  ' +
                                      lineInfo[2] + '  ' +
                                      lineInfo[3] + '  ' +
                                      lineInfo[4] + '  ' +
                                      lineInfo[5]+'\n')
                if re.match(enuc_info, line):
                    lineInfo = line.split()
                    enuc_file.write(lineInfo[-1]+'\n')
        t_file.close()
        v_file.close()
        s_file.close()
        e2_file.close()
        enuc_file.close()
