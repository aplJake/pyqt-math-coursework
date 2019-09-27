from Include.console_application.array_functions import ArrayFFunction, ArrayGFunction
from Include.console_application.polynomial_equation import PolynomialEquation

from PyQt5.QtGui import QStandardItemModel, QStandardItem

class ArrayPolynomial(PolynomialEquation):
    def __init__(self):
        super(ArrayPolynomial, self).__init__()
        self.fromBound = None;
        self.toBound = None
        self.fTableModel = None
        self.gTableModel = None

    def setModels(self, model1, model2):
        self.fTableModel = model1
        self.gTableModel = model2
        self.readFromTables()
    
    def setGModel(self, model2):
        self.gTableModel = model2

    def getFFunction(self):
        return self.getF()
    
    def getGFunction(self):
        return self.getG()

    def readFromTables(self):
        self.fData = self.getFFunctionData()
        self.gData = self.getGFunctionData()

        self.setF(ArrayFFunction(self.fData))
        self.setG(ArrayGFunction(self.gData))

        for e in self.getFFunctionData():
            print('+', e)

        print()
        for i in self.getGFunctionData():
            print('++',i)

        # print('index', self.gData[2][0])
        # self.gData.getX(2)

    def getFFunctionData(self):
        temp=[]
        if not self.fTableModel == None:
            for col in range(self.fTableModel.columnCount()):
                temp.append(self.fTableModel.data(self.fTableModel.index(1, col)) )
            print(f'getFFunctionModel, not none col count is: {self.fTableModel.columnCount()}')
            for i in temp:
                print(f'getffun el {i}')
            return temp
        else:
            print('getFFunctionModel, is none')
            return None


    def getGFunctionData(self):
        temp=[]
        if not self.gTableModel == None:
            for col in range(self.gTableModel.columnCount()):
                xPoint = self.gTableModel.data(self.gTableModel.index(0, col))
                yPoint = self.gTableModel.data(self.gTableModel.index(1, col))
                temp.append([xPoint, yPoint])
            print('getGFunctionModel, not none')
            return temp
        else:
            print('getGFunctionModel, is none')
            return None

    def clearEquation(self):
        self.fData = []
        self.gData = []
        self.setF(ArrayFFunction(self.fData))
        self.setG(ArrayGFunction(self.gData))
        return self



