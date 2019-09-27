import xml.etree.ElementTree as ET
from Include.console_application.abstract_functions import AbstractFFunction, AbstractGFunction

class XMLFFunction(AbstractFFunction):
    incrIndexA = 0

    def __init__(self, data):
        self.__data = data

    def getAList(self):
        temp = []
        for row in self.__data.findall('./ACoefs/ACoef'):
            acoefIndex = int(row.get('Index'))
            acoefValue = float(row.get('Value'))
            temp.insert(acoefIndex, acoefValue)
        return temp

    def aCount(self):
        return len(self.__data.findall('./ACoefs/ACoef'))

    def getA(self, index):
        acoef = self.__data.findall(".//*[@Index='" + str(index) + "']")
        return float(acoef[0].get('Value'))

    def setA(self, index, a):
        try:
            acoef = self.__data.findall(".//*[@Index='" + str(index) + "']")
            acoef[0].set('Value', str(a))
        except IndexError:
            print('setA: List index out of range!')

    def addA(self, a):
        if not self.__data.find('ACoefs') and self.incrIndexA == 0:
            # create ACoefs sub-root
            aCoefs = ET.SubElement(self.__data, 'ACoefs')
            # create ACoef with 0 index
            ET.SubElement(aCoefs, 'ACoef', Index=str(self.incrIndexA), Value=str(a))
        else:
            ET.SubElement(self.__data.find('ACoefs'), 'ACoef', Index=str(self.incrIndexA), Value=str(a))
        self.incrIndexA += 1

class XMLGFunction(AbstractGFunction):
    incrIndexXY = 0

    def __init__(self, data):
        self.__data = data
        self.fromVal = None
        self.toVal = None

    def getXYList(self):
        temp = []

        for row in self.__data.findall('./XYPoints/XYPoint'):
            xypointXValue = float(row.get('X'))
            xypointYValue = float(row.get('Y'))
            temp.append([xypointXValue, xypointYValue])
            # xypointIndex = int(row.get('Index'))
            # temp.insert(xypointIndex, [xypointXValue, xypointYValue])
        return temp

    def xyCount(self):
        return len(self.getXYList())

    def getX(self, index):
        acoef = self.__data.findall(".//XYPoint[@Index='" + str(index) + "']")
        return float(acoef[0].get('X'))

    def getY(self, index):
        acoef = self.__data.findall(".//XYPoint[@Index='" + str(index) + "']")
        return float(acoef[0].get('Y'))

    def setX(self, index, x):
        acoef = self.__data.findall(".//XYPoint[@Index='" + str(index) + "']")
        acoef[0].set('X', str(x))

    def setY(self, index, y):
        acoef = self.__data.findall(".//XYPoint[@Index='" + str(index) + "']")
        acoef[0].set('Y', str(y))

    def setXY(self, index, x, y):
        acoef = self.__data.findall(".//XYPoint[@Index='" + str(index) + "']")
        acoef[0].set('X', str(x))
        acoef[0].set('Y', str(y))

    def addXY(self, x, y):
        if not self.__data.find('XYPoints') and self.incrIndexXY == 0:
            # create XYPoints sub-root
            xyPoints = ET.SubElement(self.__data, 'XYPoints')
            # create XYPoint with 0 index
            ET.SubElement(xyPoints, 'XYPoint', Index=str(self.incrIndexXY), X=str(x), Y=str(y))
        else:
            ET.SubElement(self.__data.find('XYPoints'), 'XYPoint', Index=str(self.incrIndexXY), X=str(x), Y=str(y))
        self.incrIndexXY += 1

    def getFrom(self):
        temp = []
        aValues = self.__data.findall('./XYPoints/XYPoint')
        # print("Type of array in getFrom ", type(aValues))
        for row in aValues:
            xypointIndex = int(row.get('Index'))
            xypointXValue = float(row.get('X'))
            temp.append(xypointXValue)

        print('From val+', min(temp))
        return min(temp)
        # pass

    def getTo(self):
        temp = []
        aValues = self.__data.findall('./XYPoints/XYPoint')
        # print("Type of array in getFrom ", type(aValues))
        for row in aValues:
            xypointIndex = int(row.get('Index'))
            xypointXValue = float(row.get('X'))
            temp.append(xypointXValue)

        print('To val+', max(temp))
        return max(temp)


