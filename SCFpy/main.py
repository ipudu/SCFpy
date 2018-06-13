######################################################
#
# SCFpy: A Simple restricted Hartree-Fock code
# written by Pu Du (pudugg@gmail.com)
#
######################################################

from __future__ import print_function, division

import argparse
import os
import subprocess
from .scf import rhf
from .iterator import SCFIterator
from .parser import parser as read
from .__init__ import __version__

def welcome():
    print('#' * 42)
    print('#SCFpy: Simple restricted Hartree-Fock code#')
    print('#' * 42)
    print('\n')

def enable_cache():
    if not os.path.exists('perm'):
        os.makedirs('perm')
    if not os.path.exists('scratch'):
        os.makedirs('scratch')

def nwchem(args):
    name = os.path.splitext(args['input'])[0]
    with open(name + '.nw', 'w') as f:
        f.write('echo\n')
        f.write('start ' + os.path.splitext(args['input'])[0] + '\n\n')
        f.write('permanent_dir ./perm\n')
        f.write('scratch_dir ./scratch\n\n')
        f.write('charge ' + str(args['charge']) + '\n')
        f.write('geometry units angstroms noautosym\n')
        with open(args['input'],'r') as i:
            for line in i:
                lineInfo = line.split()
                if len(lineInfo) == 4:
                    f.write(line)
        f.write('end\n\n')
        f.write('basis\n')
        f.write(' * library ' + args['basis'] + '\n')
        f.write('end\n\n')
        f.write('scf\nprint overlap kinetic potential ao2eints debug\nend\n')
        f.write('task scf\n')
    return name

def get_parser():
    parser = argparse.ArgumentParser(description='SCFpy: simple restricted Hartree-Fock code')
    parser.add_argument('input', type=str, nargs='?',help='xyz file of molecule')
    parser.add_argument('-c', '--charge',  default=0, type=int,
                        help='specify total charge of the molecule (default: 0)')
    parser.add_argument('-b','--basis', default='sto-3g', type=str,
                        help='specify basis set (default: sto-3g)')
    parser.add_argument('-v', '--version', action='store_true',
                        help='displays the current version of SCFpy')
    return parser

def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())
    if args['version']:
        print(__version__)
        return
    if not args['input']:
        parser.print_help()
        return
    else:
        welcome()
        enable_cache()
        print('Preparing the input file for NWChem ............')
        name = nwchem(args)
        print('NWChem is running...............................')
        os.system('nwchem '+ name +'.nw' + '>' + name +'.nwo')
        print('Getting following infomation from NWChem output:')
        print('Number of total electrons')
        print('Nuclear replusion energy')
        print('Kinetic integral')
        print('Potential integral')
        print('Overlap integral')
        print('two electrons integral\n')

        p = read(name+'.nwo')
        mol = rhf(p.Nelec,'enuc.dat','s.dat','t.dat','v.dat','e2.dat')
        print('=====> Begin SCF Iterations <====\n\n')
        ens = mol.converge(SCFIterator)
        print("*    Total SCF energy = " +str(mol.energy))

if __name__ == '__main__':
    command_line_runner()
