import socket #Used for hostname
import getpass #Used for username
import os #Various functions
import sys #Various functions
import platform #Various functions
import wmi #Various functions
import collections #Various functions
import colorama #Coloring
import _winreg #Various functions
import ctypes #Various functions
import datetime #Specificallyish for uptime
import subprocess #Various functions
import re #Various functions

from datetime import datetime
from colorama import init
init()
from colorama import Fore, Back, Style
from win32api import GetSystemMetrics

global ascii
global totalRam
global availableRam
global blackbox
blackbox = 0

print Style.BRIGHT

def get_registry_value(key, subkey, value):
    if sys.platform != 'win32':
        raise OSError("get_registry_value is only supported on Windows")
        
    import _winreg
    key = getattr(_winreg, key)
    handle = _winreg.OpenKey(key, subkey)
    (value, type) = _winreg.QueryValueEx(handle, value)
    return value

def ramValue():
	global totalRam
	global availableRam
        kernel32 = ctypes.windll.kernel32
        c_ulong = ctypes.c_ulong
        class MEMORYSTATUS(ctypes.Structure):
            _fields_ = [
                ('dwLength', c_ulong),
                ('dwMemoryLoad', c_ulong),
                ('dwTotalPhys', c_ulong),
                ('dwAvailPhys', c_ulong),
                ('dwTotalPageFile', c_ulong),
                ('dwAvailPageFile', c_ulong),
                ('dwTotalVirtual', c_ulong),
                ('dwAvailVirtual', c_ulong)
            ]
            
        memoryStatus = MEMORYSTATUS()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUS)
        kernel32.GlobalMemoryStatus(ctypes.byref(memoryStatus))
        totalRam = memoryStatus.dwTotalPhys
        availableRam = memoryStatus.dwAvailPhys


_ntuple_diskusage = collections.namedtuple('usage', 'total used free')

ascii_windows = [
	colorama.Fore.RED + " ,.=:!!t3Z3z., " + colorama.Fore.RESET,
	colorama.Fore.RED + " :tt:::tt333EE3 " + colorama.Fore.RESET,
	colorama.Fore.RED + " Et:::ztt33EEEL " + colorama.Fore.GREEN + "@Ee., ..," + colorama.Fore.RESET,
	colorama.Fore.RED + " ;tt:::tt333EE7 " + colorama.Fore.GREEN + ";EEEEEEttttt33#" + colorama.Fore.RESET,
	colorama.Fore.RED + " :Et:::zt333EEQ. " + colorama.Fore.GREEN + "$EEEEEttttt33QL" + colorama.Fore.RESET,
	colorama.Fore.RED + " ;3=*^````*4EEV " + colorama.Fore.GREEN + ":EEEEEEttttt33@." + colorama.Fore.RESET,
	colorama.Fore.BLUE + " ,.=::::!t=., ` " + colorama.Fore.GREEN + "@EEEEEEtttz33QF " + colorama.Fore.RESET,
	colorama.Fore.BLUE + " ;::::::::zt33) " + colorama.Fore.GREEN + "`4EEEtttji3P* " + colorama.Fore.RESET,
	colorama.Fore.BLUE + " :t::::::::tt33. " + colorama.Fore.YELLOW + ":Z3z.. `` ,..g. " + colorama.Fore.RESET,
	colorama.Fore.BLUE + " i::::::::zt33F " + colorama.Fore.YELLOW + "AEEEtttt::::ztF " + colorama.Fore.RESET,
	colorama.Fore.BLUE + " ;:::::::::t33V " + colorama.Fore.YELLOW + ";EEEttttt::::t3 " + colorama.Fore.RESET,
	colorama.Fore.BLUE + " E::::::::zt33L " + colorama.Fore.YELLOW + "@EEEtttt::::z3F " + colorama.Fore.RESET,
	colorama.Fore.BLUE + " {3=*^````*4E3) " + colorama.Fore.YELLOW + ";EEEtttt:::::tZ` " + colorama.Fore.RESET,
	colorama.Fore.BLUE + " ` " + colorama.Fore.YELLOW + "             :EEEEtttt::::z7 " + colorama.Fore.RESET,
	colorama.Fore.YELLOW + "                 `VEzjt:;;z>*` " + colorama.Fore.RESET,
]

def get_ascii():
	if platform.system() == 'Windows':
		return ascii_windows

ascii = get_ascii()

if os.name == 'nt':
    import ctypes
    import sys

    def disk_usage(path):
        _, total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong(), \
                           ctypes.c_ulonglong()
        if sys.version_info >= (3,) or isinstance(path, unicode):
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExW
        else:
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExA
        ret = fun(path, ctypes.byref(_), ctypes.byref(total), ctypes.byref(free))
        if ret == 0:
            raise ctypes.WinError()
        used = total.value - free.value
        return _ntuple_diskusage(total.value, used, free.value)
else:
    raise NotImplementedError("OS not supported for checking Disk Space.")

disk_usage.__doc__ = __doc__

def bytes2human(n):
    symbols = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

def Name(): #Name
	hostName = socket.gethostname()
	userName = getpass.getuser()
	print("%s" + Fore.RED + "                   Name: " + Fore.WHITE + userName + Fore.RED + "@" + Fore.WHITE + hostName) % ascii[1] 


def winKernel(): #Windows Kernel Version
	kerNel = platform.platform()
	print("%s" + Fore.RED + "          Kernel: " + Fore.WHITE + kerNel) % ascii[2]


def oS(): #Operating System
	oS = platform.win32_ver()
	if '6.1.' in oS[1]:
    		print("%s" + Fore.RED + "    Operating System: " + Fore.WHITE + "Windows 7 " + oS[2]) % ascii[3]
	elif '6.0.' in oS[1]:
    		print("%s" + Fore.RED + "    Operating System: " + Fore.WHITE + "Windows Vista" + oS[2]) % ascii[3]
	elif '6.2.' in oS[1]:
                print("%s" + Fore.RED + "    Operating System: " + Fore.WHITE + "Windows 8" + oS[2]) % ascii[3]
	elif '5.1.' in os[1]:
    		print("%s" + Fore.RED + "    Operating System: " + Fore.WHITE + "Windows XP" + oS[2]) % ascii[3]
	elif '5.0.' in oS[1]:
    		print("%s" + Fore.RED + "    Operating System: " + Fore.WHITE + "Windows 2000" + oS[2]) % ascii[3]
	else:
    		print("%s" + Fore.RED + "    Operating System: " + Fore.WHITE + platform.release()) % ascii[3]

def currentRamUsage(): #Ram Free and Maximum
    global availableRam
    global totalRam
    availableRam = availableRam / (1024*1024)
    totalRam = totalRam / (1024*1024)
    print(ascii[12] + Fore.RED + "  RAM: " + Fore.GREEN + "%sMB" + Fore.RED + "/" + Fore.BLUE + "%sMB") % (availableRam, totalRam)

def time_metric(secs=60): #Coded by aki--aki
    time = ''
    for metric_secs, metric_char in [[7*24*60*60, 'w '], [24*60*60, 'd '], [60*60, 'h '], [60, 'm ']]:
        if secs > metric_secs:
            time += '{}{}'.format(int(secs / metric_secs), metric_char)
            secs -= int(secs / metric_secs) * metric_secs
    if secs > 0:
        time += '{}s'.format(secs)
    return time

def winUpTime(): #Uptime coded by aki--aki
    from datetime import timedelta
    ret = ctypes.windll.kernel32.GetTickCount64()
    diff = timedelta(milliseconds = ret)
    print "%s %s  Uptime: %s%s" % (ascii[4], Fore.RED, Fore.WHITE, time_metric(diff.seconds))

#Shell Detect/bbLean Dectection Detection
def detectBBLean(): #Detect what shell is being used, currently only support Explorer and bbLean
    c = wmi.WMI ()
    global printed
    global blackbox
    for process in c.Win32_Process (name="blackbox.exe"):
        blackbox = blackbox+1

def winShell():
    global blackbox
    if blackbox == 1:
        print(ascii[6] + Fore.RED + "   Shell: " + Fore.WHITE + "bbLean")
    else:
        print(ascii[6] + Fore.RED + "   Shell: " + Fore.WHITE + "Explorer")
		

def screenRes(): #Screen Resolution
    print ascii[8], Fore.RED + " Resolution:" + Fore.WHITE, str(GetSystemMetrics (0)) + Fore.RED + "x" + Fore.WHITE + str(GetSystemMetrics(1))

def winProcessor(): #Processor
    print ascii[10] + Fore.RED + "   CPU:" + Fore.WHITE, get_registry_value("HKEY_LOCAL_MACHINE", "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0", "ProcessorNameString")

def winGPU(): #GPU/Graphics Card
    reg = subprocess.check_output(["wmic", "path", "Win32_VideoController", "get", "caption"]).split("\n")[1:]
    print ascii[11] + Fore.RED + "   GPU: " + Fore.WHITE + ", ".join(filter(bool, [s.strip() for s in reg]))
    

def diskMinMax(): #Disk max and free
	usage = disk_usage('C:\\')
	print ascii[13] + Fore.RED + "   Disk:" + Fore.GREEN, bytes2human(usage.free) + Fore.RED + "/" + Fore.BLUE + bytes2human(usage.total)

def screenShot(): #-s screenshot
    	from time import gmtime, strftime
	from PIL import ImageGrab
    	im = ImageGrab.grab()
    	im.save('pyFetch-' + strftime("%Y-%m-%d-%H-%M-%S", gmtime()) + ".png")

def winVisualStyle(): #Windows 7 Visual Style
	visualStyle = get_registry_value("HKEY_CURRENT_USER", "Software\Microsoft\Windows\CurrentVersion\ThemeManager", "DllName")
	visualStyle = visualStyle.split('\\')[-1].split(".")[0]
	print(ascii[7] + Fore.RED + "     Visual Style: " + Fore.WHITE + "%s") % (visualStyle)

def defaultBrowser(): #Default webbrowser
    browser = get_registry_value("HKEY_CURRENT_USER", "Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice", "Progid")
    for browser_ret, browser_str in [ ["FirefoxURL", "Mozilla Firefox"], ["ChromeHTML", "Google Chrome"] ]:
        if browser_ret in browser:
            print "%s %s  Browser: %s%s" % (ascii[5], Fore.RED, Fore.WHITE, browser_str)
            return None
    print "%s %s  Browser: %sUnknown" % (ascii[5], Fore.RED, Fore.WHITE)

print("")
print("")

print(ascii[0] + Fore.CYAN + "                   Info" ) #General Information
Name()
winKernel()
oS()
winUpTime()
defaultBrowser()

print(ascii[6] + Fore.CYAN + "  Theming") #Theming section
detectBBLean()
winShell()
winVisualStyle()
screenRes()

print(ascii[9] + Fore.CYAN + "  Hardware") #Hardware related statistics
winProcessor()
winGPU()
ramValue()
currentRamUsage()
diskMinMax()
print '\n'.join(ascii[14:])

try:
	if sys.argv[1] == "-s":
		screenShot()
except:
        None