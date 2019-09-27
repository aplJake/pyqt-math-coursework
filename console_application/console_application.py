from Include.console_application.xml_polynomial import XMLPolynomial

class ConsoleApplication:
    @staticmethod
    def main():
        print('Creating equation form from xml...')
        includePath = 'E:/Users/Asus/PycharmProjects/semester_work/venv/Include'

        polynomial = XMLPolynomial(xmlFileName=f'{includePath}/xml_examples/four_roots_on_fm10_to30.xml')
        # read from file [4 roots]
        polynomial.saveReport(fileName=f'{includePath}/reports/html/four_roots.html', a=-10, b=30, imgName=f'../reports/img/four_roots.png')

        # read from file [2 roots]
        print(polynomial.readXML(f'{includePath}/xml_examples/two_roots_ex.xml').solve(-6, 15))
        polynomial.saveReport(fileName=f'{includePath}/reports/html/two_roots_ex.html', a=-6, b=15, imgName=f'../reports/img/two_roots_ex.png')

        # read from file [1 roots]
        print(polynomial.readXML(f'{includePath}/xml_examples/one_root_ex.xml').solve(-5, 7))
        polynomial.saveReport(fileName=f'{includePath}/reports/html/one_root_ex.html', a=-5, b=7,
                              imgName=f'../reports/img/one_root_ex.png')

        # read from file [equation no solutions]
        print(polynomial.readXML(f'{includePath}/xml_examples/no_roots_ex.xml').solve(-33, 7))
        polynomial.saveReport(fileName=f'{includePath}/reports/html/no_roots.html', a=-5, b=8, imgName=f'../reports/img/no_roots.png')

        # creating the equation [equation 2 solutions]
        polynomial.clearEquation()
        polynomial.getFFunction().addA(2)
        polynomial.getFFunction().addA(1)
        polynomial.getFFunction().addA(-5)
        polynomial.getFFunction().addA(12)
        polynomial.getFFunction().addA(10)
        polynomial.getGFunction().addXY(0, -2)
        polynomial.getGFunction().addXY(1, -5)
        polynomial.getGFunction().addXY(2, 0)
        polynomial.getGFunction().addXY(3, -4)
        print(polynomial.solve(-3, 4))
        polynomial.saveReport(fileName=f'{includePath}/reports/html/console_equat.html', a=-3, b=4, imgName='../reports/img/console_equat.png')

        # changing the xml-input data
        polynomial.getFFunction().setA(3, 23)
        print(polynomial.getFFunction().getA(3))
        polynomial.writeToXML('ChangedXMLFile.xml')
        print(polynomial.readXML('ChangedXMLFile.xml').solve(-10, 0))

if __name__ == "__main__":
    ConsoleApplication().main()
