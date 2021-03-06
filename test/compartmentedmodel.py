# Test compartmented model basic functions
#
# Copyright (C) 2017 Simon Dobson
# 
# This file is part of epydemic, epidemic network simulations in Python.
#
# epydemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# epydemic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with epydemic. If not, see <http://www.gnu.org/licenses/gpl.html>.

from epydemic import *

import epyc
import unittest
import networkx
import traceback

class CompartmentedModelTest(unittest.TestCase):

    def setUp( self ):
        '''Set up the experimental parameters and experiment.'''
        self._er = networkx.erdos_renyi_graph(1000, 0.005)
        self._params = dict(pInfect = 0.1,
                            pInfected = 0.01,
                            pRemove = 0.05)
       
    def testPopulation( self ):
        '''Test populating a model.'''
        m = SIR()
        e = CompartmentedStochasticDynamics(m, self._er)
        e.setUp(self._params)
                
    def testLoci( self ):
        '''Test we can populate loci correctly.'''
        m = SIR()
        g = networkx.Graph()
        g.add_edges_from([ (1, 2), (2, 3), (1, 4), (3, 4) ])
        e = CompartmentedStochasticDynamics(m, g)
        params = dict(pInfect = 0.1,
                      pInfected = 1.0,    # infect all nodes initially
                      pRemove = 0.05)
        e.setUp(params)

        # keep track of the other compartments as well
        e._model.addLocus(SIR.SUSCEPTIBLE)
        e._model.addLocus(SIR.REMOVED)
        
        # all nodes in I
        self.assertItemsEqual(e._model._loci[SIR.INFECTED].elements(), [ 1, 2, 3, 4 ])

        # one node from I into S, two edges into SI
        m.changeCompartment(e.network(), 1, SIR.SUSCEPTIBLE)
        self.assertItemsEqual(e._model._loci[SIR.INFECTED].elements(), [ 2, 3, 4 ])
        self.assertItemsEqual(e._model._loci[SIR.SUSCEPTIBLE].elements(), [ 1 ])
        self.assertItemsEqual(e._model._loci[SIR.SI].elements(), [ (1, 2), (1, 4) ])

        # recover the infected node
        m.changeCompartment(e.network(), 1, SIR.REMOVED)
        self.assertItemsEqual(e._model._loci[SIR.INFECTED].elements(), [ 2, 3, 4 ])
        self.assertItemsEqual(e._model._loci[SIR.SUSCEPTIBLE].elements(), [])
        self.assertItemsEqual(e._model._loci[SIR.REMOVED].elements(), [ 1 ])
        self.assertItemsEqual(e._model._loci[SIR.SI].elements(), [ ])        
