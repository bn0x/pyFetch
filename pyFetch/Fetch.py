import os
import sys
import colorama
from optparse import OptionParser
from colorama import Fore, Back, Style

import pyFetch.Debug
import pyFetch.Platform
import pyFetch.Art
import pyFetch.Format


"""\
pyFetch, a Python system information tool
"""

def draw(system, options, args):
    """\
    Draw the system's ASCII art and output system information.
    """

    line = pyFetch.Art.line
    data = system.collate_data()

    if options.bright and options.color:
        sys.stdout.write(Style.BRIGHT)
        sys.stdout.flush()

    if options.art:
        ascii = pyFetch.Art.system(options.art)
    else:
        ascii = pyFetch.Art.system(data['default_ascii'])

    pyFetch.Debug.debug("ASCII art: %s" % ascii.__name__)    

    import getpass, socket

    line(ascii)
    osstr = " ".join([s.strip() for s in ("%s %s %s" % (data['os_release']['name'] if data['os_release'] else "Unknown", data['os_release']['ver'] if data['os_release'] else "Unknown", data['os_release']['codename'] if data['os_release'] else "Unknown")).split()])
    line(ascii, "%sOS:      %s%s %s" % (ascii.highlight, ascii.text, osstr, data['arch']['arch'] if data['arch'] else "Unknown"))
    if system.show_kernel:
        line(ascii, "%sKernel:  %s%s" % (ascii.highlight, ascii.text, data['kernel'] if data['kernel'] else "Unknown"))
    line(ascii, "%sName:    %s%s%s@%s%s" % (ascii.highlight, ascii.plustext, data['username'] if data['username'] else "Unknown", ascii.highlight, ascii.text, data['hostname'] if data['hostname'] else "Unknown"))
    line(ascii, "%sUptime:  %s%s" % (ascii.highlight, ascii.text, pyFetch.Format.time_metric(data['uptime']) if data['uptime'] else "Unknown"))
    line(ascii)

    if system.__class__.__name__ == "Windows":
        line(ascii, "%sShell:   %s%s" % (ascii.highlight, ascii.text, data['window_manager']['name'] if data['window_manager'] else "Unknown"))
    elif system.__class__.__name__ != "MacOSX":
        line(ascii, "%sWM:      %s%s" % (ascii.highlight, ascii.text, data['window_manager']['name'] if data['window_manager'] else "Unknown"))

    line(ascii, "%sBrowser: %s%s" % (ascii.highlight, ascii.text, data['web_browser']['name'] if data['web_browser'] else "Unknown"))
    line(ascii, "%sTheme:   %s%s" % (ascii.highlight, ascii.text, data['visual_style']['name'] if data['visual_style'] else "Unknown"))
    line(ascii)

    if options.free:
        fmtDisk = "%sDisk:    %s%s free %s/%s %s total" % (ascii.highlight, ascii.plustext, pyFetch.Format.sizeof_fmt(data['system_disk_usage']['free']) if data['system_disk_usage'] else "Unknown", ascii.highlight, ascii.text, pyFetch.Format.sizeof_fmt(data['system_disk_usage']['total']) if data['system_disk_usage'] else "Unknown")
        fmtRAM  = "%sRAM:     %s%s free %s/%s %s total" % (ascii.highlight, ascii.plustext, pyFetch.Format.sizeof_fmt(data['ram']['free']) if data['ram'] else "Unknown", ascii.highlight, ascii.text, pyFetch.Format.sizeof_fmt(data['ram']['total']) if data['ram'] else "Unknown")
    else:
        fmtDisk = "%sDisk:    %s%s used %s/%s %s total" % (ascii.highlight, ascii.plustext, pyFetch.Format.sizeof_fmt(data['system_disk_usage']['used']) if data['system_disk_usage'] else "Unknown", ascii.highlight, ascii.text, pyFetch.Format.sizeof_fmt(data['system_disk_usage']['total']) if data['system_disk_usage'] else "Unknown")
        fmtRAM  = "%sRAM:     %s%s used %s/%s %s total" % (ascii.highlight, ascii.plustext, pyFetch.Format.sizeof_fmt(data['ram']['used']) if data['ram'] else "Unknown", ascii.highlight, ascii.text, pyFetch.Format.sizeof_fmt(data['ram']['total']) if data['ram'] else "Unknown")

    line(ascii, fmtDisk)
    line(ascii, fmtRAM)
    line(ascii)
    line(ascii, "%sCPU:     %s%s" % (ascii.highlight, ascii.text, data['cpu']['name'] if data['cpu'] else "Unknown"))
    line(ascii, "%sUsage:   %s%s%s/%s100%%" % (ascii.highlight, ascii.plustext, data['cpu']['load_percentage'] if data['cpu'] else "Unknown", ascii.highlight, ascii.text))
    line(ascii)
    line(ascii, "%sGPU:     %s%s" % (ascii.highlight, ascii.text, data['gpu'] if data['gpu'] else "Unknown"))
    line(ascii, "%sRes:     %s%s%sx%s%s%s" % (ascii.highlight, ascii.plustext, data['screen_resolution']['x'] if data['screen_resolution'] else "Unknown", ascii.highlight, ascii.plustext, data['screen_resolution']['y'] if data['screen_resolution'] else "Unknown", Fore.RESET))
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

    parser.add_option("-d", "--distro", action="store", dest="forcedistro", metavar="DISTRO", help="Ignore system distribution information and use DISTRO instead. On Linux, selects distro; on Darwin and Mac OS X, switches between vanilla Darwin (\"Darwin\") and OS X (\"MacOSX\")")
    parser.add_option("-p", "--platform", action="store", dest="forceplatform", metavar="PLATFORM", help="Ignore system platform information and use the PLATFORM platform class instead", default=False)
    
    parser.add_option("--debug", action="store_true", dest="debugmode", help="Enable debugging mode.")
    parser.add_option("--version", action="store_true", dest="version", help="Print version information and exit")

    (options, args) = parser.parse_args()

    if options.debugmode:
        pyFetch.Debug.enable_debug()
        pyFetch.Debug.debug("Welcome to pyFetch.")

    pyFetch.Debug.debug("Color strip mode: %s" % str(not options.color))
    colorama.init(strip=(not options.color))

    if options.version:
        print "pyFetch, a Python system information tool"
        print "version %s" % pyFetch.version
        print ""

    elif options.artlist:
        pyFetch.Debug.debug("Printing ASCII art list.")
        pyFetch.Art.list()

    else:
        system = pyFetch.Platform.guess_platform(options.forceplatform)()
        pyFetch.Debug.debug("System: %s" % system.__class__.__name__)
        pyFetch.Debug.debug(system.__class__.__doc__)

        if options.maxwidth:
            pyFetch.Debug.debug("Maximum width set to %d." % options.maxwidth)
            pyFetch.Art.setMaxWidth(options.maxwidth)

        if options.forcedistro:
            if system.__class__.__name__ == "Linux":
                pyFetch.Debug.debug("Setting distro force flag to \"%s\"." % options.forcedistro)
                system.force_distro(options.forcedistro)
            elif system.__class__.__name__ == "Darwin" or system.__class__.__name__ == "MacOSX":
                system = pyFetch.Platform.guess_platform("Darwin", options.forcedistro)()
            else:
                pyFetch.Debug.debug("Ignoring distro force flag, we're not on Linux or Darwin", force=True)

        pyFetch.Debug.debug("Calling pyFetch.fetch.draw()...")
        draw(system, options, args)

        if options.screenshot:
            if system.screen_shot():
                print "Screenshot captured."
            else:
                print "Failed to capture screenshot."
