CRITTERS
========

C++ implamantation of the "critters" reversible cellular automaton, with simple Python interface, written in ctypes.
More information about this: 
- http://en.wikipedia.org/wiki/Reversible_cellular_automaton
- http://www.cise.ufl.edu/~skoehler/critters/index.html

COMPILATION
-----------

Run make.sh for Linux or make.cmd fow Windows.
For Windows, Mingw (g++) is expected to be installed. Edit the batch file, if you are using a different compiler.

FEATURES
--------
Implements "Critters" and other block cellular automatons with Margolus neighborhood and 2 states.


INSTALLATION
------------
Not supported yet. Run it from the compilation folder.


FILES
-----

- critters.py - Python interface for the C++ library.
- test_critters.py - some sample program, that run simulation
- critters.cpp - C++ implementation of the algorithm.

REQUIREMENTS
------------
Python2, Numpy, C++ compiler.

Sample program can use Matplotlib or PIL.