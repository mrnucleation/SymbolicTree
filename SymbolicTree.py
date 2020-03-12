#from itertools import Combination

from SymClass import Addition, Multiply, Division
from SymClass import Constant, GeneralVar, DistVar



#===============================================================
class UnboundedIndicie(Exception):
    pass
#===============================================================
class SymTree():
    #-----------------------------------------------------------
    def __init__(self):
        self.leaftypes = [Constant, GeneralVar]
        self.headnode = Multiply()
        self.indicielist = ["i"]
        self.indicieranges = {
                            "i": [0.0, 2.0],
                             }
        termlist = [Constant(-10.5, parentNode=self.headnode), Constant(2.0, parentNode=self.headnode)]
        self.headnode.setterms(termlist)

    #-----------------------------------------------------------
    def __str__(self):
        return str(self.headnode)

    #-----------------------------------------------------------
    def evaluate(self):
        indicies = self.headnode.getfreeindicie()
        if len(indicies) > 0:
            raise UnboundedIndicie("Sumation Index defined, but not used by a sumation node")

        coordval = {
                    "x": 2.0,
                   }
        indicies = {}


        return self.headnode.evaluate(indicies,coordval)
    #-----------------------------------------------------------
#===============================================================

if __name__ == "__main__":
    test = SymTree()
    val = test.evaluate()
    print(val)
    print(test)
