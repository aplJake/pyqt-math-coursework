import xmlschema
import xml.etree.ElementTree as ET
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import matplotlib.pyplot as plt
import numpy as np

from Include.console_application.polynomial_equation import PolynomialEquation
from Include.console_application.xml_functions import XMLFFunction, XMLGFunction


class FileException(Exception):
    def __init__(self, fileName):
        self.__fileName = fileName

    def getFileName(self):
        return self.__fileName

class FileReadException(FileException):
    def __init__(self, fileName):
        super().__init__(fileName)


class XMLPolynomial(PolynomialEquation):


    def __init__(self, xmlFileName=None):
        super(XMLPolynomial, self).__init__()
        if xmlFileName:
            self.xmlFileName = xmlFileName
            if self.isValid():
                self.__data = ET.ElementTree()
                self.readXML(xmlFileName)
        else:
            self.xmlFileName = None
            self.clearEquation()

    def getFFunction(self):
        return self.getF()

    def getGFunction(self):
        return self.getG()

    def getEquationData(self):
        return self.__data

    def getFileName(self):
        return self.xmlFileName

    def isValid(self):
        myEquationSchema = xmlschema.XMLSchema('E:/Users/Asus/PycharmProjects/semester_work/venv/Include/EquationForm.xsd')

        return myEquationSchema.is_valid(self.xmlFileName)

    def readXML(self, xmlFileName):
        self.xmlFileName = xmlFileName
        print('\n\n\nReading XML...')
        try:
            tree = ET.parse(xmlFileName)
            self.__data = tree.getroot()
            self.setF(XMLFFunction(self.__data))
            self.setG(XMLGFunction(self.__data))
            return self
        except FileReadException:
            raise FileReadException(xmlFileName)
        except NameError:
            print('NameError')

    def writeToXML(self, xmlFileName):
        root = self.__data
        tree = ET.ElementTree(root)
        tree.write(xmlFileName)

    def saveReport(self, fileName, a, b, imgName=None, dynamFile=None):
        try:
            self.clearRoots()
            f = open(f'{fileName}', 'w')
            f.write('<!doctype html>')
            f.write('<html lang="en">')
            f.write('<head>')
            f.write('<meta http-equiv="X-UA-Compatible" content="ie=edge" charset="UTF-8">')
            f.write('</head>')
            f.write('<body>')
            f.write('<h1>Report</h1>')
            f.write('<p>Polynomial equation was solved with such input data</p>')
            # f function input data
            f.write('<h4>Data for function <span style="font-family:Times, Serif">\
                <em>f(t)</em></span></h4>')
            f.write('<table border = "1" cellpadding=4 cellspacing=0>')
            f.write('<tr>')
            f.write('<th>Index</th>')
            f.write('<th>A coefficient</th>')
            f.write('</tr>')

            for i in range(self.getFFunction().aCount()):
                f.write('<tr>')
                f.write(f'<td> {i} </td>')
                f.write(f'<td> {self.getFFunction().getA(i)} </td>')
                f.write('</tr>')
            f.write('</table>')
            # g function input data
            f.write('<h4>Data for function <span style="font-family:Times, Serif;">\
                <em>g(t)</em></span></h4>')
            f.write('<table border = "1" cellpadding=4 cellspacing=0>')
            f.write('<tr>')
            f.write('<th>Index</th>')
            f.write('<th>X point</th>')
            f.write('<th>Y point</th>')
            f.write('</tr>')
            for i in range(self.getGFunction().xyCount()):
                f.write('<tr>')
                f.write(f'<td> {i} </td>')
                f.write(f'<td> {self.getGFunction().getX(i)} </td>')
                f.write(f'<td> {self.getGFunction().getY(i)} </td>')
                f.write('</tr>')
            f.write('</table>')
            # roots of equation

            f.write(f'<h4>Interval values for searching the root <em>from a</em>: {a}\
            <em>to b</em>: {b} </h4>')
            self.solve(a, b)
            roots = self.getRoots()
            if len(roots) == 0:
                f.write('<p>Equation has 0 roots.</p>')
            elif len(roots) == 1:
                f.write(f'<p>Eqution root is x = {str(roots[0][0])} y = {str(roots[0][1])}.</p>')
            elif len(roots) >= 2 and len(roots) <= 10:
                f.write('<p>Equation has such roots:</p>')
                for i in range(len(roots)):
                    f.write(f'x = {str(roots[i][0])} y = {str(roots[i][1])}<br>')
            else:
                f.write('<p>The number of roots greater than 10</p>')

            # static image integration
            if imgName:
                f.write('<h4>Image report</h4>')
                self.getIMGReport(imgName)
                f.write(f'<img src = "../{imgName}"/>')

            # dynamic image integration
            if dynamFile:
                self.getPlotlyFigure(f'E:/Users/Asus/PycharmProjects/semester_work/venv/Include/reports/html/{dynamFile}')
                f.write('<h4>Dynamic graph report</h4>')
                f.write('<button >')
                f.write(f'<a style="text-decoration: none; color: black" href="..reports//html/{dynamFile}">Show dynamic graph</a>')
                f.write('</button>')
            f.write('</body>')
            f.write('</html>')
            f.close()
        except(ValueError, ZeroDivisionError):
            print('Try to enter another data to solve equation')
        except(IOError, FileNotFoundError):
            print('I/O Error')

    def clearEquation(self):
        print('\nDeleting the equation...')
        self.xmlFileName = None
        self.__data = ET.Element('EquationData')
        self.setF(XMLFFunction(self.__data))
        self.setG(XMLGFunction(self.__data))
        self.clearRoots()
        return self

    def printStructure(self):
        ET.dump(self.__data)

    def getIMGReport(self, imgName):
        xFrom = self.getFromVal()
        xTo = self.getToVal()

        print(f'**From {xFrom} to {xTo}')

        xBounded = np.linspace(xFrom, xTo, 500)
        yFFun = [self.getFFunction().function(i) for i in xBounded]
        yGFun = [self.getGFunction().function(i) for i in xBounded]
        yPolyFun = [yF - yG for yF, yG in zip(yFFun, yGFun)]

        # figure
        fig = plt.figure()
        origins = plt.subplot()
        origins.axhline(y=0, color='k', linewidth=1)
        origins.axvline(x=0, color='k', linewidth=1)

        # f(x)
        plt.plot(xBounded, yFFun, label='f(x)')
        # g(x)
        plt.plot(xBounded, yGFun, label='g(x)')
        # f(x)-g(x)
        plt.plot(xBounded, yPolyFun, label='f(x)-g(x)')

        roots = self.getRoots()
        for j in range(len(roots)):
            x = roots[j][0]
            y = roots[j][1]
            plt.plot(x, y, 'o', color='#2ca02cff')

        plt.title('linear')
        plt.grid(True)
        plt.xlabel('x label')
        plt.ylabel('y label')

        plt.legend()
        plt.draw()
        fig.savefig(f'{imgName}', bbox_inches='tight')

    def getPlotlyFigure(self, htmlFileName):
        xFrom = self.getFromVal()
        xTo = self.getToVal()
        title = 'Graphical report'
        traces = []

        # traces data
        xBounded = np.linspace(xFrom, xTo, 500)
        yFFun = [self.getFFunction().function(i) for i in xBounded]
        yGFun = [self.getGFunction().function(i) for i in xBounded]
        yPolyFun = [yF - yG for yF, yG in zip(yFFun, yGFun)]
        # Create and style traces
        fFunction = go.Scatter(
            x = xBounded,
            y = yFFun,
            mode='lines',
            name = 'f(x)',
            line = dict(
                color=('rgb(22, 96, 167)'),
                width=3,
                shape='spline')
        )
        gFunction = go.Scatter(
            x=xBounded,
            y=yGFun,
            mode='lines',
            name='g(x)',
            line=dict(
                color=('rgb(0, 255, 0)'),
                width=3,
                shape='spline')
        )
        polyFunction = go.Scatter(
            x=xBounded,
            y=yPolyFun,
            mode='lines',
            name='f(x)-g(x)',
            line=dict(
                color=('rgb(205, 12, 24)'),
                width=3,
                shape='spline')
        )
        traces = [fFunction, gFunction, polyFunction]
        # Edit the layout
        layout = dict(
            # width=600,
            # height=600,
            title=title)
        fig = dict(data=traces, layout=layout)
        plotly.offline.plot(fig, filename=htmlFileName)