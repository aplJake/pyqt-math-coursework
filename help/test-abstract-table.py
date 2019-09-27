import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

my_array = [['00','01'],
            ['10','11']]

# création de la vue et du conteneur
class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        tablemodel = MyTableModel(my_array, self)
        tableview = QTableView()
        tableview.setModel(tablemodel)

        layout = QVBoxLayout(self)
        layout.addWidget(tableview)
        self.setLayout(layout)

        print('adding a row 23-32')
        # my_array.append(['23', '32'])
        # tablemodel.index()
        # i = QModelIndex()
        # tablemodel.
        # tablemodel.setData(4, '32')

# création du modèle
class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, parent = None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.arraydata)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return (self.arraydata[index.column()][index.row()])

    def setData(self, index, value):
        self.arraydata[index.column()][index.row()] = value
        return True

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())