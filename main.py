import struct
import os

FAT_list=[]
Full_EXT=[]
Full_Cluster=[]


def Mhash(key,value,pp):
    global Full_EXT
    global Full_Cluster
    if key in Full_Cluster:
        return 0
    Full_EXT.append(value)
    Full_Cluster.append(key)


def FAT_Entry(f,start,size):
    global FAT_list
    f.seek(start,0)
    Max=int((size-3)/4)
    c_number=0
    check=0
    while(c_number<=Max):
        read=f.read(4)
        if(struct.unpack_from(">I",read,0x0)[0]>=0 and struct.unpack_from(">I",read,0x0)[0]<=15 and check==0):
            FAT_list.append(c_number)
        c_number+=1

#Check FAT Entry
def check_FAT_Entry(C_before,secNumber_C,sector_size):
    global FAT_list
    complete=len(FAT_list)
    run_rules=int(complete/100)
    currnets=0
    for i in FAT_list:
        if(int(i/run_rules)>currnets and int(i/run_rules)<101):
            currnets+=1
            print("Running ",currnets,"%")
        try:
            f.seek(((i-2)+C_before)*secNumber_C*sector_size,0)
            sig_read=f.read(4)
            sig=struct.unpack_from(">I", sig_read, 0x00)[0]
        except:
            continue
        if(sig==0):  #This is real free
            continue
        elif(sig==1347093252):  #ZIP
            sig_read = f.read(4)
            sig = struct.unpack_from(">I", sig_read, 0x00)[0]
            if(sig!=335545856):
                f.read(22)
                namings=f.read(1)
                namings2=struct.unpack_from(">B",namings,0x0)[0]
                name=""
                name+=namings.decode('ascii')
                while(1):
                    while(namings2!=46 and namings2!=47):
                        namings = f.read(1)
                        namings2 = struct.unpack_from(">B", namings, 0x0)[0]
                        name += namings.decode('ascii')
                    if(namings2==47):
                        name=""
                        namings = f.read(1)
                        name+=namings.decode('ascii')
                        namings2 = struct.unpack_from(">B", namings, 0x0)[0]
                    elif(namings2==46):
                        break
                Mhash(i, "ZIP"+"  "+name,0)
            else:
                sig_read = f.read(4)
                sig = struct.unpack_from(">I", sig_read, 0x00)[0]
                if(sig!=134217728):
                    f.read(26)
                    namings = f.read(1)
                    namings2 = struct.unpack_from(">B", namings, 0x0)[0]
                    name = ""
                    name += namings.decode("ascii")
                    while (1):
                        while (namings2 != 46 or namings2 != 47):
                            name += namings.decode("ascii")
                        if (namings2 == 47):
                            name = ""
                        elif (namings2 == 46):
                            break
                    Mhash(i, "ZIP" + "  " + name,0)
                else:
                    f.seek(1010,1)
                    di=f.read(1)
                    di_a=struct.unpack_from(">B",di,0x00)[0]
                    while(di_a==0):
                        di = f.read(1)
                        di_a = struct.unpack_from(">B", di, 0x00)[0]
                    f.seek(-1,1)
                    di=f.read(4)
                    di_a=struct.unpack_from(">I",di,0x0)[0]
                    if(di_a==2895269199):
                        Mhash(i,"XLSX",0)
                    elif(di_a==2895298922):
                        Mhash(i,"DOCX",0)
                    elif(di_a==2895305546):
                        Mhash(i,"PPTX",0)
        elif(sig==626017350):   #PDF
            Mhash(i,'PDF',0)
        elif(sig==2303741511):  #PNG
            sig_read=f.read(4)
            sig = struct.unpack_from(">I", sig_read, 0x00)[0]
            if(sig==218765834):
                Mhash(i, 'PNG',0)
        elif(sig==4292411360):
            sig_read=f.read(2)
            sig=struct.unpack_from(">H",sig_read,0x00)[0]
            if(sig==65497):
                Mhash(i, 'JPEG',0)
        elif (sig == 4292411368):
            sig_read = f.read(2)
            sig = struct.unpack_from(">H", sig_read, 0x00)[0]
            if (sig == 65497):
                Mhash(i, 'JPEG',0)
        elif(sig==4292411361):
            Mhash(i,'JPG',0)
        elif(sig==24):
            sig_read = f.read(4)
            sig = struct.unpack_from(">I", sig_read, 0x00)[0]
            if(sig==1718909296):
                Mhash(i,'MP4',0)
        elif(sig==65544):
            Mhash(i,'IMG',0)
        elif(sig==707406368):
            sig_read = f.read(4)
            sig = struct.unpack_from(">I", sig_read, 0x00)[0]
            if (sig == 541683315):
                Mhash(i, 'LOG',0)





            #시그니처 확인 파일이름 클러스터번호 입력
        #0인애들은 무시

def Check_Cluster(f,c_number,default,dirbit):
    f.seek(0,0)
    boot = f.read(512)
    C_before = struct.unpack_from("<I", boot, 0x1C)[0]
    Snumber_reserve = struct.unpack_from("<H", boot, 0x0E)[0]
    sector_size = struct.unpack_from("<H", boot, 0x0B)[0]
    secNumber_C = struct.unpack_from("<B", boot, 0x0D)[0]
    f.seek(Snumber_reserve*sector_size,0)
    f.read(c_number*4)
    live=f.read(4)
    c_offset=struct.unpack_from("<I",live,0x0)[0]
    if(c_offset!=0 and dirbit==0):
        f.seek(0,0)
        f.read(default)
        return -1

    f.seek(0,0)
    f.read(default)
    return ((c_number-2)+C_before)*secNumber_C*sector_size





    #루트디렉토리 순환
def Reading_dir(f2,seeks,adder):
    f2.seek(seeks)
    if(adder!=0):
        f2.read(adder)
    lens=0
    names=[]
    while(1):
        data_dir=f2.read(32)
        status=struct.unpack_from("<B",data_dir,0x0)[0]
        formal=struct.unpack_from("<B",data_dir,0x0B)[0]
        upper=struct.unpack_from("<H",data_dir,0x14)[0]
        down=struct.unpack_from("<H",data_dir,0x1A)[0]
        ext1=struct.unpack_from("<B",data_dir,0x08)[0]
        ext2 = struct.unpack_from("<B", data_dir, 0x09)[0]
        ext3 = struct.unpack_from("<B", data_dir, 0x0A)[0]
        ext=chr(ext1)+chr(ext2)+chr(ext3)
        c_number=upper*65536+down
        if(formal==15):
            lens+=1
            continue
        elif(formal==16):
            if(status==229):
                lens=0
                continue
            else:
                a=Check_Cluster(f2,c_number,f2.tell(),1)
                Reading_dir(f2,a,64)
                lens=0
        elif(status==229):
            a=Check_Cluster(f2,c_number,f2.tell(),0)
            if(a==-1):
                lens = 0
                continue
            Mhash(c_number,ext,1)
            lens=0
        else:
            lens=0




        if(status==0 and formal==0):
            #print("tell"+str(f2.tell()))
            break

if __name__=='__main__':
    print("Input Drive Name")
    D_name=input()
    f=open('\\\\.\\'+str(D_name)+':','rb')
    f.seek(0)
    i=0
    boot=f.read(512)
    sector_size=struct.unpack_from("<H",boot,0x0B)[0]
    secNumber_C=struct.unpack_from("<B",boot,0x0D)[0]
    Snumber_reserve=struct.unpack_from("<H",boot,0x0E)[0]   #Sector number of reserve space
    Snumber_fat=struct.unpack_from("<I",boot,0x24)[0]   #Sector number of fat
    Rdir=(struct.unpack_from("<I",boot,0x1C)[0]*sector_size*secNumber_C)    #Fat1+Fat2(back up)+reserve space
    C_before=struct.unpack_from("<I",boot,0x1C)[0]
    FAT_NUM=struct.unpack_from("<B",boot,0x10)[0]

    #1
    print("Wating... Calcuminate Free Cluster")
    FAT_Entry(f, Snumber_reserve * sector_size, Snumber_fat * sector_size)
    print("Running 0%")
    check_FAT_Entry(int(((Snumber_fat*FAT_NUM)+Snumber_reserve)/secNumber_C),secNumber_C,sector_size)

    Reading_dir(f,Rdir,0)
    j=0
    for i in Full_Cluster:
        print(i," ",Full_EXT[j])
        j+=1
