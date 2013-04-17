import socket, getpass, os, sys, platform, wmi, collections, win32api, colorama
from colorama import init
init()
from colorama import Fore, Back, Style
from win32api import GetSystemMetrics
global printed
printed = 0

_ntuple_diskusage = collections.namedtuple('usage', 'total used free')

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
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

#Name
def Name():
	hostName = socket.gethostname()
	userName = getpass.getuser()
	print Fore.RED + "       :tt:::tt333EE3" + Fore.RED + "                Name: " + Fore.WHITE + userName + "@" + hostName


#Windows Kernel Version?
def winKernel():
	kerNel = platform.platform()
	print Fore.RED + "       Et:::ztt33EEEL " + Fore.GREEN + "@Ee.,      ..," + Fore.RED + " Kernel: " + Fore.WHITE + kerNel

#Operating System
def oS():
	oS = platform.win32_ver()
	if '6.1.' in oS[1]:
    		print Fore.RED + "      ;tt:::tt333EE7 " + Fore.GREEN + ";EEEEEEttttt33#" + Fore.RED + " Operating System: " + Fore.WHITE + "Windows 7 " + oS[2]
	elif '5.1.' in oS[1]:
    		print Fore.RED + "      ;tt:::tt333EE7 " + Fore.GREEN + ";EEEEEEttttt33#" + Fore.RED + " Operating System: " + Fore.WHITE + "Windows Vista" + oS[2]
	elif 'XP' or 'xp' in platform.release():
    		print Fore.RED + "      ;tt:::tt333EE7 " + Fore.GREEN + ";EEEEEEttttt33#" + " Operating System: " + Fore.WHITE + "Windows XP" + oS[2]
	else:
    		print Fore.RED + "      ;tt:::tt333EE7 " + Fore.GREEN + ";EEEEEEttttt33#" + Fore.RED + " Operating System: " + Fore.WHITE + platform.release()

#RAM Usage // Not coded yet, can't find a good way.


#Uptime
def winUpTime():   
	upTime = os.popen("net stats srv").readlines()
	upTime = upTime[3]
	upTime = upTime.split(" ")
	upTime = upTime[3]
	print(Fore.RED + "     :Et:::zt333EEQ. " + Fore.GREEN + "$EEEEEttttt33QL" + Fore.RED + " Up Since: " + Fore.WHITE + "%s" % (upTime))


#Theme // Uncoded, don't know how to find


#Shell Detect/bbLean Dectection Detection
def detectBBLean():
	c = wmi.WMI ()
	global printed
	for process in c.Win32_Process (name="explorer.exe"):
		printed = 1
		print Fore.RED +  "     ,.=::::!t=., ` " + Fore.GREEN + "@EEEEEEtttz33QF"  + Fore.RED + "  Shell: " + Fore.WHITE + "Explorer"
	for process in c.Win32_Process (name="blackbox.exe"):
		if printed == 1:
                    None
		else:
		    print "     ,.=::::!t=., ` @EEEEEEtttz33QF" + Fore.RED + "  Shell: " + Fore.WHITE + "bbLean"

def screenRes():
    print Fore.RED +  "    ;::::::::zt33)   " + Fore.GREEN + "`4EEEtttji3P*" + Fore.RED + "   Resolution:" + Fore.WHITE, GetSystemMetrics (0), Fore.BLUE + "x", Fore.WHITE + str(GetSystemMetrics(1))

def winProcessor():
    print Fore.CYAN + "   i::::::::zt33F" + Fore.YELLOW + " AEEEtttt::::ztF" + Fore.RED + "    CPU:" + Fore.WHITE, platform.processor()

def diskMinMax():
	usage = disk_usage('C:\\')
	print Fore.CYAN + "   ;:::::::::t33V " + Fore.YELLOW + ";EEEttttt::::t3"  + Fore.RED + "    Disk:" + Fore.WHITE, bytes2human(usage.free) + "/" + bytes2human(usage.total)

def ansiArt():
	print Fore.CYAN + "  E::::::::zt33L " + Fore.YELLOW +"@EEEtttt::::z3F"
	print Fore.CYAN + " {3=*^````*4E3)  " + Fore.YELLOW +";EEEtttt:::::tZ`"
	print Fore.CYAN + "             ` " + Fore.YELLOW + ":EEEEtttt::::z7"
	print Fore.CYAN + "                 " + Fore.YELLOW + "`VEzjt:;;z>*`"

def screenShot():
    	from time import gmtime, strftime
	from PIL import ImageGrab
    	im = ImageGrab.grab()
    	im.save('pyFetch-' + strftime("%Y-%m-%d-%H-%M-%S", gmtime()) + ".png")

print(Fore.RED + "         ,.=:!!t3Z3z.," + Fore.GREEN + "               Info" )
Name()
winKernel()
oS()
winUpTime()
print( Fore.RED + "     ;3=*^````*4EEV " + Fore.GREEN + ":EEEEEEttttt33@." + Fore.GREEN + " Theming")
detectBBLean()
screenRes()
print( Fore.CYAN + "   :t::::::::tt33. " + Fore.YELLOW + ":Z3z..  `` ,..g." + Fore.GREEN + "  Hardware")
winProcessor()
diskMinMax()
ansiArt()
try:
	if sys.argv[1] == "-s":
		screenShot()
except:
        None







