import os
import re
import subprocess
from colorama import Fore, Back, Style

ascii_art = [
                "                             ",
    Fore.RED  + "##        ########  ##       ",
    Fore.RED  + "##        ##    ##  ##       ",
    Fore.RED  + "##        ##    ##  ##       ",
    Fore.RED  + "##        ##    ##  ##       ",
    Fore.RED  + "##        ##    ##  ##       ",
    Fore.RED  + "########  ########  ######## ",
    Fore.CYAN + "                             ",
    Fore.CYAN + "  (i don't have real ascii   ",
    Fore.CYAN + " art for your system, sorry) ",
    Fore.CYAN + "                             ",
    Fore.RED  + "#    # ##    # ###### #    # ",
    Fore.RED  + "#    # # #   #   ##    #  #  ",
    Fore.RED  + "#    # #  #  #   ##     ##   ",
    Fore.RED  + "#    # #   # #   ##    #  #  ",
    Fore.RED  + "###### #    ## ###### #    # ",
]

def disk_usage(path):
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

def system_disk_usage():
    """\
    Returns the `disk_usage(...)` dict for the root filesystem.

    :rtype: dict
    """

    return disk_usage("/")

def ram():
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

def uptime():
    """\
    Return the system uptime in seconds.

    :rtype: int
    """

    with open('/proc/uptime', 'r') as f:
        return float(f.readline().split()[0])

def os_release():
    """\
    Return a human-readable string of the OS release information.

    :rtype: string
    """

    try:
        output = subprocess.check_output(["uname", "-sr"])
        return output.strip()
    except:
        return "Unknown"

def cpu():
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
    
def gpu():
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

def screen_resolution():
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

def web_browser():
    """\
    Get the default webbrowser of the system.

    :rtype: dict
    """

    return { 'raw': "Unknown", 'name': "Unknown" }

def screen_shot():
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

def window_manager(): 
    """\
    Get current window manager.

    :rtype: dict
    """

    return { 'raw': "Unknown", 'name': "Unknown" }

def visual_style():
    """\
    Current visual style.

    :rtype: dict
    """
    
    return { 'name': "Unknown"}
