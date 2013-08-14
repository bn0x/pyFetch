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