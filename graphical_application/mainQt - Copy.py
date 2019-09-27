import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout, QWidget, QMessageBox, QTableWidgetItem, QVBoxLayout, QFileDialog, QMainWindow
from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.uic import loadUi
from PyQt5.QtGui import QStandardItemModel, QFont, QDoubleValidator, QStandardItem

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np

from Include.console_application.array_polynomial import ArrayPolynomial, ArrayFFunction, ArrayGFunction
from Include.console_application.xml_polynomial import XMLPolynomial

class MainApplicationWindow(QMainWindow):
    def __init__(self):
        super(MainApplicationWindow, self).__init__()
        self.polynomial = ArrayPolynomial()
        self.xmlPolynomial = XMLPolynomial()
        self.aBound = None
        self.bBound = None
        self.setInitUI()


    def setInitUI(self):
        loadUi('main_window.ui', self)

        self.setWindowTitle('Equation solver')
        self.setMinimumSize(QSize(808, 506))

        # f & g tables for input data to the table
        self.setFTable()
        self.setGTable()
        self.setCoordinateSystem()
        # roots line edit field
        self.roots_text_edit.setText('Roots field')
        # restrictions for entered type of data
        onlyDouble = QDoubleValidator()
        self.f_add_coef_line_edit.setValidator(onlyDouble)
        self.g_add_x_line_edit.setValidator(onlyDouble)
        self.g_add_y_line_edit.setValidator(onlyDouble)
        '''
        ACTIONS IN MENU BAR
        '''
        self.actionOpen.triggered.connect(self.chooseFromFileOnClick)
        self.actionBuild.triggered.connect(self.buildOnClick)
        self.actionClear.triggered.connect(self.clearOnClick)
        self.actionGenerate_report.triggered.connect(self.generateReportOnClick)
        self.actionSave.triggered.connect(self.saveFileOnClick)
        '''
        BUTTONS CONNECTORS
        '''
        # connect f_add_coefficient & g_add_point btn
        self.f_add_coef_button.clicked.connect(self.addAOnClick)
        self.g_add_point_button.clicked.connect(self.addXYOnClick)
        # connect bounds button
        self.add_bounds_button.clicked.connect(self.addBoundsOnClick)
        # connect build button
        self.build_button.clicked.connect(self.buildOnClick)

    def getFModelColSize(self):
        return self.fModel.columnCount()

    def getGModelColSize(self):
        return self.gModel.columnCount()

    def setFTable(self):
        self.fModel = QStandardItemModel()
        print(f'setFtable, type of fModel is: {self.fModel}')
        self.fModel.setVerticalHeaderLabels(['Index', 'A coef'])
        self.f_function_table_view.setModel(self.fModel)
        return True

    def setGTable(self):
        self.gModel = QStandardItemModel()
        self.gModel.setVerticalHeaderLabels(['X point', 'Y point'])
        self.g_function_table_view.setModel(self.gModel)
        return True

    def setCoordinateSystem(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)

        self.graphical_layout.addLayout(layout, 1, 1)

        self.ax = self.figure.add_subplot(111)

        self.axPoints = self.figure.add_subplot(111)

        self.ax.axhline(y=0, color='k', linewidth=1)
        self.ax.axvline(x=0, color='k', linewidth=1)
        self.ax.grid(True)

    # menu bar action [generate HTML]
    def generateReportOnClick(self):
        # check wether equation was solved and wether it has data in the tables
        if self.polynomial.getFFunctionData() and self.polynomial.getGFunctionData()\
                and self.getFModelColSize() > 0 and self.getGModelColSize() > 0:
            path = QFileDialog.getSaveFileName(self, 'Save file', '', 'HTML files (*.html)')
            filePath = str(path[0])

            # imgPath = filePath.replace('.html', '.png')
            imgPath = '../reports/img/temp_web_img_report.png'

            if path and not filePath == '':
                # if equation is already saved and has solutions, then generate report
                print('Generating report...')
                self.xmlPolynomial.saveReport(filePath, float(self.aBound), float(self.bBound), imgName=imgPath)
                self.showWarningMessageBox('HTML report was generated.', 'Message')
        else:
            self.showWarningMessageBox('You can`t generate report. Please enter data and build function and then try again.', 'Warning')

    # menu bar action [save]
    def saveFileOnClick(self):
        if self.polynomial.getFFunctionData() and self.polynomial.getGFunctionData()\
                and self.getFModelColSize() > 0 and self.getGModelColSize() > 0:
            name = QFileDialog.getSaveFileName(self, 'Save file', '', 'XML files (*.xml)')
            fileName = str(name[0])

            if name:
                fData = self.polynomial.getFFunctionData()
                gData = self.polynomial.getGFunctionData()

                # delete the data for xml polynomial
                self.xmlPolynomial.clearEquation()
                # set data
                for a in fData:
                    self.xmlPolynomial.getFFunction().addA(str(a))

                for point in gData:
                    self.xmlPolynomial.getGFunction().addXY(str(point[0]), str(point[1]))

                self.xmlPolynomial.writeToXML(fileName)
                self.showWarningMessageBox(
                    'File was saved', 'Message')

        else:
            self.showWarningMessageBox('You can`t save empty file. Please enter data and build function and then try again.', 'Warning')

    @pyqtSlot()
    def addAOnClick(self):
        aCoefEditText = self.f_add_coef_line_edit.text()
        print(type(aCoefEditText))
        if aCoefEditText:
            self.f_add_coef_line_edit.clear()

            index = self.fModel.columnCount()
            # insert index
            self.fModel.setItem(0, index, QStandardItem(str(index)) )
            # insert element
            self.fModel.setItem(1, index, QStandardItem(aCoefEditText))
            print(f'Was added new a coef {aCoefEditText}')

        else:
            self.showWarningMessageBox('Enter value for a coefficient and try again!', 'Warning')

    @pyqtSlot()
    def addXYOnClick(self):
        addXEditText = self.g_add_x_line_edit.text()
        addYEditText = self.g_add_y_line_edit.text()
        if addXEditText and addYEditText:

            self.g_add_x_line_edit.clear()
            self.g_add_y_line_edit.clear()

            index = self.gModel.columnCount()
            # insert x value
            self.gModel.setItem(0, index, QStandardItem(addXEditText))
            # insert y value
            self.gModel.setItem(1, index, QStandardItem(addYEditText))

            print(f'Was added {addXEditText}, {addYEditText} point')
        else:
            self.showWarningMessageBox('Enter values for a point and try again!', 'Warning')

    @pyqtSlot()
    def addBoundsOnClick(self):
        self.aBound = self.from_line_edit.text()
        self.bBound = self.to_line_edit.text()

        if not self.aBound and not self.bBound:
            self.showWarningMessageBox("Enter both of bound fields!", 'Warning')
        else:
            self.roots_text_edit.setText(f'Entered bounds [{self.aBound}, {self.bBound}]')


    # menu bar action [open]
    def chooseFromFileOnClick(self):
        filename, filter = QFileDialog.getOpenFileName(parent=self, caption='Open file', directory='',
                                                       filter='*.xml')
        if filename and XMLPolynomial(filename).isValid():
            self.clearData()
            self.xmlPolynomial.readXML(filename)

            # self.aBound = self.xmlPolynomial.getGFunction().getFrom()
            # self.bBound = self.xmlPolynomial.getGFunction().getTo()
            self.aBound = -3
            self.bBound = 3

            self.xmlPolynomial.solve(self.aBound, self.bBound)

            # show roots
            msg = self.rootsMsg(self.xmlPolynomial.getRoots())
            self.roots_text_edit.setText(msg)

            # f(x) table
            alist = self.xmlPolynomial.getFFunction().getAList()
            print(f'type of a list {alist}')
            for coef in alist:
                print(coef)
                # insert index
                index = alist.index(coef)
                self.fModel.setItem(0, index, QStandardItem(str(index)))
                # insert element
                self.fModel.setItem(1, index, QStandardItem(str(coef)))

                print(f'type of an index {coef} {str(coef)}')

            # g(x) table
            pointList = self.xmlPolynomial.getGFunction().getXYList()
            for point in pointList:
                # insert index
                index = pointList.index(point)
                print(f'index {index}')
                self.gModel.setItem(0, index, QStandardItem(str(point[0])))
                # insert element
                self.gModel.setItem(1, index, QStandardItem(str(point[1])))
            # xyArr = self.xmlPolynomial.getGFunction().getXYList()

            # set data to polynomial from opened file
            self.polynomial.setModels(self.fModel, self.gModel)
            # functions data
            xBounded = np.linspace(self.aBound, self.bBound, 500)
            yFFun = [self.xmlPolynomial.getFFunction().function(i) for i in xBounded]
            yGFun = [self.xmlPolynomial.getGFunction().function(i) for i in xBounded]

            # plot the graph
            xyList = self.xmlPolynomial.getGFunction().getXYList()
            self.plotGraphs(xBounded, yFFun, yGFun, xyList, self.xmlPolynomial.getRoots())

    # menu bar action [clear]
    # button on click [build]
    @pyqtSlot()
    def buildOnClick(self):
        self.polynomial.setModels(self.fModel, self.gModel)
        print('array polynomial created')

        if self.polynomial.getFFunctionData() and self.polynomial.getGFunctionData() and self.aBound and self.bBound\
                and self.getFModelColSize() > 0 and self.getGModelColSize() > 0:
            print('Creating array equation...')

            self.setCoordinateSystem()

            print('soving///')
            a = float(self.aBound)
            b = float(self.bBound)
            print(self.polynomial.solve(a, b))

            # show roots
            msg = self.rootsMsg(self.polynomial.getRoots())
            self.roots_text_edit.setText(msg)

            # functions data
            xBounded = np.linspace(a, b, 500)
            yFFun = [self.polynomial.getFFunction().function(i) for i in xBounded]
            yGFun = [self.polynomial.getGFunction().function(i) for i in xBounded]
            # plot the graphs
            self.plotGraphs(xBounded, yFFun, yGFun, self.polynomial.getGFunctionData(), self.polynomial.getRoots())
        else:
            self.showWarningMessageBox('You cant build solution with empty fields!', 'Waning')

    def rootsMsg(self, arr):
        rootsArr = arr
        if len(rootsArr) == 0 or rootsArr == None:
            return 'Equation has 0 roots'
        elif len(rootsArr) == 1:
            return f'Eqution root is {str(rootsArr[0][0])}'
        elif len(rootsArr) >= 2 and len(rootsArr) <= 10:
            s = 'Equation roots: '
            for i in range(len(rootsArr)):
                s += str(rootsArr[i][0]) + ' ' + str(rootsArr[i][1]) + '\n'
            return s
        else:
            return 'Equation has infinite number of roots'

    # menu bar action [clear]
    def clearOnClick(self):
        if self.getFModelColSize() > 0 or self.getGModelColSize() > 0:
            font = QFont()
            font.setFamily('Rubik')
            font.setPointSize(9)

            msgBox = QMessageBox()
            msgBox.setWindowTitle('Warning')
            msgBox.setText('Are you sure to clear all the data?')
            msgBox.setFont(font)

            msgBox.addButton(QtWidgets.QPushButton('OK'), QMessageBox.YesRole)
            msgBox.addButton(QtWidgets.QPushButton('Cancel'), QMessageBox.RejectRole)
            result = msgBox.exec_()

            if result == 0:
                # yes role
                self.clearData()
            else:
                # reject role
                pass
        else:
            self.showWarningMessageBox('All data is already cleared.', 'Warning')


    # sub function for clearing data
    def clearData(self):
        # clear and update coordinate system
        self.setCoordinateSystem()
        # clear f g tables
        self.setFTable()
        self.setGTable()

        # clear add fields
        self.f_add_coef_line_edit.clear()
        self.g_add_x_line_edit.clear()
        self.g_add_y_line_edit.clear()
        # clear bounds
        self.from_line_edit.clear()
        self.to_line_edit.clear()
        # clear line edit root field
        self.roots_text_edit.clear()

        self.xmlPolynomial.clearEquation()

    def plotGraphs(self, xBounded, yFFun, yGFun, gXYArr, rootsArr):
        # functions data
        xBounded = np.linspace(a, b, 500)
        yFFun = [self.polynomial.getFFunction().function(i) for i in xBounded]
        yGFun = [self.polynomial.getGFunction().function(i) for i in xBounded]
        # solution graph
        yPolyFun = [yF - yG for yF, yG in zip(yFFun, yGFun)]

        self.prompt_line_edit.clear()

        # self.ax = self.figure.add_subplot(111)

        self.ax.axhline(y=0, color='k', linewidth=1)
        self.ax.axvline(x=0, color='k', linewidth=1)

        # # draw the points
        # for i in range(len(gXYArr)):
        #     xp = gXYArr[i][0]
        #     yp = gXYArr[i][1]
        #     # self.axPoints.plot(xp, yp, 'o', color='#ff7f0e')
        #     self.ax.scatter(xp, yp, 10)

        self.ax.grid(True)

        # draw the roots
        for j in range(len(rootsArr)):
            x = rootsArr[j][0]
            y = rootsArr[j][1]
            self.ax.plot(x, y, 'o', color='#2ca02cff')
        # # f(x)
        self.ax.plot(xBounded, yFFun, label='f(x)')
        # g(x)
        self.ax.plot(xBounded, yGFun, label='g(x)')
        # f(x)-g(x)
        self.ax.plot(xBounded, yPolyFun, label='f(x)-g(x)')

        self.ax.legend()
        self.ax.set_title('Builded solution')

        self.canvas.draw()

        self.figure.savefig('img_reports/temp_img_report.png', bbox_inches='tight')

    # messagebox if user didnt enter the value to list edit
    def showWarningMessageBox(self, msg, title):
        font = QFont()
        font.setFamily('Rubik')
        font.setPointSize(9)

        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(str(msg))
        msgBox.setFont(font)
        msgBox.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainApplicationWindow()
    widget.show()
    sys.exit(app.exec_())