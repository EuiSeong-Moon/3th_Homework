from winreg import *
import Evtx.Evtx as evtx
import sys
import string
from datetime import datetime, timedelta, tzinfo
import struct
import time
import csv


class USB_Class:
    def __init__(self):
        self.serial = None
        self.s_time = None
        self.f_stime = []
        self.D_name = None
        self.V_name = None
        self.M_name = None
        self.f_ftime = []
        self.evt_life = []
        self.execute_t = []
        self.execute_n = []
        self.execute_num = []

    def set_exe(self, a, b, c):
        self.execute_t.append(a)
        self.execute_n.append(b)
        self.execute_num.append(c)

    def set_usbstor(self, a, b):
        self.serial = a
        self.D_name = b

    def set_v(self, a):
        self.V_name = a

    def set_M(self, a):
        self.M_name = a

    def set_fstime(self, a):
        self.f_stime.append(a)

    def set_fftime(self, a, index):
        self.f_ftime.append(a)
        self.f_ftime[index] = a

    def set_e_life(self, a):
        self.evt_life.append(a)

    def set_stime(self, a):
        self.s_time = a


usb_barket = []
Usb_class_barket = []


def check_time(c, t):
    j = 0
    for i in c.f_stime:
        import datetime
        i = datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
        k = datetime.datetime.strptime(c.f_ftime[j], '%Y-%m-%d %H:%M:%S')

        if (t - i > datetime.timedelta(seconds=0) and k - t > datetime.timedelta(seconds=0)):
            return j

        j += 1
    return -1


def index_serial(serial):
    try:
        return usb_barket.index(serial)
    except:
        return -1


for ii in range(9):
    ii += 1
    ccc = 'ControlSet00'
    ccc = ccc + str(ii)
    print(ccc)
    try:
        varSubkey = 'SYSTEM\\' + ccc + '\\Enum\\USBSTOR'
        varReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        varkey = OpenKey(varReg, varSubkey)
    except:
        print('break')
        break

    for i in range(1024):
        try:
            keyname = EnumKey(varkey, i)
            varSubkey2 = "%s\\%s" % (varSubkey, keyname)
            varkey2 = OpenKey(varReg, varSubkey2)

            try:
                for j in range(1024):
                    keyname3 = EnumKey(varkey2, j)
                    varSubkey3 = "%s\\%s" % (varSubkey2, keyname3)
                    varkey3 = OpenKey(varReg, varSubkey3)
                    try:
                        for k in range(1024):
                            index = 0
                            if (index_serial(keyname3) == -1):
                                index = len(usb_barket)
                                usb_barket.append(keyname3)
                                a = USB_Class()
                                Usb_class_barket.append(a)
                            else:
                                index = index_serial(keyname3)

                            n, v, t = EnumValue(varkey3, k)
                            if (n == 'FriendlyName'):
                                print('index', index)
                                Usb_class_barket[index].set_usbstor(keyname3, v)
                    except:
                        print("3")
                    CloseKey(varkey3)
            except:
                print("2")

        except:
            break
        CloseKey(varkey2)
print('---------------------')
varSubkey = 'SOFTWARE\\Microsoft\\Windows Portable Devices\\Devices'
varReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
varkey = OpenKey(varReg, varSubkey)

for i in range(1024):
    try:
        keyname = EnumKey(varkey, i)
        varSubkey2 = "%s\\%s" % (varSubkey, keyname)
        varkey2 = OpenKey(varReg, varSubkey2)
        try:
            for j in range(1024):
                keys = keyname.split('#')[-2]
                keys = keys.lower()

                index = index_serial(keys)
                if (index == -1):
                    index = index_serial(keys.upper())
                n, v, t = EnumValue(varkey2, j)
                if (index != -1 and n == 'FriendlyName'):
                    Usb_class_barket[index].set_M(v)

        except:
            print("2")
    except:
        break
    CloseKey(varkey2)

print('----------------------')
varSubkey = 'SYSTEM\\ControlSet001\\Enum\\WpdBusEnumRoot\\UMB'
varReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
varkey = OpenKey(varReg, varSubkey)

for i in range(1024):
    try:
        keyname = EnumKey(varkey, i)
        varSubkey2 = "%s\\%s" % (varSubkey, keyname)
        varkey2 = OpenKey(varReg, varSubkey2)
        try:
            for j in range(1024):
                keys = keyname.split('#')[-2]
                keys = keys.lower()
                index = index_serial(keys)
                if (index == -1):
                    index = index_serial(keys.upper())
                n, v, t = EnumValue(varkey2, j)
                if (index != -1 and n == 'FriendlyName'):
                    Usb_class_barket[index].set_v(v)
        except:
            print("2")
    except:
        break
    CloseKey(varkey2)


def get_child(node, tag, ns="{http://schemas.microsoft.com/win/2004/08/events/event}"):
    """
    @type node: etree.Element
    @type tag: str
    @type ns: str
    """
    return node.find("%s%s" % (ns, tag))


def parsing_evt(epath):
    with evtx.Evtx(epath) as log:
        for record in log.records():
            node = record.lxml()
            # print(record.xml())
            if (int(get_child(get_child(node, "System"), "EventID").text) == 2003):
                test = record.xml().split('UserData')[1].split('#')[4]
                testss = ''
                for jj in test.split('amp;'):
                    testss += jj
                test = testss
                time = record.xml().split('TimeCreated SystemTime="')[1].split('.')[0]
                lifetime = record.xml().split('lifetime="')[1].split('"')[0]
                index = index_serial(test)
                Usb_class_barket[index].set_fstime(time)
                Usb_class_barket[index].set_e_life(lifetime)


            elif (int(get_child(get_child(node, "System"), "EventID").text) == 2100):
                test = record.xml().split('UserData')[1].split('#')[4]
                testss = ''
                for jj in test.split('amp;'):
                    testss += jj
                test = testss
                time = record.xml().split('TimeCreated SystemTime="')[1].split('.')[0]
                lifetime = record.xml().split('lifetime="')[1].split('"')[0]

                index = index_serial(test)
                index2 = Usb_class_barket[index].evt_life.index(lifetime)
                Usb_class_barket[index].set_fftime(time, index2)


f = open('C:\\Windows\\inf\\setupapi.dev.log', 'r')
lines = f.readlines()
kkk = 0
# print('ssss')
no_ovlap = []
indexss = None
for line in lines:
    if (kkk == 2):
        # print('aaabbbbba')
        time = line.split('start ')[1].split('.')[0]
        Usb_class_barket[indexss].set_stime(time)
        kkk = 0
    if (line.find(">>>  [Device Install (Hardware initiated) - USBSTOR") != -1):
        serial = line.split('\\')[-1].split(']')[0]
        if (serial in no_ovlap):
            continue
        no_ovlap.append(serial)
        indexss = index_serial(serial)
        # print(indexss)
        kkk = 2

epath = 'C:\\windows\\system32\\winevt\\logs\\Microsoft-Windows-DriverFrameworks-UserMode%4Operational.evtx'
parsing_evt(epath)

varSubkey = 'Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\Shell\\BagMRU'
varReg = ConnectRegistry(None, HKEY_CURRENT_USER)
varkey = OpenKey(varReg, varSubkey)

WIN32_EPOCH = datetime(1601, 1, 1)


def dt_from_win32_ts(timestamp):
    return WIN32_EPOCH + timedelta(microseconds=timestamp // 10)


def circuit(key_n, var_s, varReg, data, nnn):
    ppp = 0
    try:
        for ii in range(1024):
            keyname = EnumKey(key_n, ii)

            varSubkey = '%s\\%s' % (var_s, keyname)
            varkey = OpenKey(varReg, varSubkey)
            if (str(keyname) == str(nnn)):
                for jj in range(1024):
                    n, v, t = EnumValue(varkey, jj)

                    if (n != 'MRUListEx' and n != 'NodeSlot'):
                        ppp = 1

                        ts = QueryInfoKey(varkey)[2]
                        # print('777777777')
                        dt = dt_from_win32_ts(ts)
                        #  print('88888888')
                        indexxx = -1
                        lll = 0
                        for i in Usb_class_barket:
                            # print(type(dt))
                            indexxx = check_time(i, dt)  # dt.strftime('%Y-%m-%d %H:%M:%S')
                            #  print('indexxx',indexxx)
                            if (indexxx != -1):
                                break
                            lll += 1
                        print(indexxx)

                        test1 = struct.unpack_from('>B', v, 0x2E)[0]
                        kking = 46
                        while (test1 == 0):
                            kking += 1
                            test1 = struct.unpack_from('>B', v, kking)[0]

                        pp = 0
                        ffing = kking
                        while (pp == 0):
                            ffing += 1
                            test1 = struct.unpack_from('>B', v, ffing)[0]

                            if (test1 == 0):
                                ffing += 1
                                test1 = struct.unpack_from('>B', v, ffing)[0]

                                if (test1 == 0):
                                    ffing += 1
                                    test1 = struct.unpack_from('>B', v, ffing)[0]

                                    if (test1 == 0):
                                        ffing -= 3
                                        break

                        name_ms = v[kking:ffing + 2].decode('utf-16')
                        print(name_ms)
                        Usb_class_barket[lll].set_exe(dt, data + name_ms + '\\', indexxx)

                        circuit(varkey, varSubkey, varReg, data + name_ms + '\\', n)
    except:
        if (ppp == 0):
            print("")


for i in range(1024):
    try:
        keyname = EnumKey(varkey, i)
        varSubkey2 = "%s\\%s" % (varSubkey, keyname)
        varkey2 = OpenKey(varReg, varSubkey2)
        if (keyname == '1'):

            try:
                for j in range(1024):

                    n, v, t = EnumValue(varkey2, j)
                    if (n != 'MRUListEx' and n != 'NodeSlot'):
                        v = v.decode('utf-8')
                        v = v.split('\\')[0].split('/')[1]
                        if (v == 'C:' or v == 'c:'):
                            continue

                        circuit(varkey2, varSubkey2, varReg, v, n)
            except:
                print("")
    except:
        break
    CloseKey(varkey2)

print('----------------------------')
outputs = open('output.csv', 'w+', encoding='utf-8', newline='')
wr = csv.writer(outputs)
wr.writerow(
    ['Seiral', 'Volume_name', 'Mount_name', 'Device_name', 'USB_start_time(UTC)', 'USB_Finish_time(UTC)', 'Init_connect_time(UTC+9)',
     'Execute_name', 'Execute_time(UTC)'])
out_data = []
exe_data = []
q = 0
k = 0
nn = 0
for i in Usb_class_barket:
    for j in i.f_stime:
        out_data.clear()
        out_data.append(i.serial)
        out_data.append(i.V_name)
        out_data.append(i.M_name)
        out_data.append(i.D_name)
        out_data.append(j)
        out_data.append(i.f_ftime[k])
        out_data.append(i.s_time)
        print(i.serial)
        print(i.V_name)
        print(i.M_name)
        print(i.D_name)
        print(j)
        print(i.f_ftime[k])
        print(i.s_time)  # utc+9
        for m in i.execute_num:
            if (m == k):
                exe_data.clear()
                exe_data.append(i.execute_n[nn])
                exe_data.append(i.execute_t[nn].strftime('%Y-%m-%d %H:%M:%S'))
                q = 1

                print(i.execute_n[nn])
                print(i.execute_t[nn].strftime('%Y-%m-%d %H:%M:%S'))

                wr.writerow([str(out_data[0]), str(out_data[1]), str(out_data[2]), str(out_data[3]), str(out_data[4]),
                             str(out_data[5]), str(out_data[6]), str(exe_data[0]), str(exe_data[1])])

            nn += 1

        if (q == 1):
            q = 0
        else:
            wr.writerow([str(out_data[0]), str(out_data[1]), str(out_data[2]), str(out_data[3]), str(out_data[4]),
                         str(out_data[5]), str(out_data[6])])

        nn = 0
        k += 1
    k = 0
print('----------------------------')
outputs.close()
