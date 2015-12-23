fullrmc
=======
It's a Reverse Monte Carlo (RMC) python/Cython/C package, especially designed to solve an inverse 
problem whereby an atomic/molecular model is adjusted until its atoms positions have the greatest 
consistency with a set of experimental data. RMC is probably best known for its applications in 
condensed matter physics and solid state chemistry. fullrmc is a fully object-oriented package 
where everything can be overloaded allowing easy development, implementation and maintenance of the code. 
It's core sub-package and modules are fully optimized written in cython/C. fullrmc is unique in its approach, 
among other functionalities:

1. Atomic and molecular systems are supported.
2. All types (not limited to cubic) of periodic boundary conditions systems are supported.
3. Atoms can be grouped into groups so the system can evolve atomically, clusterly, molecularly or any combination of those.
4. Every group can be assigned a different move generator (translation, rotation, a combination of moves generators, etc).
5. Selection of groups to perform moves can be done manually OR automatically, randomly OR NOT !!
6. Supports Artificial Intelligence and Reinforcement Machine Learning algorithms. 

Next on the list
================
* Generators machine learning algorithms.
* Elements transmutation.

News
====
* Coordination number constraint added.
* Groups swap and atoms position exchange added to generators.
* Machine learning is added to group selection. First tests are very promising show great improvements.

Installation
============
##### fullrmc requires:
* Python (>= 2.6 and < 3),
* NumPy (lowest version tested is 1.7.1),
* cython (lowest version tested is 0.21.1),
* matplotlib (lowest version tested is 1.4),
* pdbParser (lowest version tested is 0.1.2),
* pysimplelog (lowest version tested is 0.1.7).

##### Installation using pip:
numpy and cython must be installed and updated manually. 

```bash
pip install -U "numpy>=1.7.1"
pip install -U "cython>=0.21.1"
pip install fullrmc
```

##### Installation by cloning github repository
Ensure all fullrmc required packages are installed.
```python
# check whether all packages are already installed
import numpy
assert numpy.__version__ >= '1.7.1', 'numpy installation must be upgraded'
import cython
assert cython.__version__ >= '0.21.1', 'cython installation must be upgraded'
import pdbParser
assert pdbParser.__version__ >= '0.1.2', 'pdbParser installation must be upgraded'
import pysimplelog
assert pysimplelog.__version__ >= '0.1.7', 'pysimplelog installation must be upgraded'
import matplotlib
assert matplotlib.__version__ >= '1.4', 'matplotlib installation must be upgraded'
```
Locate python's site-packages using:
```python
import os
os.path.join(os.path.dirname(os.__file__), 'site_packages')
```
Navigate to site_packages folder and clone git repository:
```bash
cd .../site_packages
git clone https://github.com/bachiraoun/fullrmc.git  
``` 
Compile fullrmc Extension files. Change directory to .../site_packages/fullrmc/Extensions
```bash
cd .../site_packages/fullrmc/Extensions
python setup.py build_ext --inplace 
```

Online documentation
====================
http://bachiraoun.github.io/fullrmc/

Author
======
Bachir Aoun
