import os
import sys
import colorama
from optparse import OptionParser
from colorama import Fore, Back, Style

import pyFetch.Debug
import pyFetch.Platform
import pyFetch.Art
import pyFetch.Format
from pyFetch.Info import *

"""\
pyFetch, a Python system information tool
"""

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
    
    parser.add_option('-g', '--gpu', action='store_true', dest='gpu', help='GPU Information.')

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
        
        if options.gpu:
            mode = gpu
        else:
            mode = normal

        draw(system, options, args, mode)

        if options.screenshot:
            if system.screen_shot():
                print "Screenshot captured."
            else:
                print "Failed to capture screenshot."
