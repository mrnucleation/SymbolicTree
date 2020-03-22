from random import choice, random, seed
from time import time
from copy import deepcopy
from datetime import datetime

import sys
import numpy as np

seed(datetime.now())

#================================================
class MissingParameters(Exception):
    pass
#================================================
class SymbolicData(object):
    #------------------------------------------------
    def __init__(self, , evaluator=None, lbounds=None, ubounds=None):

        
        if evaluator is None:
            self.evaluator = None
        else:
            self.evaluator = evaluator

    #----------------------------------------------------
    def cleanup(self, node):
        return
    #----------------------------------------------------
    def __eq__(self, dataobj2):
        str2 = dataobj2.getstructure()
        return str2 == self.parameters
    #----------------------------------------------------
    def __str__(self):
        outstr = ' '.join([str(x) for x in self.parameters])
        return outstr

    #------------------------------------------------
    def newdataobject(self):
        newobj = SymbolicData(parameters=self.parameters, lbounds=self.lbounds, ubounds=self.ubounds, evaluator=self.evaluator)
        return newobj

    #------------------------------------------------
    def perturbate(self, node=None, parOnly=False, forceuniform=True):
        if not parOnly:
            newobj = SymbolicData(evaluator=self.evaluator)
            return newobj
        else:
            return selection
    #----------------------------------------------------
    def crossover(self,  pardata, node=None, parnode=None):

        newobj = SymbolicData(evaluator=self.evaluator)
        return newobj
    #----------------------------------------------------
    def runsim(self, playouts=1, moves=3, mass=True, node=None):

        _, playoutEList = node.getplayouts()
        nPrev = len(playoutEList)
        structlist = []
        energylist = []
        if node is not None:
            print("Node Depth: %s"%(node.getdepth()))
        for playout in range(playouts):
            newlist = self.parameters
            for iMove in range(moves):
                tempstr = None
                while tempstr is None:
                    tempstr = self.perturbate(parOnly=True, node=node, forceuniform=True)
                newlist = tempstr
            structlist.append(newlist)
            energy = self.evaluator(newlist)
            energylist.append(energy)
        for playout, energy in enumerate(energylist):
                print("Playout %s Result: %s"%(nPrev+playout+1, energy))


        return energylist, structlist
    #----------------------------------------------------
    def findplayouts(self, node=None):
        return energylist, structlist
    #----------------------------------------------------
    def computescore(self, node=None):
        self.score = self.evaluator(self.parameters)
        return self.score
    #----------------------------------------------------
    def getscore(self):
        return self.score
    #----------------------------------------------------
    def setscore(self, score):
        self.score = score
    #----------------------------------------------------
    def getuniqueness(self, inlist=None, node=None, nodelist=None):
        return 1.0
    #----------------------------------------------------
    def minimize(self, node=None):
        from GAOptimizer import GAOpt
        newobj, score = GAOpt(self, node=node, ngenerations=50)
        print("Post Minimization Score: %s"%(score))
        return newobj, score
    #----------------------------------------------------
    def getstructure(self):
        return self.parameters
    #----------------------------------------------------
    def setstructure(self, parameters):
    #----------------------------------------------------
    def setevaluator(self, evalfunc):
        self.evaluator = evalfunc

    #----------------------------------------------------
    def convertstr(self, instr):

        return par

    #----------------------------------------------------
#================================================
