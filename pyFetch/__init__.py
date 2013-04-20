import platform
import format
import ascii

import PlatformBase

if platform.system() == "Windows":
    import Windows
    system = Windows.Windows
elif platform.system() == "Linux":
    import Linux
    system = Linux.Linux
else:
    print "Your system is not supported."
    system = PlatformBase.PlatformBase

def buildinfo():
    """\
    Read the build information and display it, if it exists.

    :rtype: None
    """

    try:
        from win32api import LoadResource
        from StringIO import StringIO
        print StringIO(LoadResource(0, u'buildinfo', 1))
    except:
        pass
