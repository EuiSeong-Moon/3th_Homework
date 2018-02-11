# -*- coding:utf-8 -*-
import datetime
import os
import time
import io
from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image
import hashlib
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import sqlalchemy
from sqlalchemy import types, create_engine, Column, Integer, String, and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import piexif
from collections import defaultdict

from_class=uic.loadUiType('database.ui')[0]
drive=webdriver.Chrome()
d_user=None
d_pw=None
d_DB=None
d_Table=None
pph=0
session=None
def set_DB(name,hash,time,driver):
    global d_user
    global d_pw
    global d_DB
    global d_Table
    global pph
    global session
    if(pph==0):
        engine = create_engine('mysql+pymysql://'+str(d_user)+':'+str(d_pw)+'@localhost/'+str(d_DB)+'?charset=utf8', convert_unicode=False)
        Session = sessionmaker(bind=engine)  # Create session object that can access query
        session = Session()
        Base = declarative_base()
        print("oo")
        class d_Table(Base):
            global d_Table
            __tablename__ = str(d_Table)
            idx = Column(types.Integer, primary_key=True)
            Time = Column(types.DateTime)
            File_Name = Column(types.String)
            Hash = Column(types.String)

            def __init__(self, name, times, hash):
                self.Time=times
                self.File_Name = name
                self.Hash = hash

            def __repr__(self):
                pass
        pph=1
    add_table=d_Table(str(name),time,str(hash))
    session.add(add_table)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    names = name.split('.')[0]
    names = str(names) + '.html'
    f = open(names, 'w+',encoding='UTF-8')
    f.write(str(soup))
    f.close()
    f_hash = open(names, 'rb')
    h_data = f_hash.read()
    f_hash.close()
    hash_d = hashlib.md5(h_data).hexdigest()
    time=datetime.datetime.now()
    add_table = d_Table(str(names), time, str(hash_d))
    session.add(add_table)
    session.commit()
    session.close()

def fullpage_screenshot(driver,f_name):
    drive.maximize_window()
    total_width = driver.execute_script("return document.body.parentNode.scrollWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")

    image_box = []

    x_point=0
    y_point=0
    x_len = viewport_width
    y_len = viewport_height

    pp=0
    while (1):
        y_inital=y_point
        while (1):
            image_box.append((x_point, y_point, viewport_width, viewport_height))
            print(y_point)
            y_point=viewport_height+y_point
            if(y_point+viewport_height>=total_height):
                y_point=total_height-viewport_height
                if(y_point==0):
                    break
                image_box.append((x_point, y_point, x_len, y_len))
                print(y_point)
                break
        if(pp==1):
            break
        y_point=y_inital
        x_point=viewport_width+x_point
        if(x_point+viewport_width>=total_width):
            x_point=total_width-viewport_width
            if(x_point==0):
                break
            else:
                pp=1

    Paper = Image.new('RGB', (total_width, total_height))
    j=0
    print(len(image_box))

    for i in image_box:
        files="aaa{0}.jpg".format(j)
        driver.execute_script("window.scrollTo({0},{1})".format(i[0],i[1]))
        time.sleep(0.3)
        driver.get_screenshot_as_file(files)
        s_shot=Image.open(files)

        size=(viewport_width,viewport_height)
        s_shot.thumbnail(size)
        gap=i[3]-s_shot.size[1]
        gap_x=i[2]-s_shot.size[0]
        if (gap_x != 0 and i[0] != 0):
            cc_x = int(i[0] - gap_x * (i[0] / viewport_width))
        else:
            cc_x = i[0]

        if(gap!=0 and i[1]!=0):
            cc=int(i[1]-gap*(i[1]/viewport_height))
        else:
            cc=i[1]

        offset=(cc_x,cc)
        Paper.paste(s_shot, offset)
        j+=1

    for i in range(0,len(image_box)):
        files="aaa{0}.jpg".format(i)
        os.remove(files)
    f_time = datetime.datetime.now()
    Paper.save(f_name)
    im=Image.open(f_name)
    try:
        exif_dict=piexif.load(im.info["exif"])
    except KeyError:
        exif_dict=defaultdict(dict)
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]=str(f_time)
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized]=str(f_time)
    exif_dict['0th'][piexif.ImageIFD.DateTime]=str(f_time)
    ex_byte=piexif.dump(exif_dict)
    im.save(f_name,"jpeg",exif=ex_byte)
    f_hash=open(f_name,'rb')

    h_data=f_hash.read()
    f_hash.close()
    hash_d=hashlib.md5(h_data).hexdigest()
    pa=set_DB(f_name,hash_d,f_time,driver)
    if(pa==-5):
        return -5




class MyWindow(QMainWindow,from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_click)
        self.pushButton_2.clicked.connect(self.btn_click2)
        self.pushButton_3.clicked.connect(self.btn_click3)
        self.lineEdit.setEchoMode(QLineEdit.Password)

    def btn_click(self):
        f_name = self.textEdit_6.toPlainText()
        if(f_name.split('.')[-1]!='jpg'):
            QMessageBox.about(self, "error", "Enter include FIle extension '.jpg'")
            return -1
        try:
            w_path=self.textEdit.toPlainText()
            drive.get(w_path)
            QMessageBox.about(self, "Wait...", "Click ok Later Please Wait sceonds")
            td=fullpage_screenshot(drive,f_name)
            if(td==-5):
                QMessageBox.about(self, "error", "Error Database inforamtion Check DB user information")
                return -1
            QMessageBox.about(self, "OK", "Complete Capture")
        except:
            QMessageBox.about(self, "error", "Error URL Path")

    def btn_click2(self):
        f_name=self.textEdit_6.toPlainText()
        if (f_name.split('.')[-1] != 'jpg'):
            QMessageBox.about(self, "error", "Enter include FIle extension '.jpg'")
            return -1
        url=drive.current_url
        drive.get(url)
        QMessageBox.about(self, "Wait...", "Click ok Later Please Wait sceonds")
        td=fullpage_screenshot(drive,f_name)
        if (td == -5):
            QMessageBox.about(self, "error", "Error Database inforamtion Check DB user information")
            return -1
        QMessageBox.about(self, "OK", "Complete Capture")

    def btn_click3(self):
        if(self.textEdit_2.toPlainText()=='' or self.textEdit_3.toPlainText()=='' or self.textEdit_4.toPlainText()=='' or self.lineEdit.text()==''):
            QMessageBox.about(self, "error", "Have to Enter DB Data ALL")
        else:
            global d_DB
            d_DB=self.textEdit_2.toPlainText()
            global d_Table
            d_Table = self.textEdit_3.toPlainText()
            global d_user
            d_user = self.textEdit_4.toPlainText()
            global d_pw
            d_pw = self.lineEdit.text()
            QMessageBox.about(self, "OK", "Complete Setting DB user")






if __name__=='__main__':
    app=QApplication(sys.argv)
    mywindow=MyWindow()
    mywindow.show()
    app.exec()