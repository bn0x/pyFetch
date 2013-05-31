###### ASCII ART FILE IMPORTS ######

""" A lot of ASCII from @KittyKatt aka screenFetch """

import default
import unix_placeholder
import windows_8
import windows
import arch_big
import swastika
import swastika_no_unicode
import ubuntu
import gentoo
import macosx
import apple

######/ASCII ART FILE IMPORTS  ######

modules = []
for x in dir():
    if x[0] == "_" or x == "line" or x == "system" or x == "list" or x == "modules":
        continue

    modules.append(x)

lineno = 0
maxwidth = 0

def setMaxWidth(width):
    """\
    Set the maximum terminal width. All text drawn by `line()` will be truncated
    at this length.

    Defaults to 0, meaning no truncation will be performed.

    :param width: int
    """

    assert isinstance(width, int), "Maximum width should be an integer"
    global maxwidth
    maxwidth = width

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

    class Mark:
        pass

    mark = Mark()
    mark.skip = mark.len = 0
    mark.out = mark.input = ""

    if not ascii:
        mark.input = text
        return None
    elif fill:
        if lineno < len(ascii.ascii_art):
            print '\n'.join(ascii.ascii_art[lineno:])
            return None
    else:
        if lineno < len(ascii.ascii_art):
            mark.input = "%s %s" % (ascii.ascii_art[lineno], text)
        else:
            mark.input = "%s %s" % (ascii.ascii_art[0], text)

    if maxwidth == 0:
        print mark.input
        lineno += 1
        return None

    for character in mark.input:
        if character == "\x1b":
            # start of color character
            mark.skip += 4
        elif mark.skip != 0:
            mark.skip -= 1
        else:
            mark.len += 1
        
        mark.out += character

        if mark.len == maxwidth:
            print mark.out
            lineno += 1
            return None

    print mark.out
    lineno += 1

def system(sys):
    """\
    Get the ASCII art for the given system.

    :param sys: string
    :rtype: list
    """

    if sys in modules:
        return eval("%s" % sys)
    else:
        print "WARNING: selected ASCII art not found, returning the default one"
        return default

def list():
    """\
    Print all available ASCII art images to the screen.

    :rtype: None
    """

    global lineno
    from colorama import Fore, Back, Style

    for module in modules:
        lineno = 0
        b = system(module)
        print
        print "%s%s" % (Fore.WHITE, '-' * 80)
        print "%s %s" % (Fore.WHITE, module)
        line(b, fill=True)
        print Style.RESET_ALL
