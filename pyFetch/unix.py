import os
import re
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
    Fore.RED  +"#    # ##    # ###### #    # ",
    Fore.RED  +"#    # # #   #   ##    #  #  ",
    Fore.RED  +"#    # #  #  #   ##     ##   ",
    Fore.RED  +"#    # #   # #   ##    #  #  ",
    Fore.RED  +"###### #    ## ###### #    # ",
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
    Get the CPU model name.

    :rtype: string
    """

    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if 'model name' in line:
                return ' '.join([s.strip() for s in line.split(":")[1].strip().split()])

    return "Unknown"

def gpu():
    """\
    Get the GPU name.

    :rtype: string
    """

    return "Unknown"    

def screen_resolution():
    """\
    Get the current screen resolution as a dict with 'x' and 'y' values.

    :rtype: dict
    """

    return { 'x': 0, 'y': 0 }
