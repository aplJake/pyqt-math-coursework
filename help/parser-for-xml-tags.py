
def __str__(self):

    toPrint = ''
    tree = ET.parse(self.__xmlFileName)
    data = tree.getroot()

    acoeffs = data.find('ACoefs')
    toPrint += 'A coefficients:\n'
    for row in acoeffs.findall('ACoef'):
        acoefIndex = row.get('Index')
        acoefValue = row.get('Value')
        toPrint += 'Index ' + acoefIndex + ' Value ' + acoefValue + '\n'

    xypoints = data.find('XYPoints')
    toPrint += 'XY points:\n'
    for row in xypoints.findall('XYPoint'):
        xypointIndex = row.get('Index')
        xypointXValue = row.get('X')
        xypointYValue = row.get('Y')
        toPrint += 'Index ' + xypointIndex + ' X value ' +\
                   xypointXValue + ' Y value ' + xypointYValue + '\n'
    return toPrint

