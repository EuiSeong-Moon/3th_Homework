from PyQt5.QtWidgets import *
from PyQt5 import uic
import csv
import sys

path=None
from_class=uic.loadUiType('support.ui')[0]
class MyWindow(QMainWindow,from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_click)
        self.pushButton_2.clicked.connect(self.btn_click2)



    def btn_click(self):
        global path
        self.pushButton.setText("Update")
        path = self.textEdit.toPlainText()
        FNE = path.split('\\')[-1].split('.')[1]
        if(FNE!='csv'):
            QMessageBox.about(self, "error", "File Name Extension error")
            exit(1)
        try:
            f=open(path,'r')
        except:
            print("path error")
            QMessageBox.about(self, "error", "Path error")
            exit(1)

        r=csv.reader(f)
        while (self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0);
        self.tableWidget.setRowCount=0
        for i in r:
            if(str(i)=='[]'):
                continue
            row=self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row,0,QTableWidgetItem(i[0]))
            self.tableWidget.setItem(row,1,QTableWidgetItem(i[1]))
            self.tableWidget.setItem(row,2,QTableWidgetItem(i[2]))
            self.tableWidget.setItem(row,3,QTableWidgetItem(i[3]))
            self.tableWidget.setItem(row,4,QTableWidgetItem(i[4]))
        self.label_3.setText(str(self.tableWidget.rowCount()) + "개")
        f.close()

    def btn_click2(self):
        find_data = self.textEdit_3.toPlainText()
        if(self.comboBox.currentText()!='None'):
            combo_data=str(self.comboBox.currentText())
            f = open(path, 'r')
            r = csv.reader(f)
            while(self.tableWidget.rowCount()>0):
                self.tableWidget.removeRow(0);
            self.tableWidget.setRowCount = 0
            if(combo_data!='None'):
                for i in r:
                    if (str(i) == '[]'):
                        continue
                    if(str(i[0])==find_data):
                        row = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(row)
                        self.tableWidget.setItem(row, 0, QTableWidgetItem(i[0]))
                        self.tableWidget.setItem(row, 1, QTableWidgetItem(i[1]))
                        self.tableWidget.setItem(row, 2, QTableWidgetItem(i[2]))
                        self.tableWidget.setItem(row, 3, QTableWidgetItem(i[3]))
                        self.tableWidget.setItem(row, 4, QTableWidgetItem(i[4]))

                    elif(str(i[1])==find_data):
                        row = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(row)
                        self.tableWidget.setItem(row, 0, QTableWidgetItem(i[0]))
                        self.tableWidget.setItem(row, 1, QTableWidgetItem(i[1]))
                        self.tableWidget.setItem(row, 2, QTableWidgetItem(i[2]))
                        self.tableWidget.setItem(row, 3, QTableWidgetItem(i[3]))
                        self.tableWidget.setItem(row, 4, QTableWidgetItem(i[4]))

                    elif (str(i[2]) == find_data):
                        row = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(row)
                        self.tableWidget.setItem(row, 0, QTableWidgetItem(i[0]))
                        self.tableWidget.setItem(row, 1, QTableWidgetItem(i[1]))
                        self.tableWidget.setItem(row, 2, QTableWidgetItem(i[2]))
                        self.tableWidget.setItem(row, 3, QTableWidgetItem(i[3]))
                        self.tableWidget.setItem(row, 4, QTableWidgetItem(i[4]))

                    elif (str(i[3]) == find_data):
                        row = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(row)
                        self.tableWidget.setItem(row, 0, QTableWidgetItem(i[0]))
                        self.tableWidget.setItem(row, 1, QTableWidgetItem(i[1]))
                        self.tableWidget.setItem(row, 2, QTableWidgetItem(i[2]))
                        self.tableWidget.setItem(row, 3, QTableWidgetItem(i[3]))
                        self.tableWidget.setItem(row, 4, QTableWidgetItem(i[4]))

                    elif (str(i[4]) == find_data):
                        row = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(row)
                        self.tableWidget.setItem(row, 0, QTableWidgetItem(i[0]))
                        self.tableWidget.setItem(row, 1, QTableWidgetItem(i[1]))
                        self.tableWidget.setItem(row, 2, QTableWidgetItem(i[2]))
                        self.tableWidget.setItem(row, 3, QTableWidgetItem(i[3]))
                        self.tableWidget.setItem(row, 4, QTableWidgetItem(i[4]))
            self.label_3.setText(str(self.tableWidget.rowCount())+"개")
            f.close()
        else:
            QMessageBox.about(self, "error", "No Choice Column")


if __name__=='__main__':
    app=QApplication(sys.argv)
    mywindow=MyWindow()
    mywindow.show()
    app.exec()

