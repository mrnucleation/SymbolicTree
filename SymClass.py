from math import cos, sin
#============================================================
class IndexCountMismatch(Exception):
    pass
#============================================================
class RepeatedSumIndex(Exception):
    '''
     Exception: Implies the same sumation index.
    '''
    pass
#============================================================
class Expression():
    #--------------------------------------
    def __init__(self, parentNode=None):
        if parentNode is not None:
            self.parent = parentNode
            self.depth = parentNode.getdepth() + 1
        else:
            self.parent = None
            self.__depth = 0
        self.status = "branch"
    #--------------------------------------
    def getdepth(self):
        return self.__depth
    #--------------------------------------
    def getparent(self):
        '''
         Returns the parent node of this node. 
        '''
        return self.parent
    #--------------------------------------
    def getlineage(self, layer=0):
        '''
         Returns a list of nodes starting from the node who initiated the call
         tracing the tree back up to the head node. The list will be sorted
         in terms of depth with the deepest node listed first.
        '''
        if self.parent is None:
            return [self]

        parentlineage = self.parent.getlineage(layer=layer+1)
        outlineage = [self]+parentlineage
        if layer == 0:
            outlineage = sorted(outlineage, key=lambda x:x.getdepth(), reverse=True)

        return outlineage

    #--------------------------------------
    def setinicieranges(self, indicierange):
        self.indicierange = indicierange

#============================================================
class Sum(Expression):
    #--------------------------------------------------------
    def __init__(self, sterm, indicie, parentNode=None):
        Expression.__init__(self,parentNode)
        self.val = val
        self.sumindicie = indicie
        self.sterm = sterm

    #--------------------------------------------------------
    def __str__(self):
        return "Sum_%s:(%s)"%(self.sumindicie, str(self.sterm))
    #--------------------------------------------------------
    def evaluate(self, indicies, coordval):

        if self.sumindicie in indicies:
            raise RepeatedSumIndex

        newindicies = indicies.copy()

        lowI, highI = tuple(self.indicierange[self.sumindicie])
        sumval = 0.0
        for iSum in range(lowI, highI):
            newindicies[self.sumindicie] = iSum
            val = self.sterm.evaluate(newindicies, coordval)
            sumval += val


        return sumval
    #--------------------------------------------------------
    def getnodelist(self):
        '''
         Returns a python list containing this node and all of it's child nodes via recursion.
        '''
        totallist = []
        sublist = self.sterm.getnodelist()
        totallist = totallist + sublist
        return [self] + totallist
    #--------------------------------------------------------
    def getfreeindicie(self):
        '''
         Since a Sum effectively removes an indicie.  Thus it needs
         to modify the list accordingly
        '''
        indicies = self.sterm.getfreeindicie()
        return list(filter((self.sumindicie).__ne__, indicies))
    #--------------------------------------------------------

#============================================================
class Constant(Expression):
    #--------------------------------------------------------
    def __init__(self, val, parentNode=None):
        Expression.__init__(self,parentNode)
        self.val = val
        self.status = "leaf"
    #--------------------------------------------------------
    def __str__(self):
        return "%s"%(self.val)
    #--------------------------------------------------------
    def evaluate(self, indicies, coordval):
        return self.val
    #--------------------------------------------------------
    def getnodelist(self):
        return [self]
    #--------------------------------------------------------
    def getfreeindicie(self):
        return []
    #--------------------------------------------------------
#============================================================
class ParameterVar(Expression):
    #--------------------------------------------------------
    def __init__(self, indicies, parentNode=None):
        Expression.__init__(self,parentNode)
        self.indicies = indicies
        self.__varname = "c_%s"%(''.join([str(x) for x in incidies]))
        self.status = "leaf"
    #--------------------------------------------------------
    def __str__(self):
        return self.__varname
    #--------------------------------------------------------
    def evaluate(self, indicies, coordval):
        return coordval[self.__varname]
    #--------------------------------------------------------
    def getnodelist(self):
        return [self]
    #--------------------------------------------------------
    def getfreeindicie(self):
        return self.indicies
    #--------------------------------------------------------


#============================================================
class GeneralVar(Expression):
    #--------------------------------------------------------
    def __init__(self,  varname="x", parentNode=None):
        Expression.__init__(self,parentNode)
        self.__varname = varname
        self.status = "leaf"
    #--------------------------------------------------------
    def __str__(self):
        return self.__varname
    #--------------------------------------------------------
    def evaluate(self, indicies, coordval):
        return coordval[self.__varname]
    #--------------------------------------------------------
    def getnodelist(self):
        return [self]
    #--------------------------------------------------------
    def getfreeindicie(self):
        return []
    #--------------------------------------------------------
#============================================================
class SumVar(GeneralVar):
    #--------------------------------------------------------
    def __init__(self, indicies=None, varname="x", parentNode=None):
        Expression.__init__(self,parentNode)
        self.indicies = indicies
        self.__varname = varname+"_%s"%(''.join([str(x) for x in incidies]))
        self.status = "leaf"
    #--------------------------------------------------------
    def __str__(self):
        return self.__varname
    #--------------------------------------------------------
    def evaluate(self, indicies, coordval):
        return coordval[self.__varname]
    #--------------------------------------------------------
    def getnodelist(self):
        return [self]
    #--------------------------------------------------------
    def getfreeindicie(self):
        return self.indicies
    #--------------------------------------------------------


#============================================================
class DistVar(SumVar):
    #--------------------------------------------------------
    def __init__(self, indicies, parentNode=None):
#        Expression.__init__(self,parentNode)
        SumVar.__init__(self, indicies=indicies, varname="r", parentNode=parentNode)
        if len(indicies) != 2:
            raise IndexCountMismatch
    #--------------------------------------------------------
#============================================================
class AngleVar(SumVar):
    #--------------------------------------------------------
    def __init__(self, indicies, parentNode=None):
        SumVar.__init__(self, indicies=indicies, varname="A", parentNode=parentNode)
        if len(indicies) != 3:
            raise IndexCountMismatch
    #--------------------------------------------------------
#============================================================
class TwoTermExpression(Expression):
    #--------------------------------------------------------
    def __init__(self, lterm=None, rterm=None, parentNode=None):
        Expression.__init__(self,parentNode)
        self.lterm = lterm
        self.rterm = rterm
    #--------------------------------------------------------
    def __str__(self):
        return "(%s+%s)"%(str(self.lterm), str(self.rterm))

    #--------------------------------------------------------
    def setterms(self, termlist):
        self.lterm = termlist[0]
        self.rterm = termlist[1]
    #--------------------------------------------------------
    def evaluate(self, indicies, coordval):
        return self.lterm.evaluate(indicies, coordval) + self.rterm.evaluate(indicies, coordval)
    #--------------------------------------------------------
    def getnodelist(self):
        '''
         Returns a python list containing this node and all of it's child nodes via recursion.
        '''
        totallist = []
        sublist = self.lterm.getnodelist()
        totallist = totallist + sublist
        sublist = self.rterm.getnodelist()
        totallist = totallist + sublist
        return [self] + totallist
    #--------------------------------------------------------
    def getfreeindicie(self):
        return self.lterm.getfreeindicie() + self.rterm.getfreeindicie()
    #--------------------------------------------------------
    def getfreevariables(self):
        totallist = []
        sublist = self.lterm.getfreevariables()
        totallist = totallist + sublist
        sublist = self.rterm.getfreevariables()
        totallist = totallist + sublist
        return [self] + totallist
    #--------------------------------------
    def setinicieranges(self, indicierange):
        self.indicierange = indicierange
        self.lterm.setinicieranges(indicierange)
        self.rterm.setinicieranges(indicierange)
    #--------------------------------------------------------

#============================================================
class Addition(TwoTermExpression):
    #--------------------------------------------------------
    def __init__(self, lterm=None, rterm=None, parentNode=None):
        Expression.__init__(self,parentNode)
        self.lterm = lterm
        self.rterm = rterm
    #--------------------------------------------------------
    def __str__(self):
        return "(%s+%s)"%(str(self.lterm), str(self.rterm))
    #--------------------------------------------------------
    def evaluate(self, indicies, coordval):
        return self.lterm.evaluate(coordval,vardict) + self.rterm.evaluate(coordval,vardict)
    #--------------------------------------------------------

#============================================================
class Multiply(TwoTermExpression):
    #--------------------------------------------------------
    def __init__(self, lterm=None, rterm=None, parentNode=None):
        Expression.__init__(self,parentNode)
        self.lterm = lterm
        self.rterm = rterm
    #--------------------------------------------------------
    def __str__(self):
        return "%s*%s"%(str(self.lterm), str(self.rterm))
    #--------------------------------------------------------
    def evaluate(self, indicies, coordval):
        return self.lterm.evaluate(indicies, coordval) * self.rterm.evaluate(indicies, coordval)
    #--------------------------------------------------------

#============================================================
class Division(TwoTermExpression):
    #--------------------------------------------------------
    def __init__(self, lterm=None, rterm=None, parentNode=None):
        Expression.__init__(self,parentNode)
        self.lterm = lterm
        self.rterm = rterm
    #--------------------------------------------------------
    def __str__(self):
        return "%s/(%s)"%(str(self.lterm), str(self.rterm))
    #--------------------------------------------------------
    def evaluate(self, indicies, coordval):
        return self.lterm.evaluate(coordval,vardict) / self.rterm.evaluate(coordval,vardict)
    #--------------------------------------------------------

#============================================================
class Power(TwoTermExpression):
    #--------------------------------------------------------
    def __init__(self, lterm=None, rterm=None, parentNode=None):
        Expression.__init__(self,parentNode)
        self.lterm = lterm
        self.rterm = rterm
    #--------------------------------------------------------
    def __str__(self):
        return "%s^(%s)"%(str(self.lterm), str(self.rterm))
    #--------------------------------------------------------
    def evaluate(self, indicies, coordval):
        return self.lterm.evaluate(coordval,vardict) ** self.rterm.evaluate(coordval,vardict)
    #--------------------------------------------------------

#============================================================
class CosFunc(Expression):
    #--------------------------------------------------------
    def __init__(self, cterm=None, parentNode=None):
        Expression.__init__(self,parentNode)
        self.cterm = cterm
    #--------------------------------------------------------
    def __str__(self):
        return "cos(%s)"%(str(self.cterm))
    #--------------------------------------------------------
    def evaluate(self,coordval,vardict):

        return cos(self.cterm.evaluate(coordval,vardict))
    #--------------------------------------------------------
    def getnodelist(self):
        '''
         Returns a python list containing this node and all of it's child nodes via recursion.
        '''
        totallist = []
        sublist = self.cterm.getnodelist()
        totallist = totallist + sublist
        return [self] + totallist
    #--------------------------------------------------------
    def getfreeindicie(self):
        return self.cterm.getfreeindicie()
    #--------------------------------------------------------
#============================================================
class SinFunc(Expression):
    #--------------------------------------------------------
    def __init__(self, cterm=None, parentNode=None):
        Expression.__init__(self,parentNode)
        self.cterm = cterm
    #--------------------------------------------------------
    def __str__(self):
        return "sin(%s)"%(str(self.cterm))
    #--------------------------------------------------------
    def evaluate(self, indicies, coordval):
        return sin(self.sterm.evaluate(coordval,vardict))
    #--------------------------------------------------------
    def getnodelist(self):
        '''
         Returns a python list containing this node and all of it's child nodes via recursion.
        '''
        totallist = []
        sublist = self.sterm.getnodelist()
        totallist = totallist + sublist
        return [self] + totallist
    #--------------------------------------------------------
    def getfreeindicie(self):
        return self.sterm.getfreeindicie()
    #--------------------------------------------------------
#============================================================
