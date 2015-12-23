""" 
Inheritance diagram
===================  
.. inheritance-diagram:: fullrmc.Engine.Engine

.. inheritance-diagram:: fullrmc.Core.Group.Group
    
.. inheritance-diagram:: fullrmc.Selectors.RandomSelectors
                         fullrmc.Selectors.OrderedSelectors
                         fullrmc.Generators.Translations 
                         fullrmc.Generators.Rotations 
                         fullrmc.Generators.Swaps
                         fullrmc.Generators.Agitations
                         fullrmc.Constraints.CoordinationNumberConstraints
                         fullrmc.Constraints.DistanceConstraints
                         fullrmc.Constraints.BondConstraints
                         fullrmc.Constraints.AngleConstraints
                         fullrmc.Constraints.ImproperAngleConstraints
                         fullrmc.Constraints.PairDistributionConstraints
                         fullrmc.Constraints.PairCorrelationConstraints
    :parts: 1
    

Welcoming videos
================    
+--------------------------------------------------------------+----------------------------------------------+
|.. raw:: html                                                 | Molecular system full RMC                    |  
|                                                              | simulation. Groups are set to                |
|        <iframe width="580" height="315"                      | molecules and smart moves are                |
|        src="https://www.youtube.com/embed/untepXVc3BQ"       | applied. Translations along                  |
|        frameborder="0" allowfullscreen>                      | symmetry axes, rotations                     |
|        </iframe>                                             | about symmetry axes, etc.                    |
|                                                              |                                              |
+--------------------------------------------------------------+----------------------------------------------+
|.. raw:: html                                                 | Atomic binary Nickel-Titanium shape memory   |  
|                                                              | alloy system phase transformation RMC        |
|        <iframe width="580" height="315"                      | simulation. Random atomic translations are   |
|        src="https://www.youtube.com/embed/yTnCAw1DK3Q?rel=0" | enough to reproduce short range ordering. But|
|        frameborder="0" allowfullscreen>                      | swapping atoms is necessary to fit long range|
|        </iframe>                                             | atomic correlations.                         |
|                                                              |                                              |
+--------------------------------------------------------------+----------------------------------------------+
|.. raw:: html                                                 | Molecular system mere atomic                 |  
|                                                              | RMC simulation. Covalent bond                |
|        <iframe width="580" height="315"                      | electron density polarization                |
|        src="https://www.youtube.com/embed/xnG0wnEfbJ8"       | is modelled by allowing                      |
|        frameborder="0" allowfullscreen>                      | fullrmc to explore across                    |
|        </iframe>                                             | energy low correlation                       |
|                                                              | barriers.                                    |
+--------------------------------------------------------------+----------------------------------------------+


Brief Description
=================
Reverse Monte Carlo (RMC) is probably best known for its applications in condensed matter physics and solid state chemistry.
fullrmc (https://github.com/bachiraoun/fullrmc) is a RMC modelling package to solve an inverse problem whereby an atomic/molecular 
model is adjusted until its atoms position have the greatest consistency with a set of experimental data.\n
fullrmc is a python package with its core and calculation modules optimized and compiled in Cython. 
fullrmc is not a standard RMC package but it is rather unique in its approach to solving an atomic or molecular structure. 
fullrmc's Engine sub-module is the main module that contains the definition of 'Engine' which 
is the main and only class used to launch an RMC calculation. Engine reads only Protein Data Bank formatted 
atomic configuration files '.pdb' (http://deposit.rcsb.org/adit/docs/pdb_atom_format.html) and handles  
other definitions and attributes such as:

    #. **Group**: Engine doesn't understand atoms or molecules but group of atom indexes instead. 
       A group is a set of atom indexes, allowing no indexes redundancy 
       within the same group definition. A Group instance can contain any set of indexes and as many atom indexes as needed. 
       Grouping atoms is essential to make clusters of atoms (residues, molecules, etc) evolve and move together. A group of 
       a single atom index can be used to make a single atom move separately from the others. Engine's 'groups' attribute 
       is a simple list of group instances containing all the desired and defined groups that one wants to move.
    #. **Group selector**: Engine requires a GroupSelector instance which is the artist that selects a group from the engine's
       groups list at every engine runtime step. Among other properties, depending on which group selector is used by the
       engine, a GroupSelector can allow weighting which means selecting groups more or less frequently than the others, 
       it can also allow selection recurrence and refinement of a single group, ordered and random selection is also possible.
    #. **Move generator**: Every group instance has its own MoveGenerator. Therefore every group of atoms when selected by 
       the engine's group selector at the engine's runtime can perform a customizable and different kind of moves. 
    #. **Constraint**: A constraint is a rule that controls certain aspect of the configuration upon moving groups. 
       Engine's 'constraints' attribute is a list of all defined and used constraint instances, it is 
       the judge that controls the evolution of the system by accepting or rejecting the move of a group. 
       If engine's constraints list is empty and contains no constraint definition, this will result
       in accepting all the generated moves.

Tetrahydrofuran simple example yet complete and straight to the point
=====================================================================
.. code-block:: python
    
    ## Tetrahydrofuran (THF) molecule sketch
    ## 
    ##              O
    ##   H41      /   \      H11
    ##      \  /         \  /
    ## H42-- C4    THF    C1 --H12
    ##        \  MOLECULE /
    ##         \         /
    ##   H31-- C3-------C2 --H21
    ##        /         \\
    ##     H32            H22 
    ##
    
    ## imports
    import numpy as np
    import matplotlib.pyplot as plt
    from fullrmc.Engine import Engine
    from fullrmc.Constraints.PairDistributionConstraints import PairDistributionConstraint
    from fullrmc.Constraints.DistanceConstraints import InterMolecularDistanceConstraint
    from fullrmc.Constraints.BondConstraints import BondConstraint
    from fullrmc.Constraints.AngleConstraints import BondsAngleConstraint
    from fullrmc.Constraints.ImproperAngleConstraints import ImproperAngleConstraint
    from fullrmc.Core.MoveGenerator import MoveGeneratorCollector
    from fullrmc.Generators.Translations import TranslationGenerator, TranslationAlongSymmetryAxisGenerator
    from fullrmc.Generators.Rotations import RotationGenerator, RotationAboutSymmetryAxisGenerator
    
    #   #####################################################################################   #
    #   ############################# DECLARE USEFUL VARIABLES ##############################   #
    experimentalDataPath = "thf_pdf.exp"
    structurePdbPath     = "thf.pdb"
    engineSavePath       = "thf_engine.rmc"
    
    #   #####################################################################################   #
    #   ################################# CREATE RMC SYSTEM #################################   #
    ## create and initialize engine
    ENGINE = Engine(pdb=structurePdbFile, constraints=None)
    ## set structure boundary conditions
    ENGINE.set_boundary_conditions(np.array([48.860,0,0, 0,48.860,0, 0,0,48.860]))
    ## create and add pair distribution constraint to the engine
    PDF_CONSTRAINT = PairDistributionConstraint(engine=None, experimentalData=experimentalDataPath, weighting="atomicNumber")
    ENGINE.add_constraints([PDF_CONSTRAINT])
    ## create and add intermolecular distances constraint to the engine
    EMD_CONSTRAINT = InterMolecularDistanceConstraint(engine=None)
    ENGINE.add_constraints([EMD_CONSTRAINT])
    ## create and add bonds constraint to the engine
    B_CONSTRAINT = BondConstraint(engine=None)
    ENGINE.add_constraints([B_CONSTRAINT])
    B_CONSTRAINT.create_bonds_by_definition( bondsDefinition={"THF": [('O' ,'C1' , 1.20, 1.70),
                                                                      ('O' ,'C4' , 1.20, 1.70),
                                                                      ('C1','C2' , 1.25, 1.90),
                                                                      ('C2','C3' , 1.25, 1.90),
                                                                      ('C3','C4' , 1.25, 1.90),
                                                                      ('C1','H11', 0.88, 1.16),('C1','H12', 0.88, 1.16),
                                                                      ('C2','H21', 0.88, 1.16),('C2','H22', 0.88, 1.16),
                                                                      ('C3','H31', 0.88, 1.16),('C3','H32', 0.88, 1.16),
                                                                      ('C4','H41', 0.88, 1.16),('C4','H42', 0.88, 1.16)] })
    ## create and add angles constraint to the engine
    BA_CONSTRAINT = BondsAngleConstraint(engine=None)
    ENGINE.add_constraints([BA_CONSTRAINT])
    BA_CONSTRAINT.create_angles_by_definition( anglesDefinition={"THF": [ ('O'  ,'C1' ,'C4' , 105, 125),
                                                                          ('C1' ,'O'  ,'C2' , 100, 120),
                                                                          ('C4' ,'O'  ,'C3' , 100, 120),
                                                                          ('C2' ,'C1' ,'C3' , 95 , 115),
                                                                          ('C3' ,'C2' ,'C4' , 95 , 115),
                                                                          # H-C-H angle
                                                                          ('C1' ,'H11','H12', 98 , 118),
                                                                          ('C2' ,'H21','H22', 98 , 118),
                                                                          ('C3' ,'H31','H32', 98 , 118),
                                                                          ('C4' ,'H41','H42', 98 , 118),
                                                                          # H-C-O angle
                                                                          ('C1' ,'H11','O'  , 100, 120),
                                                                          ('C1' ,'H12','O'  , 100, 120),
                                                                          ('C4' ,'H41','O'  , 100, 120),
                                                                          ('C4' ,'H42','O'  , 100, 120),                                                                           
                                                                          # H-C-C
                                                                          ('C1' ,'H11','C2' , 103, 123),
                                                                          ('C1' ,'H12','C2' , 103, 123),
                                                                          ('C2' ,'H21','C1' , 103, 123),
                                                                          ('C2' ,'H21','C3' , 103, 123),
                                                                          ('C2' ,'H22','C1' , 103, 123),
                                                                          ('C2' ,'H22','C3' , 103, 123),
                                                                          ('C3' ,'H31','C2' , 103, 123),
                                                                          ('C3' ,'H31','C4' , 103, 123),
                                                                          ('C3' ,'H32','C2' , 103, 123),
                                                                          ('C3' ,'H32','C4' , 103, 123),
                                                                          ('C4' ,'H41','C3' , 103, 123),
                                                                          ('C4' ,'H42','C3' , 103, 123) ] })
    ## create and add improper angles constraint to the engine keeping THF molecules' atoms in the plane
    IA_CONSTRAINT = ImproperAngleConstraint(engine=None)
    ENGINE.add_constraints([IA_CONSTRAINT])
    IA_CONSTRAINT.create_angles_by_definition( anglesDefinition={"THF": [ ('C2','O','C1','C4', -15, 15),
                                                                          ('C3','O','C1','C4', -15, 15) ] })
    ## initialize constraints data
    ENGINE.initialize_used_constraints()
    ## Uncomment in order not to use a constraint in the next engine run
    #PDF_CONSTRAINT.set_used(False)
    #EMD_CONSTRAINT.set_used(False)
    #B_CONSTRAINT.set_used(False)
    #BA_CONSTRAINT.set_used(False)
    #IA_CONSTRAINT.set_used(False)
    ## initialize constraints data
    ENGINE.initialize_used_constraints()
    
    #   #####################################################################################   #
    #   ################################# RUN RMC ON ATOMS ##################################   #
    ENGINE.run(numberOfSteps=100000, saveFrequency=1000, savePath=engineSavePath)
    
    #   #####################################################################################   #
    #   ############################### RUN RMC ON MOLECULES ################################   #
    ## set groups as molecules instead of atoms
    ENGINE.reset_groups_as_molecules()  
    # set moves generators to all groups to a collection of random translations and rotations
    for g in ENGINE.groups:
        mg = MoveGeneratorCollector(collection=[TranslationGenerator(),RotationGenerator()], randomize=True)
        g.set_move_generator( mg )
    ## Uncomment to use any of the following moves generators
    ## Also other moves generators can be used to achieve a better fit for instance:
    #[g.set_move_generator(TranslationAlongSymmetryAxisGenerator(axis=0)) for g in ENGINE.groups]
    #[g.set_move_generator(TranslationAlongSymmetryAxisGenerator(axis=1)) for g in ENGINE.groups]
    #[g.set_move_generator(TranslationAlongSymmetryAxisGenerator(axis=2)) for g in ENGINE.groups]
    #[g.set_move_generator(RotationAboutSymmetryAxisGenerator(axis=0)) for g in ENGINE.groups]
    #[g.set_move_generator(RotationAboutSymmetryAxisGenerator(axis=1)) for g in ENGINE.groups]
    #[g.set_move_generator(RotationAboutSymmetryAxisGenerator(axis=2)) for g in ENGINE.groups]
    ## Molecular constraints are not necessary any more because groups are set to molecules.
    ## At every engine step a whole molecule is rotate or translated therefore its internal
    ## distances and properties are safe from any changes. At any time constraints can be 
    ## turn on again using the same method with a True flag. e.g. B_CONSTRAINT.set_used(True)
    B_CONSTRAINT.set_used(False)
    BA_CONSTRAINT.set_used(False)
    IA_CONSTRAINT.set_used(False)
    ## run engine and perform RMC on molecules
    ENGINE.run(numberOfSteps=100000, saveFrequency=1000, savePath=engineSavePath)
    
    
    #   #####################################################################################   #
    #   ################################### PLOT TOTAL GR ###################################   #
    totalGR = ENGINE.constraints[0].get_constraint_value()["pdf_total"]
    expData = ENGINE.constraints[0].experimentalPDF
    plt.plot(ENGINE.constraints[0].experimentalDistances, expData, 'ro', label="experimental", markersize=7.5, markevery=1 )
    plt.plot(ENGINE.constraints[0].shellsCenter, totalGR, 'k', linewidth=2.0,  markevery=5, label="total" )
    plt.legend()
    plt.show()  

The result shown in the figures herein is obtained by running fullrmc Engine for several hours on molecular groups.
Position optimization is achieved by using a RecursiveGroupSelector to refine every selected group position
and alternating groups moves generators. RotationAboutSymmetryAxisGenerator is used to fit the ring orientation, 
then TranslationAlongSymmetryAxisGenerator is used to translate molecules along meaningful directions. 
At the end, groups a reset to single atom index and RandomSelector is used to select groups randomly.
the Engine is run for additional several hours to refine atoms positions separately.

+----------------------------------------+----------------------------------------+----------------------------------------+ 
|.. figure:: thfBox.png                  |.. figure:: beforeFit.png               |.. figure:: afterFit.png                | 
|   :width: 300px                        |   :width: 300px                        |   :width: 300px                        | 
|   :height: 200px                       |   :height: 200px                       |   :height: 200px                       |
|   :align: left                         |   :align: left                         |   :align: left                         | 
|                                        |                                        |                                        |
|   a) Structure containing 800          |   b) Initial pair distribution function|   c) pair distribution function        |
|   Tetrahydrofuran randomly generated.  |   calculated before any fitting.       |   calculated after about 20 hours of   |
|                                        |                                        |   Engine runtime.                      |
+----------------------------------------+----------------------------------------+----------------------------------------+


Installation
============ 
fullrmc requires:
#. Python (>= 2.6 and < 3),
#. NumPy (lowest version tested is 1.7.1),
#. cython (lowest version tested is 0.21.1),
#. matplotlib (lowest version tested is 1.4),
#. pdbParser (lowest version tested is 0.1.2),
#. pysimplelog (lowest version tested is 0.1.7).

**Installation using pip:**\n
numpy and cython must be installed and updated manually. 
   
   .. code-block:: bash  
    
       pip install -U "numpy>=1.7.1"
       pip install -U "cython>=0.21.1"
       
When you already have a working installation of numpy and cython.
   
   .. code-block:: bash  
    
       pip install fullrmc

**Installation by cloning github repository:**\n
   * Ensure all fullrmc required packages are installed:
    
    .. code-block:: python
        
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
           
   * Locate python's site-packages using:
     
     .. code-block:: python
     
        import os
        os.path.join(os.path.dirname(os.__file__), 'site_packages')

   * Navigate to site_packages folder and clone git repository:\n
   
    .. code-block:: bash
       
       cd .../site_packages
       git clone https://github.com/bachiraoun/fullrmc.git   

   * Compile fullrmc Extension files. Change directory to .../site_packages/fullrmc/Extensions:\n
      
    .. code-block:: bash  
        cd .../site_packages/fullrmc/Extensions
        python setup.py build_ext --inplace 
        
"""
# get package info
from __pkginfo__ import __version__, __author__, __email__

def get_version():
    return __version__ 

def get_author():
    return __author__     
 
def get_email():
    return __email__   
    
    
    