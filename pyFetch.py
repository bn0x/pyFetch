import os
import pyFetch
import colorama
from optparse import OptionParser
from colorama import Fore, Back, Style

"""\
pyFetch, a Python system information tool
"""

lineno = 0

def line(ascii, text = "", fill = False):
    """\
    Print a line of ASCII art followed by text. Used by the draw() function.
    If `fill` is `True`, this function will print all remaining lines of ASCII art.
    Expects ascii[0] to be a line of spaces with the same length as the rest of the lines.

    :param ascii: list
    :param text: string
    :param fill: bool
    """

    global lineno

    if fill:
        if lineno < len(ascii):
            print '\n'.join(ascii[lineno:])
    else:
        if lineno < len(ascii):
            print "%s %s" % (ascii[lineno], text)
        else:
            print "%s %s" % (ascii[0], text)

    lineno += 1

def draw():
    """\
    Draw the system's ASCII art and output system information.
    """

    system = pyFetch.system

    ascii = system.ascii_art
    disk = system.system_disk_usage()
    ram = system.ram()
    res = system.screen_resolution()
    cpu = system.cpu()
    
    import getpass, socket

    line(ascii)
    line(ascii, "%sOS:      %s%s" % (Fore.WHITE, Fore.CYAN, system.os_release()))
    line(ascii, "%sName:    %s%s%s@%s%s" % (Fore.WHITE, Fore.YELLOW, getpass.getuser(), Fore.WHITE, Fore.CYAN, socket.gethostname()))
    line(ascii, "%sUptime:  %s%s" % (Fore.WHITE, Fore.CYAN, pyFetch.format.time_metric(system.uptime())))
    line(ascii)
    line(ascii, "%sWM:      %s%s" % (Fore.WHITE, Fore.CYAN, system.window_manager()['name']))
    line(ascii, "%sBrowser: %s%s" % (Fore.WHITE, Fore.CYAN, system.web_browser()['name']))
    line(ascii, "%sTheme:   %s%s" % (Fore.WHITE, Fore.CYAN, system.visual_style()['name']))
    line(ascii)
    line(ascii, "%sDisk:    %s%s free %s/%s %s total" % (Fore.WHITE, Fore.YELLOW, pyFetch.format.sizeof_fmt(disk['free']), Fore.WHITE, Fore.CYAN, pyFetch.format.sizeof_fmt(disk['total'])))
    line(ascii, "%sRAM:     %s%s free %s/%s %s total" % (Fore.WHITE, Fore.YELLOW, pyFetch.format.sizeof_fmt(ram['free']), Fore.WHITE, Fore.CYAN, pyFetch.format.sizeof_fmt(ram['total'])))
    line(ascii)
    line(ascii, "%sCPU:     %s%s" % (Fore.WHITE, Fore.CYAN, cpu['name']))
    line(ascii, "%sUsage:   %s%s%%" % (Fore.WHITE, Fore.CYAN, cpu['load_percentage']))
    line(ascii)
    line(ascii, "%s GPU:     %s%s" % (Fore.WHITE, Fore.CYAN, system.gpu()))
    line(ascii, "%sRes:     %s%s%sx%s%s" % (Fore.WHITE, Fore.CYAN, res['x'], Fore.WHITE, Fore.CYAN, res['y']))
    line(ascii, fill=True)
    print Style.RESET_ALL

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--color", action="store_false", dest="color", default=True, help="Make output colorful")
    parser.add_option("-n", "--no-color", action="store_true", dest="color", help="Strip color from output")
    parser.add_option("-s", "--screenshot", action="store_true", dest="screenshot", help="Take a screenshot after printing the information", default=False)
    (options, args) = parser.parse_args()

    colorama.init(strip=options.color)
    draw()

    if options.screenshot:
        if pyFetch.system.screen_shot():
            print "Screenshot captured."
        else:
            print "Failed to capture screenshot."
