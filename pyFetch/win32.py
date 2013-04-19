import os
import platform
import ctypes
import subprocess
import re
import _winreg
import wmi
import win32gui
import win32ui
import win32con
import win32api
from win32api import GetSystemMetrics
from datetime import datetime, timedelta
from colorama import Fore, Back, Style

win8_ascii = [
                "                     ",
    Fore.CYAN + "                _.,, ",
    Fore.CYAN + "          ,::::::::: ",
    Fore.CYAN + " ,.:::::: :::::::::: ",
    Fore.CYAN + " ,::::::: :::::::::: ",
    Fore.CYAN + " ,::::::: :::::::::: ",
    Fore.CYAN + " ,::::::: :::::::::: ",
    Fore.CYAN + " '.:::::: :::::::::: ",
    Fore.CYAN + "                     ",
    Fore.CYAN + " ,.:::::: :::::::::: ",
    Fore.CYAN + " ,::::::: :::::::::: ",
    Fore.CYAN + " ,::::::: :::::::::: ",
    Fore.CYAN + " ,::::::: :::::::::: ",
    Fore.CYAN + " '.:::::: :::::::::: ",
    Fore.CYAN + "   .::::: :::::::::: ",
    Fore.CYAN + "           ':::::::: ",
]

winX_ascii = [
                  "              " +               "                      ",
    Fore.RED    + "        ,.=:!!t3Z3z., " +               "               " + Fore.RESET,
    Fore.RED    + "       :tt:::tt333EE3 " +               "               " + Fore.RESET,
    Fore.RED    + "       Et:::ztt33EEEL " + Fore.GREEN  + "@Ee.,      .., " + Fore.RESET,
    Fore.RED    + "      ;tt:::tt333EE7 " + Fore.GREEN  + ";EEEEEEttttt33#" + Fore.RESET,
    Fore.RED    + "     :Et:::zt333EEQ." + Fore.GREEN  + " $EEEEEttttt33QL " + Fore.RESET,
    Fore.RED    + "     it::::tt333EEF " + Fore.GREEN + "@EEEEEEttttt33F  " + Fore.RESET,
    Fore.RED    + "    ;3=*^```\"*4EEV " + Fore.GREEN  + ":EEEEEEttttt33@.  " + Fore.RESET,
    Fore.CYAN   + "    ,.=::::!t=., " + Fore.GREEN  + "  @EEEEEEtttz33QF   " + Fore.RESET,
    Fore.CYAN   + "   ;::::::::zt33)   " + Fore.GREEN  + "\"4EEEtttji3P*    " + Fore.RESET,
    Fore.CYAN   + "  :t::::::::tt33." + Fore.YELLOW + ":Z3z.. " + Fore.GREEN + "``" + Fore.YELLOW +  ",..g.      " + Fore.RESET,
    Fore.CYAN   + "  i::::::::zt33F" + Fore.YELLOW + " AEEEtttt::::ztF    " + Fore.RESET,
    Fore.CYAN   + " ;::::::::t33V " + Fore.YELLOW + " ;EEEttttt::::t3      " + Fore.RESET,
    Fore.CYAN   + " E::::::::zt33L" + Fore.YELLOW + " @EEEtttt::::z3F      " + Fore.RESET,
    Fore.CYAN   + "{3=*^```\"*4E3) " + Fore.YELLOW + ";EEEtttt:::::tZ`     " + Fore.RESET,
    Fore.CYAN   + "               " + Fore.YELLOW + ":EEEEtttt::::z7       " + Fore.RESET,
    Fore.YELLOW + "               " +               "  \"VEzjt:;;z>*`       " + Fore.RESET,
]

if float(platform.win32_ver()[1][:3]) > 6.1:
    ascii_art = win8_ascii
else:
    ascii_art = winX_ascii

def get_registry_value(key, subkey, value):
    """\
    Get a value from the Windows registry.

    :param key: string
    :param subkey: string
    :param value: string
    """

    key = getattr(_winreg, key)
    
    for x in subkey.split("\\"):
        key = _winreg.OpenKeyEx(key, x)

    (value, type) = _winreg.QueryValueEx(key, value)
    return value

class MEMORYSTATUS(ctypes.Structure):
    """\
    Structure as defined by the `Windows API <http://msdn.microsoft.com/en-us/library/aa366770(v=vs.85).aspx>`
    for getting values from the GlobalMemoryStatus() API call.
    """

    _fields_ = [
        ('dwLength', ctypes.c_ulong),
        ('dwMemoryLoad', ctypes.c_ulong),
        ('dwTotalPhys', ctypes.c_ulong),
        ('dwAvailPhys', ctypes.c_ulong),
        ('dwTotalPageFile', ctypes.c_ulong),
        ('dwAvailPageFile', ctypes.c_ulong),
        ('dwTotalVirtual', ctypes.c_ulong),
        ('dwAvailVirtual', ctypes.c_ulong),
    ]

def ram():
    """\
    Get RAM statistics.
    Returns a dict with items 'total', 'used' and 'free' as bytes.

    :rtype: dict
    """

    memoryStatus = MEMORYSTATUS()
    memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUS)
    ret = ctypes.windll.kernel32.GlobalMemoryStatus(ctypes.byref(memoryStatus))

    return {
        'total': memoryStatus.dwTotalPhys, 
        'free': memoryStatus.dwAvailPhys,
        'used': memoryStatus.dwTotalPhys - memoryStatus.dwAvailPhys 
    }

def disk_usage(path):
    """\
    Get disk usage statistics about the given path.
    Returns a dict with items 'total', 'used' and 'free' as bytes.

    :param path: string
    :rtype: dict
    """

    total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong()
    ret = ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(path), None, ctypes.pointer(total), ctypes.pointer(free))
    if not ret: return None
    return { 'total': total.value, 'used': total.value - free.value, 'free': free.value }

def system_disk_usage():
    """\
    Returns the `disk_usage(...)` dict for the system drive.
    Uses the `SystemDrive` environment variable to find the system drive.

    :rtype: dict
    """

    return disk_usage(os.getenv("SystemDrive") + "\\")

def uptime():
    """\
    Return the system uptime in seconds.

    :rtype: int
    """

    ret = ctypes.windll.kernel32.GetTickCount64()
    diff = timedelta(milliseconds = ret)

    return diff.seconds

def os_release():
    """\
    Return a human-readable string of the OS release information.

    :rtype: string
    """

    windows_vers = [
        ["6.2", "Windows 8"],
        ["6.1", "Windows 7"],
        ["6.0", "Windows Vista"],
        ["5.2", "Windows Server 2003"],
        ["5.1", "Windows XP"],
        ["5.0", "Windows 2000"]
    ]

    winver = platform.win32_ver()[1]
    for ver_num, ver_str in windows_vers:
        if ver_num in winver:
            return "%s %s" % (ver_str, platform.win32_ver()[2])

    return "Unknown"

def cpu():
    """\
    Get information on the system CPU.
    Returns a dict with 'name', 'load_percentage' values.

    :rtype: dict
    """

    name = "Unknown"
    load_percentage = 0.0
    pcount = 0

    reg = get_registry_value("HKEY_LOCAL_MACHINE", "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0","ProcessorNameString")
    name =  ' '.join([s.strip() for s in reg.split()])

    c = wmi.WMI()
    for p in c.Win32_Processor():
        pcount += 1
        load_percentage += p.LoadPercentage

    load_percentage = load_percentage / pcount

    return { 'name': name, 'load_percentage': load_percentage }


def gpu():
    """\
    Get the GPU name.

    :rtype: string
    """

    try:
        reg = subprocess.check_output(["wmic", "path", "Win32_VideoController", "get", "caption"]).split("\n")[1:]
        r = []
        for x in reg:
            x = re.sub(" \(Microsoft Corporation - WDDM 1.1\)", "", x)
            x = re.sub("Microsoft Basic Render Driver", "", x)
            r.append(x)

        r = filter(bool, [s.strip() for s in r])
        return ', '.join(r)
    except:
        return "Unknown"    

def screen_resolution():
    """\
    Get the current screen resolution as a dict with 'x' and 'y' values.

    :rtype: dict
    """

    return { 'x': GetSystemMetrics(0), 'y': GetSystemMetrics(1) }

def web_browser():
    """\
    Get the default webbrowser of the system.

    :rtype: dict
    """

    try:
        name = "Unknown"
        browser = get_registry_value("HKEY_CURRENT_USER", "Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice", "Progid")
        for browser_ret, browser_str in [ ["FirefoxURL", "Mozilla Firefox"], ["ChromeHTML", "Google Chrome"] ]:
            if browser_ret in browser:
                name = browser_str
        return { 'raw': browser, 'name': name }

    except:
        return { 'raw': "Unknown", 'name': "Unknown" }


def screen_shot():
    """\
    Take a screenshot of the desktop.
    Returns True on success, False on failure.

    :rtype: bool
    """

    try:
        hwnd = win32gui.GetDesktopWindow()
 
        vscreenwidth = win32api.GetSystemMetrics(78)
        vscreenheight = win32api.GetSystemMetrics(79)
        vscreenx = win32api.GetSystemMetrics(76)
        vscreeny = win32api.GetSystemMetrics(77)

        mfcDC = win32ui.CreateDCFromHandle(win32gui.GetWindowDC(hwnd))
        saveDC = mfcDC.CreateCompatibleDC()
 
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, vscreenwidth, vscreenheight)
        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0, 0), (vscreenwidth, vscreenheight), mfcDC, (vscreenx, vscreeny), win32con.SRCCOPY)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        import Image
        im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        im.save('pyFetch-' + re.sub(":", "-", str(datetime.now())) + ".png")

        return True

    except:
        return False

def window_manager(blackbox=False, sharp=False, litestep=False, emerge=False): 
    """\
    Get current window manager.

    :rtype: dict
    """

    c = wmi.WMI ()
    for process in c.Win32_Process (name="blackbox.exe"):
        blackbox = True

    for process in c.Win32_Process (name="sharpenviro.exe"):
        sharp = True

    for process in c.Win32_Process (name="litestep.exe"):
        litestep = True

    for process in c.Win32_Process (name="emerge.exe"):
        emerge = True

    if blackbox == True:
        return{ 'name': 'bbLean' }
    elif sharp == True:
        return{ 'name': 'SharpEnviro' }
    elif litestep == True:
        return{ 'name': 'LiteStep' }
    elif emerge == True:
        return{ 'name': 'Emerge Desktop' }
    else:
        return{ 'name': 'Explorer' }




def visual_style():
    """\
    Current visual style.

    :rtype: dict
    """

    try:
        visualStyle = get_registry_value("HKEY_CURRENT_USER", "Software\Microsoft\Windows\CurrentVersion\ThemeManager", "DllName")
        visualStyle = visualStyle.split('\\')[-1].split(".")[0]
        return { 'name': visualStyle }

    except:
        try:
            visualStyle = get_registry_value("HKEY_CURRENT_USER", "Software\Microsoft\Windows\CurrentVersion\Themes", "CurrentTheme")
            visualStyle = visualStyle.split('\\')[-1].split(".")[0]
            if 'classic' in visualStyle:
                return { 'name': 'Windows Classic' }
            else:
                return { 'name': visualStyle }
        except:
            return { 'name': "Unknown"}

#def processes_running(runningProcesses=0):
#    import wmi
#    c = wmi.WMI ()
#    for process in c.Win32_Process ():
#        runningProcesses = runningProcesses+1
#    return{ 'numProcesses': runningProcesses }

def arch():
    """\
    Return platform architecture.
    
    :rtype: string
    """
    if '3' in platform.machine():
        architecture = '32bit'
    else:
        architecture = '64bit'
    return{ 'archi': architecture }

def ansi_art(windows):
    """\
    Return none due to useless on windows.

    :rtype: ret
    """

    return{ 'none': 'none' }
