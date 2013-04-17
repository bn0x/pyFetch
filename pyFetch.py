import socket, getpass, os, sys, platform, wmi, collections, colorama
from colorama import init
init()
from colorama import Fore, Back, Style
from win32api import GetSystemMetrics
global printed
printed = 0
global ascii

print Style.BRIGHT


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

#Name
def Name():
	hostName = socket.gethostname()
	userName = getpass.getuser()
	print("%s" + Fore.RED + "                  Name: " + Fore.WHITE + userName + Fore.RED + "@" + Fore.WHITE + hostName) % ascii[1] 


#Windows Kernel Version?
def winKernel():
	kerNel = platform.platform()
	print("%s" + Fore.RED + "         Kernel: " + Fore.WHITE + kerNel) % ascii[2]

#Operating System
def oS():
	oS = platform.win32_ver()
	if '6.1.' in oS[1]:
    		print("%s" + Fore.RED + "   Operating System: " + Fore.WHITE + "Windows 7 " + oS[2]) % ascii[3]
	elif '6.0.' in oS[1]:
    		print("%s" + Fore.RED + "   Operating System: " + Fore.WHITE + "Windows Vista" + oS[2]) % ascii[3]
	elif '6.2.' in oS[1]:
                print("%s" + Fore.RED + "   Operating System: " + Fore.WHITE + "Windows 8" + oS[2]) % ascii[3]
	elif '5.1.' in os[1]:
    		print("%s" + Fore.RED + "   Operating System: " + Fore.WHITE + "Windows XP" + oS[2]) % ascii[3]
	elif '5.0.' in oS[1]:
    		print("%s" + Fore.RED + "   Operating System: " + Fore.WHITE + "Windows 2000" + oS[2]) % ascii[3]
	else:
    		print("%s" + Fore.RED + "   Operating System: " + Fore.WHITE + platform.release()) % ascii[3]

#RAM Usage // Not coded yet, can't find a good way.


#Uptime
def winUpTime():   
	upTime = os.popen("net stats srv").readlines()
	upTime = upTime[3]
	upTime = upTime.split(" ")
	upTime = upTime[3]
	print("%s" + Fore.RED + "  Up Since: " + Fore.WHITE + "%s" % (upTime)) % ascii[4]


#Theme // Uncoded, don't know how to find


#Shell Detect/bbLean Dectection Detection
def detectBBLean():
	c = wmi.WMI ()
	global printed
	for process in c.Win32_Process (name="explorer.exe"):
		printed = 1
		print("%s" + Fore.RED + "  Shell: " + Fore.WHITE + "Explorer") % ascii[6]
	for process in c.Win32_Process (name="blackbox.exe"):
		if printed == 1:
                    None
		else:
		    print("%s" + Fore.RED + "  Shell: " + Fore.WHITE + "bbLean") % ascii[6]

def screenRes():
    print ascii[7], Fore.RED + "   Resolution:" + Fore.WHITE, str(GetSystemMetrics (0)) + Fore.RED + "x" + Fore.WHITE + str(GetSystemMetrics(1))

def winProcessor():
    print ascii[8] + Fore.RED + " CPU:" + Fore.WHITE, platform.processor()

def diskMinMax():
	usage = disk_usage('C:\\')
	print ascii[9] + Fore.RED + "  Disk:" + Fore.GREEN, bytes2human(usage.free) + Fore.RED + "/" + Fore.BLUE + bytes2human(usage.total)

def screenShot():
    	from time import gmtime, strftime
	from PIL import ImageGrab
    	im = ImageGrab.grab()
    	im.save('pyFetch-' + strftime("%Y-%m-%d-%H-%M-%S", gmtime()) + ".png")

print("")
print("")
print(ascii[0] + Fore.CYAN + "                    Info" )
Name()
winKernel()
oS()
winUpTime()
print(ascii[5] + Fore.CYAN + "   Theming")
detectBBLean()
screenRes()
print(ascii[8] + Fore.CYAN + "  Hardware")
#winProcessor()
diskMinMax()
print '\n'.join(ascii[11:])
try:
	if sys.argv[1] == "-s":
		screenShot()
except:
        None







