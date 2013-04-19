import platform
import format
import ascii
import buildinfo

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
        with open(os.path.join(os.path.dirname(__file__), "buildinfo"), 'r') as f:
            print f
    except:
        pass