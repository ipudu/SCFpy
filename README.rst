SCFpy
====================================================
You can use SCFpy to calculate small molecule energy:

::

    $SCFpy -c 0 -b sto-3g h2.xyz
    >Total SCF energy = -1.06609574024

Installation
------------
::

    pip install SCFpy

or

::

    git clone https://github.com/pudu1991/SCFpy.git
    python setup.py install

Usage
-----

::

    usage: scfpy [-h] [-c CHARGE] [-b BASIS] [-v] [input]

    SCFpy: simple restrited Hatree-Fock code

    positional arguments:
    input                 xyz file of molecule

    optional arguments:
    -h, --help            show this help message and exit
    -c CHARGE, --charge CHARGE
                        specify total charge of the molecule (default: 0)
    -b BASIS, --basis BASIS
                        specify basis set (default: sto-3g)
    -v, --version         displays the current version of SCFpy

Author
------

-  Pu Du (`@pudu.io <http://pudu.io>`_)

Notes
-----
- You have to have NWChem package installed on your machine.
- SCFpy get the total number of electrons, kinetic, potential, overlap, two electons
integrals from NWChem output.

Troubleshooting
---------------
