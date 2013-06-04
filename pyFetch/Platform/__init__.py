import re
import sys
import pyFetch.Debug

def guess_platform(platform=False, flag=None):
    """\
    Try to find the Platform of the system that this script is currently
    running on. On failure, print a message to stderr and call sys.exit().
    """

    if not platform:
        platform = __import__('platform').system()

    if platform == "Windows":
        pyFetch.Debug.debug("Windows found.")
        import pyFetch.Platform.Windows as Windows
        return Windows.Windows
    elif platform == "Linux":
        pyFetch.Debug.debug("Linux found.")
        import pyFetch.Platform.Linux as Linux
        return Linux.Linux
    elif platform == "Darwin":
        import pyFetch.Platform.Darwin as Darwin
        import pyFetch.Platform.MacOSX as MacOSX

        if flag == "Darwin":
            pyFetch.Debug.debug("Force flag has been set to Darwin, so returning the Darwin class")
            return Darwin.Darwin

        pyFetch.Debug.debug("Darwin found, checking for Mac OS X...")
        osx = False

        try:
            with open('/System/Library/CoreServices/SystemVersion.plist', 'r') as f:
                for line in f:
                    if re.search('Mac OS X', line):
                        osx = True
                        pyFetch.Debug.debug("Found Mac OS X.")
                        break
        except:
            tt = "assuming Darwin" if osx == False else "but OS X flag already set, so going with that"
            pyFetch.Debug.debug("Exception occurred checking for Mac OS X, %s" % tt)
            pass

        if osx or flag == "MacOSX":
            return MacOSX.MacOSX
        else:
            return Darwin.Darwin
    else:
        pyFetch.Debug.debug("Could not find platform, platform.system() is %s" % platform)

        text = """Unfortunately, your system is not currently supported.
        If you would like to help add support for your system, please
        file an issue at https://github.com/bn0x/pyFetch/issues/."""
        pyFetch.Debug.debug(text, force=True)
        sys.exit(1)
