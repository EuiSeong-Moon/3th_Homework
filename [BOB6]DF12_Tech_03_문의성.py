import piexif
import struct
import datetime
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic

x=0
y=0
from_class=uic.loadUiType('exifui.ui')[0]
path_dictionary=dict()

def image_size(f):  #Find Image_size in SOF
    global x
    global y
    tag=0
    sof_pack=f.read(1)
    sof=struct.unpack_from(">B",sof_pack,0x0)[0]    #Read Big Endian 1byte
    while(True):
        if(sof==255):
            sof_pack=f.read(1)
            sof = struct.unpack_from(">B", sof_pack, 0x0)[0]
            if(sof==192):
                tag+=1
        if(tag==2):
            break
        sof_pack=f.read(1)
        sof = struct.unpack_from(">B", sof_pack, 0x0)[0]
    f.seek(3,1) #current + 3byte(jump to sof image size)
    read_size=f.read(4)
    x=struct.unpack_from(">H",read_size,0x0)[0]
    y=struct.unpack_from(">H",read_size,0x02)[0]

def group(f,exif):
    fake_size=0
    fake_date=1
    global x
    global y

    #If image_size != PixelXDimension(ExifImageWidth) or PIxelYDimension(ExifImageHeight) is fake_size=1
    #if there is more than 2 seconds between EXIF time and FIleSystem Modify time, fake_date=1
    x=0
    y=0
    image_size(f)
    for i in exif:
        if (i == 'thumbnail'):
            continue
        for j in exif[i]:
            if(str(piexif.TAGS[i][j]["name"])=='PixelXDimension'):
                if(exif[i][j]!=y):
                    fake_size=1
            if (str(piexif.TAGS[i][j]["name"]) == 'PixelYDimension'):
                if(exif[i][j]!=x):
                    fake_size=1
            if(str(piexif.TAGS[i][j]["name"])=='DateTime'):
                etime=datetime.datetime.strptime(exif[i][j].decode(),"%Y:%m:%d %H:%M:%S")
            if (str(piexif.TAGS[i][j]["name"]) == 'DateTimeOriginal'):
                otime = datetime.datetime.strptime(exif[i][j].decode(), "%Y:%m:%d %H:%M:%S")
            if (str(piexif.TAGS[i][j]["name"]) == 'DateTimeDigitized'):
                dtime = datetime.datetime.strptime(exif[i][j].decode(), "%Y:%m:%d %H:%M:%S")
    if(etime==otime and etime==dtime):  #original, Digital, Date time are same
        fake_date=0
    if(fake_size==0 and fake_date==0):  #clean
        return 1
    if(fake_size==1 and fake_date==0):  #dirty size
        return 2
    if (fake_size==0 and fake_date==1): #dirty date
        return 3
    if (fake_size==1 and fake_date==1):
        return 4



class MyWindow(QMainWindow,from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_click)
        self.listWidget.itemClicked.connect(self.item_click)
        self.listWidget_2.itemClicked.connect(self.item_click2)
        self.listWidget_3.itemClicked.connect(self.item_click3)


    def btn_click(self):
        global x
        global y
        global path_dictionary
        path = self.textEdit.toPlainText()
        name=path.split('\\')[-1]
        path_dictionary[name]=path
        try:
            f=open(path,'rb')
            exif_data=piexif.load(path)
        except:
            print("path error")
            QMessageBox.about(self, "error", "Path error")
            exit(1)

        status=group(f, exif_data)
        if(status==1):
            self.listWidget.addItem(name)
        elif(status==2):
            self.listWidget_2.addItem(name)
        elif(status==3):
            self.listWidget_3.addItem(name)
        elif(status==4):
            self.listWidget_3.add(name)
            self.listWidget_2.add(name)

#Group 1 Item Click
    def item_click(self,item):
        self.textBrowser_4.clear()
        self.textBrowser_4.append("No Fake This is True")
        view_data(self,item.text())
#Group 2 Item Click
    def item_click2(self, item):
        self.textBrowser_4.clear()
        self.textBrowser_4.append("Size is Fake(PixelXYDimension)")
        view_data(self, item.text())
#Group 3 Item Click
    def item_click3(self, item):
        self.textBrowser_4.clear()
        self.textBrowser_4.append("Date is Fake(Datetime)")
        view_data(self, item.text())


def view_data(self,name):
    global path_dictionary
    exif_data=piexif.load(path_dictionary[name])
    for i in exif_data:
        if (i == 'thumbnail'):
            continue
        self.textBrowser_4.append('-'+i)
        for j in exif_data[i]:
            self.textBrowser_4.append(" "+str(piexif.TAGS[i][j]["name"])+":"+str(exif_data[i][j]))

if __name__=='__main__':
    app=QApplication(sys.argv)
    mywindow=MyWindow()
    mywindow.show()
    app.exec()



