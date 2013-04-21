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
        system = pyFetch.system()
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
    line(ascii, "%sOS:      %s%s %s" % (Fore.RED, Fore.WHITE, system.os_release()['name'], system.arch()['arch']))
    if system.show_kernel:
        line(ascii, "%sKernel:  %s%s" % (Fore.RED, Fore.WHITE, system.kernel()))
    line(ascii, "%sName:    %s%s%s@%s%s" % (Fore.RED, Fore.GREEN, getpass.getuser(), Fore.RED, Fore.WHITE, socket.gethostname()))
    line(ascii, "%sUptime:  %s%s" % (Fore.RED, Fore.WHITE, pyFetch.format.time_metric(system.uptime())))
    #line(ascii, "%sProcesses Running: %s%s" % (Fore.WHITE, Fore.WHITE, system.processes_running()['numProcesses']))
    line(ascii)
    line(ascii, "%sWM:      %s%s" % (Fore.RED, Fore.WHITE, system.window_manager()['name']))
    line(ascii, "%sBrowser: %s%s" % (Fore.RED, Fore.WHITE, system.web_browser()['name']))
    line(ascii, "%sTheme:   %s%s" % (Fore.RED, Fore.WHITE, system.visual_style()['name']))
    line(ascii)
    if options.free:
        fmtDisk = "%sDisk:    %s%s free %s/%s %s total" % (Fore.RED, Fore.GREEN, pyFetch.format.sizeof_fmt(disk['free']), Fore.RED, Fore.WHITE, pyFetch.format.sizeof_fmt(disk['total']))
        fmtRAM  = "%sRAM:     %s%s free %s/%s %s total" % (Fore.RED, Fore.GREEN, pyFetch.format.sizeof_fmt(ram['free']), Fore.RED, Fore.WHITE, pyFetch.format.sizeof_fmt(ram['total']))
    else:
        fmtDisk = "%sDisk:    %s%s used %s/%s %s total" % (Fore.RED, Fore.GREEN, pyFetch.format.sizeof_fmt(disk['used']), Fore.RED, Fore.WHITE, pyFetch.format.sizeof_fmt(disk['total']))
        fmtRAM  = "%sRAM:     %s%s used %s/%s %s total" % (Fore.RED, Fore.GREEN, pyFetch.format.sizeof_fmt(ram['used']), Fore.RED, Fore.WHITE, pyFetch.format.sizeof_fmt(ram['total']))

    line(ascii, fmtDisk)
    line(ascii, fmtRAM)
    line(ascii)
    line(ascii, "%sCPU:     %s%s" % (Fore.RED, Fore.WHITE, cpu['name']))
    line(ascii, "%sUsage:   %s%s%s/%s100%%" % (Fore.RED, Fore.GREEN, cpu['load_percentage'], Fore.RED, Fore.WHITE))
    line(ascii)
    line(ascii, "%sGPU:     %s%s" % (Fore.RED, Fore.WHITE, gpu))
    line(ascii, "%sRes:     %s%s%sx%s%s%s" % (Fore.RED, Fore.GREEN, res['x'], Fore.RED, Fore.GREEN, res['y'], Fore.RESET))
    line(ascii, fill=True)
    print Style.RESET_ALL

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--color", action="store_true", dest="color", default=True, help="Make output colorful")
    parser.add_option("-C", "--no-color", action="store_false", dest="color", help="Strip color from output")
    parser.add_option("-s", "--screenshot", action="store_true", dest="screenshot", help="Take a screenshot after printing the information", default=False)
    parser.add_option("-a", "--art", action="store", dest="art", help="Select ASCII art to display. Uses the art for your OS by default. Use \"none\" to disable ASCII art display.")
    parser.add_option("-A", "--list-art", action="store_true", dest="artlist", help="List available ASCII art images and exit", default=False)
    parser.add_option("-b", "--bright", action="store_true", dest="bright", help="Enable bright colors", default=True)
    parser.add_option("-B", "--no-bright", action="store_false", dest="bright", help="Disable bright colors")
    parser.add_option("-f", "--free", action="store_true", dest="free", help="Show amount of free RAM/disk instead of used")
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
            if pyFetch.system().screen_shot():
                print "Screenshot captured."
            else:
                print "Failed to capture screenshot."
