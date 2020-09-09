# coding=utf-8
import sys
from PyQt5 import QtWidgets
import gui
from PyShopping import *



class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.lineEdit.returnPressed.connect(self.search_by_tag)
        self.tableWidget.setColumnCount(4)

    def search_by_tag(self):
        tag = self.lineEdit.text()
        if tag != "":
            self.tableWidget.clear()
            result = search_by_tag(tag)
            for i in range(len(result)):
                self.tableWidget.insertRow(1)
                for j in range(4):
                    self.tableWidget.setItem(i, j, result[i][j])


def main():
    conn = sqlite3.connect('products_bd.sqlite')
    cursor = conn.cursor()
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
