#from itertools import Combination

from SymClass import Addition, Multiply, Division, Sum
from SymClass import Constant, GeneralVar, DistVar, SumVar



#===============================================================
class UnboundedIndicie(Exception):
    pass
#===============================================================
class SymTree():
    #-----------------------------------------------------------
    def __init__(self):
        self.leaftypes = [Constant, GeneralVar]
        self.headnode = Sum()
        self.indicielist = ["i"]
        self.indicieranges = {
                            "i": [0, 10],
                             }
#        termlist = [GeneralVar(parentNode=self.headnode), Constant(2.0, parentNode=self.headnode)]
        termlist = [SumVar(indicies=self.indicielist, parentNode=self.headnode)]
        self.headnode.setterms(termlist)
        self.headnode.setinicieranges(self.indicieranges)

    #-----------------------------------------------------------
    def __str__(self):
        return str(self.headnode)

    #-----------------------------------------------------------
    def evaluate(self):
        indicies = self.headnode.getfreeindicie()
        if len(indicies) > 0:
            raise UnboundedIndicie("Sumation Index defined, but not used by a sumation node")

        coordval = {}
        iLow, iHigh = tuple(self.indicieranges["i"])
        for i in range(iLow, iHigh+1):
            coordval["x_%s"%(i)] = i

#        for key in coordval:
#            print(key, coordval[key])
        indicies = {}


        return self.headnode.evaluate(indicies,coordval)
    #-----------------------------------------------------------
#===============================================================

if __name__ == "__main__":
    test = SymTree()
    val = test.evaluate()
    print(val)
    print(test)
