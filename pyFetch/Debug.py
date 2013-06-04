import sys
from colorama import Fore, Back, Style

debugmode = False

def enable_debug():
    """\
    Enable debugging information.
    """

    global debugmode
    debugmode = True

def debug(text, force=False):
    """\
    Print the given text if debugging mode is enabled (or if force is True)
    """

    if debugmode or force:
        text = "\n".join([s.strip() for s in text.split('\n')])
        for index, line in enumerate(text.split('\n')):
            t = "!! " if index is 0 else "   "
            sys.stderr.write(Style.RESET_ALL + Fore.RED + t + Fore.RESET + line + "\n")
        sys.stderr.flush()
