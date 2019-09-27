from Include.console_application.abstract_functions import AbstractFFunction, AbstractGFunction

class ArrayFFunction(AbstractFFunction):

    def __init__(self, data):
        self.coefData = data

    def getAList(self):
        return self.coefData

    def aCount(self):
        return len(self.coefData)

    def getA(self, index):
        return self.coefData[index]

    def setA(self, index, a):
        self.coefData[index] = a

    def addA(self, a):
        self.coefData.append(a)


class ArrayGFunction(AbstractGFunction):
    def __init__(self, data):
        self.pointsData = data

    def getXYList(self):
        return self.pointsData

    def xyCount(self):
        # print(len("arraysize", self.pointsData))
        return len(self.pointsData)

    def getX(self, index):
        return float(self.pointsData[index][0])

    def getY(self, index):
        return float(self.pointsData[index][1])

    def setX(self, index, x):
        self.pointsData[index][0] = x

    def setY(self, index, y):
        self.pointsData[index][1] = y

    def setXY(self, index, x, y):
        self.pointsData[index][0] = x
        self.pointsData[index][1] = y

    def addXY(self, x, y):
        self.pointsData.append([x, y])

    def getFrom(self):
        temp = []
        for els in self.pointsData:
            temp.append(float(els[0]))
        return min(temp)

    def getTo(self):
        temp = []
        for els in self.pointsData:
            temp.append(float(els[0]))
        return max(temp)