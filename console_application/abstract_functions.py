from abc import ABC, abstractmethod
from Include.console_application.extended_function import ExtendedFunction
import math

class AbstractFFunction(ExtendedFunction):

    @abstractmethod
    def getAList(self): pass

    @abstractmethod
    def aCount(self): pass

    @abstractmethod
    def getA(self, index): pass

    @abstractmethod
    def setA(self, index, a): pass

    @abstractmethod
    def addA(self, a): pass

    def function(self, x):
        resultSum = 0
        eq = ''
        if self.aCount() > 0:
            ir = self.aCount()-1
            for i in range(self.aCount()):

                resultSum += (math.pow(x, ir) * float(self.getA(i)))
                ir -= 1
            return resultSum
        else:
            return None

class AbstractGFunction(ExtendedFunction):

    @abstractmethod
    def getXYList(self): pass

    @abstractmethod
    def xyCount(self): pass

    @abstractmethod
    def getX(self, index): pass

    @abstractmethod
    def getY(self, index): pass

    @abstractmethod
    def setX(self, index, x): pass

    @abstractmethod
    def setY(self, index, y): pass

    @abstractmethod
    def setXY(self, index, x, y): pass

    @abstractmethod
    def addXY(self, x, y): pass

    # bounds for function
    @abstractmethod
    def getFrom(self): pass

    @abstractmethod
    def getTo(self): pass



    def function(self, x):
        z = 0
        for j in range(self.xyCount()):
            p1 = 1
            p2 = 1
            for i in range(self.xyCount()):
                if i == j:
                    p1 = p1 * 1
                    p2 = p2 * 1
                else:
                    p1 = p1 * (x - self.getX(i))
                    p2 = p2 * (self.getX(j) - self.getX(i))

            if p2 == 0:
                print('Division by zero. Please change the value.')
                raise ZeroDivisionError
            else:
                z = z + self.getY(j) * p1 / p2
        # print('AGF', 'x=', x, 'y=', z)
        return z

