import os
import platform
import ctypes
import subprocess
import re
import _winreg
from win32api import GetSystemMetrics
from datetime import datetime
from colorama import Fore, Back, Style

ascii_art = [
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

def get_registry_value(key, subkey, value):
    """\
    Get a value from the Windows registry.

    :param key: string
    :param subkey: string
    :param value: string
    """
    key = getattr(_winreg, key)
    handle = _winreg.OpenKey(key, subkey)
    (value, type) = _winreg.QueryValueEx(handle, value)
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

    output = subprocess.check_output(["net", "stats", "srv"])
    timestring = " ".join(output.split("\n")[3].split()[2:]).strip()
    timestring = re.sub("p.m.", "PM", timestring)
    timestring = re.sub("a.m.", "AM", timestring)
    try:
        diff = datetime.now() - datetime.strptime(timestring, "%d/%m/%Y %I:%M:%S %p")
    except ValueError:
        # yay, americans
        diff = datetime.now() - datetime.strptime(timestring, "%m/%d/%Y %I:%M:%S %p")

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
            return ver_str

    return "Unknown"

def cpu():
    """\
    Get the CPU model name.

    :rtype: string
    """

    reg = get_registry_value("HKEY_LOCAL_MACHINE", "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0","ProcessorNameString")
    return ' '.join([s.strip() for s in reg.split()])

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