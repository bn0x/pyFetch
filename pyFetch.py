import os
import pyFetch
import colorama
from optparse import OptionParser
from colorama import Fore, Back, Style

"""\
pyFetch, a Python system information tool
"""

def draw(options, args):
    """\
    Draw the system's ASCII art and output system information.
    """

    if options.bright and options.color:
        print Style.BRIGHT

    try:
        system = pyFetch.system
    except:
        print "Error: could not determine your system."
        return None

    line = pyFetch.ascii.line

    if options.art:
        ascii = pyFetch.ascii.system(options.art)
    else:
        ascii = pyFetch.ascii.system(system.default_ascii())

    disk = system.system_disk_usage()
    ram = system.ram()
    res = system.screen_resolution()
    cpu = system.cpu()
    gpu = pyFetch.format.smart_truncate(system.gpu(), 40)
    
    import getpass, socket

    line(ascii)
    line(ascii, "%sOS:      %s%s %s" % (Fore.WHITE, Fore.CYAN, system.os_release(), system.arch()['arch']))
    line(ascii, "%sName:    %s%s%s@%s%s" % (Fore.WHITE, Fore.YELLOW, getpass.getuser(), Fore.WHITE, Fore.CYAN, socket.gethostname()))
    line(ascii, "%sUptime:  %s%s" % (Fore.WHITE, Fore.CYAN, pyFetch.format.time_metric(system.uptime())))
    #line(ascii, "%sProcesses Running: %s%s" % (Fore.WHITE, Fore.CYAN, system.processes_running()['numProcesses']))
    line(ascii)
    line(ascii, "%sWM:      %s%s" % (Fore.WHITE, Fore.CYAN, system.window_manager()['name']))
    line(ascii, "%sBrowser: %s%s" % (Fore.WHITE, Fore.CYAN, system.web_browser()['name']))
    line(ascii, "%sTheme:   %s%s" % (Fore.WHITE, Fore.CYAN, system.visual_style()['name']))
    line(ascii)
    line(ascii, "%sDisk:    %s%s used %s/%s %s total" % (Fore.WHITE, Fore.YELLOW, pyFetch.format.sizeof_fmt(disk['used']), Fore.WHITE, Fore.CYAN, pyFetch.format.sizeof_fmt(disk['total'])))
    line(ascii, "%sRAM:     %s%s used %s/%s %s total" % (Fore.WHITE, Fore.YELLOW, pyFetch.format.sizeof_fmt(ram['used']), Fore.WHITE, Fore.CYAN, pyFetch.format.sizeof_fmt(ram['total'])))
    line(ascii)
    line(ascii, "%sCPU:     %s%s" % (Fore.WHITE, Fore.CYAN, cpu['name']))
    line(ascii, "%sUsage:   %s%s%s/%s100%%" % (Fore.WHITE, Fore.YELLOW, cpu['load_percentage'], Fore.WHITE, Fore.CYAN))
    line(ascii)
    line(ascii, "%sGPU:     %s%s" % (Fore.WHITE, Fore.CYAN, system.gpu()))
    line(ascii, "%sRes:     %s%s%sx%s%s" % (Fore.WHITE, Fore.YELLOW, res['x'], Fore.WHITE, Fore.YELLOW, res['y']))
    line(ascii, fill=True)
    print Style.RESET_ALL

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--color", action="store_true", dest="color", default=True, help="Make output colorful")
    parser.add_option("-C", "--no-color", action="store_false", dest="color", help="Strip color from output")
    parser.add_option("-s", "--screenshot", action="store_true", dest="screenshot", help="Take a screenshot after printing the information", default=False)
    parser.add_option("-a", "--art", action="store", dest="art", help="Select ASCII art to display (default: current OS)")
    parser.add_option("-A", "--list-art", action="store_true", dest="artlist", help="List available ASCII art images and exit", default=False)
    parser.add_option("-b", "--bright", action="store_true", dest="bright", help="Enable bright colors", default=True)
    parser.add_option("-B", "--no-bright", action="store_false", dest="bright", help="Disable bright colors")
    parser.add_option("--version", action="store_true", dest="version", help="Print version information and exit")
    (options, args) = parser.parse_args()

    colorama.init(strip=(not options.color))

    if options.version:
        print "pyFetch, a Python system information tool"
        pyFetch.buildinfo()

    elif options.artlist:
        pyFetch.ascii.list()

    else:
        draw(options, args)

        if options.screenshot:
            if pyFetch.system.screen_shot():
                print "Screenshot captured."
            else:
                print "Failed to capture screenshot."
