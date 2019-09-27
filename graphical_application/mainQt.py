import sys
import numpy as np
import webbrowser
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QFileDialog, QMainWindow
from PyQt5.QtCore import QSize, QSysInfo, Qt
from PyQt5.uic import loadUi
from PyQt5.QtGui import QStandardItemModel, QFont, QDoubleValidator, QStandardItem

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from Include.console_application.array_polynomial import ArrayPolynomial, ArrayFFunction, ArrayGFunction
from Include.console_application.xml_polynomial import XMLPolynomial


class AboutDialog(QDialog):
    def __init__(self, parent=None, flags=None):
        super(AboutDialog, self).__init__(parent, flags)
        self.setInitUI()
        self.closeAboutButton.clicked.connect(self.closeDialog)

    def setInitUI(self):
        loadUi('about_ui.ui', self)

    def closeDialog(self):
        self.close()


class MainApplicationWindow(QMainWindow):
    def __init__(self):
        super(MainApplicationWindow, self).__init__()
        self.polynomial = ArrayPolynomial()
        self.xmlPolynomial = XMLPolynomial()
        self.aBound = None
        self.bBound = None
        self.savedFileName = None
        self.setInitUI()

    def setInitUI(self):
        loadUi('main_window.ui', self)

        self.setWindowTitle('Equation solver')
        self.setMinimumSize(QSize(879, 511))
        self.setMaximumSize(QSize(879, 511))

        self.setFTable()
        self.setGTable()
        self.setCoordinateSystem()
        self.roots_text_edit.setText('Empty')
        # restrictions for entered type of data
        self.from_line_edit.setValidator(QDoubleValidator())
        self.to_line_edit.setValidator(QDoubleValidator())
        '''
        ACTIONS IN MENU BAR
        '''
        self.actionOpen.triggered.connect(self.chooseFromFileOnClick)
        self.actionBuild.triggered.connect(self.buildOnClick)
        self.actionClear.triggered.connect(self.clearOnClick)
        self.actionGenerate_report.triggered.connect(self.generateReportOnClick)
        self.actionSave.triggered.connect(self.saveAction)
        self.actionGetHelp.triggered.connect(self.getHelpOnClick)
        self.actionNew.triggered.connect(self.clearOnClick)
        self.actionSaveAs.triggered.connect(self.saveFileOnClick)
        self.actionAbout.triggered.connect(self.showAboutOnClick)
        '''
        BUTTONS CONNECTORS
        '''
        self.fAddColBtn.clicked.connect(self.addColToFTable)
        self.gAddColBtn.clicked.connect(self.addColToGTable)
        self.add_bounds_button.clicked.connect(self.addBoundsOnClick)

    '''
    F TABLE METHODS
    '''
    def setFTable(self):
        self.fModel = QStandardItemModel()
        print(f'setFtable, type of fModel is: {self.fModel}')
        self.fModel.setVerticalHeaderLabels(['Power', 'Coefficient'])
        self.f_function_table_view.setModel(self.fModel)
        self.setTablesStyleW10(self.f_function_table_view)
        return True

    def getFModelColSize(self):
        return self.fModel.columnCount()

    def addColToFTable(self):
        # if table contains at least one cell
        # check whether it is populated and add empty row
        columnNumber = self.fModel.columnCount()
        if columnNumber == 0:
            self.insertNewColumnToFTable(self.fModel)
        elif self.checkFModelItems(self.fModel, columnNumber - 1):
            checkItem = self.fModel.item(1, columnNumber - 1)
            if checkItem:
                self.insertNewColumnToFTable(self.fModel)
            else:
                self.showWarningMessageBox('Populate already created fields!', 'Warning')
        else:
            self.showWarningMessageBox('Populate already created fields!', 'Warning')

    def insertNewColumnToFTable(self, model):
        index = model.columnCount()
        model.insertColumn(index)
        # insert index
        item = QStandardItem(str(index))
        item.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)
        model.setItem(0, index, item )

    # check whether f-table is fully populated
    def checkFModelItems(self, model, checkingRange):
        if model and checkingRange >= 0:
            for column in range(checkingRange):
                cellData = model.item(1, column)
                if not cellData or len(cellData.text()) == 0:
                    return False
            return True
        else:
            return False

    '''
    G TABLE METHODS
    '''
    def setGTable(self):
        self.gModel = QStandardItemModel()
        self.gModel.setVerticalHeaderLabels(['X point', 'Y point'])
        self.g_function_table_view.setModel(self.gModel)
        self.setTablesStyleW10(self.g_function_table_view)
        return True

    def getGModelColSize(self):
        return self.gModel.columnCount()

    def addColToGTable(self):
        # if table contains at least one cell
        # check whether it is populated and add empty row
        columnNumber = self.gModel.columnCount()
        if columnNumber == 0:
            self.insertNewColumnToGTable(self.gModel)
        elif self.checkGModelItems(self.gModel, columnNumber - 1):
            checkItemX = self.gModel.item(0, columnNumber - 1)
            checkItemY = self.gModel.item(1, columnNumber - 1)
            if checkItemX and checkItemY:
                # self.sortByXCoordinate(self.gModel)
                self.insertNewColumnToGTable(self.gModel)
            else:
                self.showWarningMessageBox('Populate already created fields!', 'Warning')
        else:
            self.showWarningMessageBox('Populate already created fields!', 'Warning')

    def insertNewColumnToGTable(self, model):
        index = model.columnCount()
        model.insertColumn(index)

    # check whether g-table is fully populated
    def checkGModelItems(self, model, checkingRange):
        if model and checkingRange >= 0:
            for column in range(checkingRange):
                cellXData = model.item(0, column)
                cellYData = model.item(1, column)
                if  not cellXData or \
                    not cellYData or \
                    len(cellXData.text()) == 0 or \
                    len(cellYData.text()) == 0:
                    return False
            return True
        else:
            return False

    def sortByXCoordinate(self, tableModel):
        data2d = []
        for col in range(tableModel.columnCount()):
            print(f'colN sort {tableModel.columnCount()}')
            xPoint = tableModel.data(tableModel.index(0, col))
            yPoint = tableModel.data(tableModel.index(1, col))
            data2d.append([float(xPoint), float(yPoint)])
            print(data2d)
        data2d.sort(key=lambda x: x[0])
        print(f'*****{format(tableModel.columnCount())}')
        for index in range(tableModel.columnCount()):
            # insert x value
            print(index)
            xItem = data2d[index][0]
            self.gModel.setItem(0, index, QStandardItem(str(xItem)))
            # insert y value
            yItem = data2d[index][1]
            self.gModel.setItem(1, index, QStandardItem(str(yItem)))
    '''
    BOUNDS
    '''
    def addBoundsOnClick(self):
        if not self.from_line_edit.text() and not self.to_line_edit.text():
            self.showWarningMessageBox("Enter both of bound fields!", 'Warning')
        else:
            if float(self.from_line_edit.text()) >= float(self.to_line_edit.text()):
                self.showWarningMessageBox("Enter correct data.", 'Warning')
                self.from_line_edit.clear()
                self.to_line_edit.clear()
            else:
                self.aBound = float(self.from_line_edit.text())
                self.bBound = float(self.to_line_edit.text())
                self.roots_text_edit.setText(f'Entered bounds [{self.aBound}, {self.bBound}]')
    '''
    PLOT
    '''
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
        self.ax.set_xlabel('x axis')
        self.ax.set_ylabel('y axis')
        self.ax.yaxis.set_label_position("right")
        self.ax.axhline(y=0, color='k', linewidth=1)
        self.ax.axvline(x=0, color='k', linewidth=1)
        self.ax.grid(True)

    def plotGraphs(self, rootsArr, gXYArr, xFrom, xTo):
        xBounded = np.linspace(xFrom, xTo, 500)
        yFFun = [self.polynomial.getFFunction().function(i) for i in xBounded]
        yGFun = [self.polynomial.getGFunction().function(i) for i in xBounded]
        yPolyFun = [yF - yG for yF, yG in zip(yFFun, yGFun)]

        self.prompt_line_edit.clear()
        self.ax.axhline(y=0, color='k', linewidth=1)
        self.ax.axvline(x=0, color='k', linewidth=1)

        # draw the roots
        for j in range(len(rootsArr)):
            x = rootsArr[j][0]
            y = rootsArr[j][1]
            self.ax.plot(x, y, 'o', color='#2ca02cff')
        # plot the graphs
        self.ax.plot(xBounded, yFFun, label='f(x)')
        self.ax.plot(xBounded, yGFun, label='g(x)')
        self.ax.plot(xBounded, yPolyFun, label='f(x)-g(x)')

        self.ax.legend()
        self.ax.set_title('Builded solution')
        self.ax.grid(True)

        self.canvas.draw()
        self.figure.savefig('img_reports/temp_img_report.png', bbox_inches='tight')

    '''
    HELP ACTIONS
    '''
    def showAboutOnClick(self):
        aboutWindow = AboutDialog(parent=self, flags=Qt.WindowTitleHint and Qt.WindowCloseButtonHint)
        aboutWindow.show()

    @staticmethod
    def getHelpOnClick():
        webbrowser.open('file://' + os.path.realpath('doc/html/index.html'))
    '''
    FILE ACTIONS
    '''
    def buildOnClick(self):
        self.polynomial.setModels(self.fModel, self.gModel)
        print('array polynomial created')

        if self.polynomial.getFFunctionData(): print('/1')
        if self.polynomial.getGFunctionData(): print('/2')
        if self.aBound: print('/3')
        if self.bBound: print('/4')
        if self.getFModelColSize() > 0: print('/5')
        if self.getGModelColSize() > 0: print('/6')

        if self.polynomial.getFFunctionData() and self.polynomial.getGFunctionData()\
                and self.aBound  and self.bBound\
                and self.getFModelColSize() > 0 and self.getGModelColSize() > 0:
            self.setCoordinateSystem()

            try:
                print('soving...')
                self.sortByXCoordinate(self.gModel)
                a = float(self.aBound)
                b = float(self.bBound)
                self.polynomial.solve(a, b)

                # show roots
                msg = self.rootsMsg(self.polynomial.getRoots())
                self.roots_text_edit.setText(msg)
                # plot the graphs
                self.setCoordinateSystem()
                self.plotGraphs(self.polynomial.getRoots(), self.polynomial.getGFunctionData(),
                                self.polynomial.getFromVal(), self.polynomial.getToVal())
            except(ValueError, ZeroDivisionError):
                self.showWarningMessageBox('Try open file with proper values', 'Error')
            except Exception:
                self.showWarningMessageBox('Unknown error', 'Error')
        else:
            self.showWarningMessageBox('You cant build solution with empty fields;)!', 'Waning')

    def saveFileOnClick(self):
        if self.polynomial.getFFunctionData() and self.polynomial.getGFunctionData()\
                and self.getFModelColSize() > 0 and self.getGModelColSize() > 0:
            name = QFileDialog.getSaveFileName(self, 'Save file', '', 'XML files (*.xml)')

            self.savedFileName = name
            self.actionSave.setEnabled(True)

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
            self.showWarningMessageBox('You can`t save empty file.\
             Please enter data and build function and then try again.', 'Warning')

    def saveAction(self):
        # get name from the saveOnClick fuction (Save as)
        if self.polynomial.getFFunctionData() and self.polynomial.getGFunctionData() \
                and self.getFModelColSize() > 0 and self.getGModelColSize() > 0:

            fData = self.polynomial.getFFunctionData()
            gData = self.polynomial.getGFunctionData()

            # delete the data for xml polynomial
            self.xmlPolynomial.clearEquation()
            # set data
            for a in fData:
                self.xmlPolynomial.getFFunction().addA(str(a))

            for point in gData:
                self.xmlPolynomial.getGFunction().addXY(str(point[0]), str(point[1]))

            self.xmlPolynomial.writeToXML(self.savedFileName)
            self.showWarningMessageBox(
                'File was saved', 'Message')
        else:
            self.showWarningMessageBox(
                'You can`t save empty file. Please enter data and build function and then try again.', 'Warning')

    def generateReportOnClick(self):
        # check whether equation was solved and wether it has data in the tables
        if self.polynomial.getFFunctionData() and self.polynomial.getGFunctionData()\
                and self.getFModelColSize() > 0 and self.getGModelColSize() > 0:
            path = QFileDialog.getSaveFileName(self, 'Save file', '', 'HTML files (*.html)')
            filePath = str(path[0])

            # imgPath = filePath.replace('.html', '.png')
            includePath = 'E:/Users/Asus/PycharmProjects/semester_work/venv/Include'
            imgPath = '../reports/img/temp_web_img_report.png'

            if path and not filePath == '':
                # if equation is already saved and has solutions, then generate report
                print('Generating report...')
                self.xmlPolynomial.saveReport(filePath, float(self.aBound), float(self.bBound), imgName=imgPath)
                self.showWarningMessageBox('HTML report was generated.', 'Message')
        else:
            self.showWarningMessageBox('You can`t generate report.\
             Please enter data and build function and then try again.', 'Warning')

    def chooseFromFileOnClick(self):
        filename, filter = QFileDialog.getOpenFileName(parent=self, caption='Open file', directory='',
                                                       filter='*.xml')
        self.savedFileName = filename
        self.actionSave.setEnabled(True)

        if filename and XMLPolynomial(filename).isValid():
            self.clearData()
            self.xmlPolynomial.readXML(filename)

            self.aBound = self.xmlPolynomial.getGFunction().getFrom()
            self.bBound = self.xmlPolynomial.getGFunction().getTo()

            self.from_line_edit.setText(str(self.aBound))
            self.to_line_edit.setText(str(self.bBound))

            xPointsArr = []
            for col in range(self.gModel.columnCount()):
                xPoint = self.gModel.data(self.gModel.index(0, col))
                xPointsArr.append(float(xPoint))

            try:
                self.xmlPolynomial.solve(self.aBound, self.bBound)
                # show roots
                msg = self.rootsMsg(self.xmlPolynomial.getRoots())
                self.roots_text_edit.setText(msg)

                # f(x) table
                alist = self.xmlPolynomial.getFFunction().getAList()
                print(f'type of a list {alist}')
                for coef in alist:
                    index = alist.index(coef)
                    self.fModel.setItem(0, index, QStandardItem(str(index)))
                    self.fModel.setItem(1, index, QStandardItem(str(coef)))

                # g(x) table
                pointList = self.xmlPolynomial.getGFunction().getXYList()
                for point in pointList:
                    index = pointList.index(point)
                    print(f'index {index}')
                    self.gModel.setItem(0, index, QStandardItem(str(point[0])))
                    self.gModel.setItem(1, index, QStandardItem(str(point[1])))

                # set data to polynomial from opened file
                self.polynomial.setModels(self.fModel, self.gModel)

                # plot the graph
                xyList = self.xmlPolynomial.getGFunction().getXYList()
                self.plotGraphs(self.xmlPolynomial.getRoots(), xyList,\
                                self.xmlPolynomial.getFromVal(), self.xmlPolynomial.getToVal())
            except(ValueError, ZeroDivisionError):
                self.showWarningMessageBox('Try open file with proper values', 'Error')
            except Exception:
                self.showWarningMessageBox('Check the data', 'Error')

    def clearOnClick(self):
        if self.getFModelColSize() > 0 or self.getGModelColSize() > 0:
            font = QFont()
            font.setFamily('Arial')
            font.setPointSize(9)

            msgBox = QMessageBox()
            msgBox.setWindowTitle('Warning')
            msgBox.setText('Are you sure you want to create a new file, your data will be los')
            msgBox.setFont(font)

            msgBox.addButton(QtWidgets.QPushButton('OK'), QMessageBox.YesRole)
            msgBox.addButton(QtWidgets.QPushButton('Cancel'), QMessageBox.RejectRole)
            result = msgBox.exec_()

            if result == 0:
                # yes role
                self.savedFileName = None
                self.actionSave.setEnabled(False)
                self.clearData()
            else:
                # reject role
                pass
        else:
            self.showWarningMessageBox('All data is already cleared.', 'Warning')

    '''
    HELPER FUNCTIONS
    '''
    def rootsMsg(self, arr):
        rootsArr = arr
        if len(rootsArr) == 0 or rootsArr is None:
            return 'Equation has 0 roots'
        elif len(rootsArr) == 1:
            return f'Eqution roots: \n[x = {str(rootsArr[0][0])} y = {str(rootsArr[0][1])}]'
        elif len(rootsArr) >= 2 and len(rootsArr) <= 10:
            s = 'Equation roots: \n'
            for i in range(len(rootsArr)):
                s += f'[x = {str(rootsArr[i][0])} y = {str(rootsArr[i][1])}' + '\n'

            return s
        else:
            return 'Equation has infinite number of roots'

    def clearData(self):
        # clear and update coordinate system
        self.setCoordinateSystem()
        # clear f g tables
        self.setFTable()
        self.setGTable()
        # clear bounds
        self.from_line_edit.clear()
        self.to_line_edit.clear()
        # clear line edit root field
        self.roots_text_edit.clear()

        self.xmlPolynomial.clearEquation()

    @staticmethod
    def showWarningMessageBox(msg, title):
        font = QFont()
        font.setFamily('Rubik')
        font.setPointSize(9)

        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(str(msg))
        msgBox.setFont(font)
        msgBox.exec_()

    # create the header borders in the table on win10
    @staticmethod
    def setTablesStyleW10(tableView):
        if QSysInfo.windowsVersion() == QSysInfo.WV_WINDOWS10:
            tableView.setStyleSheet(
                "QHeaderView::section{"
                "border-top:0px solid #D8D8D8;"
                "border-left:0px solid #D8D8D8;"
                "border-right:1px solid #D8D8D8;"
                "border-bottom: 1px solid #D8D8D8;"
                "background-color:white;"
                "padding:4px;"
                "}"
                "QTableCornerButton::section{"
                "border-top:0px solid #D8D8D8;"
                "border-left:0px solid #D8D8D8;"
                "border-right:1px solid #D8D8D8;"
                "border-bottom: 1px solid #D8D8D8;"
                "background-color:white;"
                "}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainApplicationWindow()
    widget.show()
    sys.exit(app.exec_())