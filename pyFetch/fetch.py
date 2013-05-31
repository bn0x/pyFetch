import os
import pyFetch
import colorama
import platform
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

    system = pyFetch.system()
    line = pyFetch.ascii.line

    if options.maxwidth:
        pyFetch.ascii.setMaxWidth(options.maxwidth)

    if options.forcedistro:
        system.force_distro(options.forcedistro)

    if options.art:
        ascii = pyFetch.ascii.system(options.art)
    else:
        ascii = pyFetch.ascii.system(system.default_ascii())

    disk = system.system_disk_usage()
    ram = system.ram()
    res = system.screen_resolution()
    cpu = system.cpu()
    gpu = system.gpu()
    osobj = system.os_release()
    osstr = "%s %s %s" % (osobj['name'], osobj['ver'], osobj['codename'])
    osstr = " ".join([s.strip() for s in osstr.split()])

    import getpass, socket

    line(ascii)
    line(ascii, "%sOS:      %s%s %s" % (ascii.highlight, ascii.text, osstr, system.arch()['arch']))
    if system.show_kernel:
        line(ascii, "%sKernel:  %s%s" % (ascii.highlight, ascii.text, system.kernel()))
    line(ascii, "%sName:    %s%s%s@%s%s" % (ascii.highlight, ascii.plustext, getpass.getuser(), ascii.highlight, ascii.text, socket.gethostname()))
    line(ascii, "%sUptime:  %s%s" % (ascii.highlight, ascii.text, pyFetch.format.time_metric(system.uptime())))
    line(ascii)
    if system.__class__.__name__ == "Windows":
        line(ascii, "%sShell:   %s%s" % (ascii.highlight, ascii.text, system.window_manager()['name']))
    elif system.__class__.__name__ != "MacOSX":
        line(ascii, "%sWM:      %s%s" % (ascii.highlight, ascii.text, system.window_manager()['name']))
    line(ascii, "%sBrowser: %s%s" % (ascii.highlight, ascii.text, system.web_browser()['name']))
    line(ascii, "%sTheme:   %s%s" % (ascii.highlight, ascii.text, system.visual_style()['name']))
    line(ascii)
    if options.free:
        fmtDisk = "%sDisk:    %s%s free %s/%s %s total" % (ascii.highlight, ascii.plustext, pyFetch.format.sizeof_fmt(disk['free']), ascii.highlight, ascii.text, pyFetch.format.sizeof_fmt(disk['total']))
        fmtRAM  = "%sRAM:     %s%s free %s/%s %s total" % (ascii.highlight, ascii.plustext, pyFetch.format.sizeof_fmt(ram['free']), ascii.highlight, ascii.text, pyFetch.format.sizeof_fmt(ram['total']))
    else:
        fmtDisk = "%sDisk:    %s%s used %s/%s %s total" % (ascii.highlight, ascii.plustext, pyFetch.format.sizeof_fmt(disk['used']), ascii.highlight, ascii.text, pyFetch.format.sizeof_fmt(disk['total']))
        fmtRAM  = "%sRAM:     %s%s used %s/%s %s total" % (ascii.highlight, ascii.plustext, pyFetch.format.sizeof_fmt(ram['used']), ascii.highlight, ascii.text, pyFetch.format.sizeof_fmt(ram['total']))

    line(ascii, fmtDisk)
    line(ascii, fmtRAM)
    line(ascii)
    line(ascii, "%sCPU:     %s%s" % (ascii.highlight, ascii.text, cpu['name']))
    line(ascii, "%sUsage:   %s%s%s/%s100%%" % (ascii.highlight, ascii.plustext, cpu['load_percentage'], ascii.highlight, ascii.text))
    line(ascii)
    line(ascii, "%sGPU:     %s%s" % (ascii.highlight, ascii.text, gpu))
    line(ascii, "%sRes:     %s%s%sx%s%s%s" % (ascii.highlight, ascii.plustext, res['x'], ascii.highlight, ascii.plustext, res['y'], Fore.RESET))
    line(ascii, fill=True)
    print Style.RESET_ALL

def run():
    parser = OptionParser()
    parser.add_option("-c", "--color", action="store_true", dest="color", default=True, help="Make output colorful")
    parser.add_option("-C", "--no-color", action="store_false", dest="color", help="Strip color from output")

    parser.add_option("-s", "--screenshot", action="store_true", dest="screenshot", help="Take a screenshot after printing the information", default=False)
    parser.add_option("-f", "--free", action="store_true", dest="free", help="Show amount of free RAM/disk instead of used")
    parser.add_option("-w", "--maxwidth", action="store", dest="maxwidth", type=int, help="Set the maximum number of characters per line")

    parser.add_option("-a", "--art", action="store", dest="art", help="Select ASCII art to display. Uses the art for your OS by default. Use \"default\" to disable ASCII art display.")
    parser.add_option("-A", "--list-art", action="store_true", dest="artlist", help="List available ASCII art images and exit", default=False)

    parser.add_option("-b", "--bright", action="store_true", dest="bright", help="Enable bright colors", default=True)
    parser.add_option("-B", "--no-bright", action="store_false", dest="bright", help="Disable bright colors")

    parser.add_option("-d", "--distro", action="store", dest="forcedistro", metavar="DISTRO", help="Ignore system distribution information and use DISTRO instead (Linux only)")

    parser.add_option("--version", action="store_true", dest="version", help="Print version information and exit")
    (options, args) = parser.parse_args()

    colorama.init(strip=(not options.color))

    if options.version:
        print "pyFetch, a Python system information tool"
        print "version %s" % pyFetch.version
        print ""

    elif options.artlist:
        pyFetch.ascii.list()

    else:
        draw(options, args)

        if options.screenshot:
            if pyFetch.system().screen_shot():
                print "Screenshot captured."
            else:
                print "Failed to capture screenshot."
