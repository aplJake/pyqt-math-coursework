from abc import ABC, abstractmethod
import math

class PolynomialEquation:
    def __init__(self):
        self.__roots = None
        self.__fromVal = None
        self.__toVal = None

    def __str__(self):
        if not self.getRoots():
            return 'You still haven`t solve the equation'
        else:
            eqRoots = self.getRoots()
            if len(eqRoots) == 0:
                return 'Equation has 0 roots'
            elif len(eqRoots) == 1:
                return f'Eqution root is {str(eqRoots[0][0])} {str(eqRoots[0][1])}'
            elif len(eqRoots) > 2 and len(eqRoots) < 10:
                s = 'Equation roots: '
                for i in range(len(eqRoots)):
                    s += str(eqRoots[i][0]) +' ' + str(eqRoots[i][1])
                return s
            else:
                return 'Equation has infinite number of roots'

    def getF(self):
        return self.__f

    def getG(self):
        return self.__g

    def setF(self, f):
        self.__f = f
        return self.clearRoots()

    def setG(self, g):
        self.__g = g
        return self.clearRoots()

    def setEquation(self, f, g):
        self.__f = f
        self.__g = g
        return self.clearRoots()

    def clearRoots(self):
        self.__roots = []
        return self

    def getFromVal(self):
        return self.__fromVal

    def getToVal(self):
        return self.__toVal

    # a, b is general bounds setted by user
    def solve(self, a, b, eps = 0.00001):
        print('\n23Solving equation...')
        aGBound = float(self.getG().getFrom())
        bGBound = float(self.getG().getTo())
        if a < b and aGBound < bGBound:
            if b < aGBound or a > bGBound:
                print("No solutions")
                raise ValueError
            else:
                if a < aGBound and b >= aGBound and b <= bGBound:
                    self.__fromVal = aGBound
                    self.__toVal = b
                elif b > bGBound and a >= aGBound and a <= bGBound:
                    self.__fromVal = a
                    self.__toVal = bGBound
                elif a <= aGBound and b >= bGBound:
                    self.__fromVal = aGBound
                    self.__toVal = bGBound
                elif a >= aGBound and b <= bGBound:
                    self.__fromVal = a
                    self.__toVal = b
                else:
                    raise ValueError
        else:
            raise ValueError

        dichFrom = self.__fromVal
        dichTo = self.__toVal
        while dichFrom < dichTo-1:
            delta = 1
            x = dichFrom
            # check when the sign changes
            y0 = self.yVal(x)
            y1 = self.yVal(x + delta)
            if (y0 < 0 and y1 > 0) or (y0 > 0 and y1 < 0):
                root = self.dichotomy(x, x + delta)
                self.__roots.append([root, self.yVal(root)])
            dichFrom += delta
        return self

    def yVal(self, x):
        return self.__f.function(x) - self.__g.function(x)

    def dichotomy(self, fromVal, toVal, eps=0.00001):
        x = 0
        while math.fabs(toVal - fromVal) > eps:
            x = (fromVal + toVal) / 2
            if self.yVal(fromVal) * self.yVal(x) > 0:
                fromVal = x
            else:
                toVal = x
        return x

    def getRoots(self):
        return self.__roots
