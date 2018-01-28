import socket
import os
import threading
import time
import datetime
import dns.resolver
import csv
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from_class=uic.loadUiType('main.ui')[0]
class MyWindow(QMainWindow,from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_click)
        self.pushButton_2.clicked.connect(self.btn_click2)



    def btn_click(self):
        global path
        path = 'collect.csv'
        self.pushButton.setText("Update")
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
        self.label.setText(str(self.tableWidget.rowCount()) + "개")
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
            self.label.setText(str(self.tableWidget.rowCount()) + "개")
            f.close()
        else:
            QMessageBox.about(self, "error", "No Choice Column")


def run(self):
    while True:
        r=dns.resolver.Resolver()
        r.nameservers=['8.8.8.8'] #Dns server is google
        DnsServer='8.8.8.8'
        try:
            fulldata=r.query('fl0ckfl0ck.info').response  #check Domain
        except dns.resolver.Timeout or dns.resolver.NoAnswer:
            r.nameservers=['208.67.222.222']    #Dns server is opendns
            DnsServer='208.67.222.222'
            fulldata = r.query('fl0ckfl0ck.info').response  # check Domain
        f = open("collect.csv", 'a')  # if not exist file then we needs create file
        f.close()
        f=open("collect.csv",'r')
        strdata=str(fulldata)


        #split & extraction Domain and IP datas
        tok=strdata.split(';ANSWER')[1]
        tok=tok.split(';AUTHORITY')[0]
        Entire=[]   #Domain + IP
        DnsName=[]  #Domain
        Ipdata=[]   #IP
        j=0
        DnsName.append((tok.split(' ')[0]).split('\n')[1])
        while(j<len(tok.split(' '))-1):
            Entire.append(tok.split(' ')[j+4])  #IP + Domain
            j+=4
        for i in Entire:
            if(i.split('\n')[1]!=None):
                DnsName.append(i.split('\n')[1])
                Ipdata.append(i.split('\n')[0])
            else:
                Ipdata.append(i)

        #Write File
        idx=getidx(f)
        f.close()
        f = open("collect.csv", 'a')  # output file
        wr=csv.writer(f)
        t=datetime.datetime.utcnow()    #GMT Time
        ktime=t+datetime.timedelta(hours=9) #GMT+9
        for i in range(0,len(Ipdata)):
            idx=int(idx)+1
            wr.writerow([str(idx),ktime.strftime("%Y-%m-%d %H:%M:%S"),DnsName[i],Ipdata[i],DnsServer])
           # f.write(str(idx)+' '+ktime.strftime("%Y-%m-%d %H:%M:%S")+' '+DnsName[i]+' '+Ipdata[i]+' '+DnsServer+"\n")


        #Execuete every 1 hours
        f.close()
        time.sleep(3600)

#we check before idx
def getidx(f):
    line='0'
    check=csv.reader(f)
    idx='0'
    for i in check:
        if(str(i).split(',')[0]!='[]'):
            idx=str(i).split(',')[0]
            idx=str(i).split('[')[1]
            idx=str(i).split('\'')[1]
    return str(idx)

# Is it String?
def isNumber(s):
    try:
        float(s)
        return False
    except ValueError:
        return True

i=0

#garbage dummy in order to stdout,stderr garbage setting
class Dummy:
    def write(self,s):
        pass
#fork
if os.fork():
    os._exit(0)

os.setpgrp()    #make solo group
os.umask(0)
#stdin, stdout, stderr garbage setting is don't influenced console
sys.stdin.close()
sys.stdout=Dummy()
sys.stderr=Dummy()
#daemon process execute run funtion
thread=threading.Thread(target=run,args=(i,))
thread.start()


if __name__=='__main__':
    app=QApplication(sys.argv)
    mywindow=MyWindow()
    mywindow.show()
    app.exec()

