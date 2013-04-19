import platform
import format
import ascii

if platform.system() == "Windows":
    import win32 as system
elif platform.system() == "Linux":
    import unix as system

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