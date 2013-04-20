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

import PlatformBase

class Windows(PlatformBase.PlatformBase):
    """\
    Windows platform class.
    """

    def default_ascii(self):
        """\
        Return the name of the default ASCII art for this platform.

        :rtype: string
        """

        if float(platform.win32_ver()[1][:3]) > 6.1:
            return "windows_8"
        else:
            return "windows"

    def get_registry_value(self, key, subkey, value):
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

    def ram(self):
        """\
        Get RAM statistics.
        Returns a dict with items 'total', 'used' and 'free' as bytes.

        :rtype: dict
        """

        memoryStatus = self.MEMORYSTATUS()
        memoryStatus.dwLength = ctypes.sizeof(self.MEMORYSTATUS)
        ret = ctypes.windll.kernel32.GlobalMemoryStatus(ctypes.byref(memoryStatus))

        return {
            'total': memoryStatus.dwTotalPhys, 
            'free': memoryStatus.dwAvailPhys,
            'used': memoryStatus.dwTotalPhys - memoryStatus.dwAvailPhys 
        }

    def disk_usage(self, path):
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

    def system_disk_usage(self):
        """\
        Returns the `disk_usage(...)` dict for the system drive.
        Uses the `SystemDrive` environment variable to find the system drive.

        :rtype: dict
        """

        return self.disk_usage(os.getenv("SystemDrive") + "\\")

    def uptime(self):
        """\
        Return the system uptime in seconds.

        :rtype: int
        """

        ret = ctypes.windll.kernel32.GetTickCount64()
        diff = timedelta(milliseconds = ret)

        return diff.seconds

    def os_release(self):
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

    def cpu(self):
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


    def gpu(self):
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
                if not x in r:
                    r.append(x)

            r = filter(bool, [s.strip() for s in r])
            return ', '.join(r)
        except:
            return "Unknown"    

    def screen_resolution(self):
        """\
        Get the current screen resolution as a dict with 'x' and 'y' values.

        :rtype: dict
        """

        return { 'x': GetSystemMetrics(0), 'y': GetSystemMetrics(1) }

    def web_browser(self):
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


    def screen_shot(self):
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

    def window_manager(self): 
        """\
        Get current window manager.

        :rtype: dict
        """

        wms = [
            ["blackbox.exe", "bbLean"],
            ["sharpenviro.exe", "SharpEnviro"],
            ["litestep.exe", "LiteStep"],
            ["emergecore.exe", "Emerge Desktop"],
        ]

        name = ""

        c = wmi.WMI ()
        for process in c.Win32_Process:
            for wm_str, wm_name in wms:
                if wm_str in process.Caption:
                    return { 'name': wm_name }

        return { 'name': 'Explorer' }

    def visual_style(self):
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

    def arch(self):
        """\
        Return platform architecture.
    
        :rtype: dict
        """

        return { 'arch': platform.machine() }

