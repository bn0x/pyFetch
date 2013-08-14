import pyFetch.Debug
import pyFetch.Platform
import pyFetch.Art
import pyFetch.Format

import os
import sys
import colorama
from optparse import OptionParser
from colorama import Fore, Back, Style

def draw(system, options, args):
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
    line(ascii, 'GPU Switch')