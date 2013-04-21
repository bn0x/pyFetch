import os
import re
import subprocess
import platform
import sys
from colorama import Fore, Back, Style
import PlatformBase

class Unix(PlatformBase.PlatformBase):

    def default_ascii(self):
        """\
        Return the name of the default ASCII art for this platform.

        :rtype: string
        """

        return "unix_placeholder"

    def disk_usage(self, path):
        """\
        Get disk usage statistics about the given path.
        Returns a dict with items 'total', 'used' and 'free' as bytes.

        :param path: string
        :rtype: dict
        """

        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return { 'total': total, 'used': used, 'free': free }

    def system_disk_usage(self):
        """\
        Returns the `disk_usage(...)` dict for the root filesystem.

        :rtype: dict
        """

        return self.disk_usage("/")

    def ram(self):
        """\
        Get RAM statistics.
        Returns a dict with items 'total', 'used' and 'free' as bytes.

        :rtype: dict
        """

        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if 'MemTotal' in line:
                    total = float(line.strip().split()[-2]) * 1024
                elif 'MemFree' in line:
                    free = float(line.strip().split()[-2]) * 1024

        return {
            'total': total,
            'used': total - free,
            'free': free
        }

    def uptime(self):
        """\
        Return the system uptime in seconds.

        :rtype: int
        """

        with open('/proc/uptime', 'r') as f:
            return float(f.readline().split()[0])

    def os_release(self):
        """\
        Return a human-readable string of the OS release information.

        :rtype: string
        """

        try:
            output = subprocess.check_output(["uname", "-sr"])
            return { 'name': output.strip(), 'ver': '', 'codename': '' }
        except:
            return { 'name': "Unknown", 'ver': '', 'codename': '' }

    def cpu(self):
        """\
        Get information on the system CPU.
        Returns a dict with 'name', 'load_percentage' values.

        :rtype: dict
        """

        name = "Unknown"
        load_percentage = 0.0

        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if 'model name' in line:
                    name = ' '.join([s.strip() for s in line.split(":")[1].strip().split()])

        try:
            output = subprocess.check_output(["top", "-bn1"], stderr=subprocess.STDOUT).split("\n")
            for x in output:
                if '%Cpu(s)' in x:
                    y = x.split(",")
                    for z in y:
                        if 'id' in z:
                            z = re.sub("id", "", z)
                            load_percentage = 100 - float(z.strip())
        except:
            pass

        return { 'name': name, 'load_percentage': load_percentage }
    
    def gpu(self):
        """\
        Get the GPU name.

        :rtype: string
        """

        try:
            output = subprocess.check_output(["lspci"], stderr=subprocess.STDOUT).split("\n")
            for x in output:
                if 'VGA' in x:
                    x = x.split(":")[2].strip()
                    return x

            return "Unknown"    

        except:
            return "Unknown"    

    def screen_resolution(self):
        """\
        Get the current screen resolution as a dict with 'x' and 'y' values.

        :rtype: dict
        """

        try:
            output = subprocess.check_output(["xrandr"], stderr=subprocess.STDOUT).split("\n")
            for x in output:
                if 'connected' in x:
                    x = x.split()[2].split("+")[0].split("x")
                    return { 'x': x[0], 'y': x[1] }

            return { 'x': 0, 'y': 0 }

        except:
            return { 'x': 0, 'y': 0 }

    def screen_shot(self):
        """\
        Take a screenshot of the desktop.
        Returns True on success, False on failure.

        :rtype: bool
        """

        try:
            if subprocess.call(["scrot"]) == 0:
                return True
            return False

        except:
            return False

    def arch(self):
        """\
        Return platform architecture.
    
        :rtype: dict
        """

        try:
            arch = subprocess.check_output(["uname", "-m"]).strip()
            return { 'arch': arch }

        except:
            return { 'arch': "unknown" }

