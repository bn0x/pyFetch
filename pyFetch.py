import os
import pyFetch
import colorama
from colorama import Fore, Back, Style

"""\
pyFetch, a Python system information tool
"""

def draw():
    """\
    Draw the system's ASCII art and output system information.
    """
    system = pyFetch.system

    ascii = system.ascii_art
    disk = system.system_disk_usage()
    ram = system.ram()
    res = system.screen_resolution()

    print ascii[0]
    print "%s %sOS:     %s%s" % (ascii[1], Fore.WHITE, Fore.CYAN, system.os_release())
    print "%s %sName:   %s%s%s@%s%s" % (ascii[2], Fore.WHITE, Fore.YELLOW, __import__('getpass').getuser(), Fore.WHITE, Fore.CYAN, __import__('socket').gethostname())
    print "%s %sUptime: %s%s" % (ascii[3], Fore.WHITE, Fore.CYAN, pyFetch.format.time_metric(system.uptime()))
    print ascii[4]
    print "%s %sDisk:   %s%s%s/%s%s" % (ascii[5], Fore.WHITE, Fore.YELLOW, pyFetch.format.sizeof_fmt(disk['free']), Fore.WHITE, Fore.CYAN, pyFetch.format.sizeof_fmt(disk['total']))
    print "%s %sRAM:    %s%s%s/%s%s" % (ascii[5], Fore.WHITE, Fore.YELLOW, pyFetch.format.sizeof_fmt(ram['free']), Fore.WHITE, Fore.CYAN, pyFetch.format.sizeof_fmt(ram['total']))
    print "%s %sCPU:    %s%s" % (ascii[7], Fore.WHITE, Fore.CYAN, system.cpu())
    print ascii[8]
    print "%s %sGPU:    %s%s" % (ascii[9], Fore.WHITE, Fore.CYAN, system.gpu())
    print "%s %sRes:    %s%s%sx%s%s" % (ascii[10], Fore.WHITE, Fore.CYAN, res['x'], Fore.WHITE, Fore.CYAN, res['y'])
    
    print '\n'.join(ascii[9:])
    print Style.RESET_ALL

if __name__ == "__main__":
    colorama.init()
    draw()
