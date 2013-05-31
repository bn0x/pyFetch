import platform
import format
import ascii
import re

import PlatformBase

version = "0.1.2"

if platform.system() == "Windows":
    import Windows
    system = Windows.Windows
elif platform.system() == "Linux":
    import Linux
    system = Linux.Linux
elif platform.system() == "Darwin":
    osx = False

    try:
        with open('/System/Library/CoreServices/SystemVersion.plist', 'r') as f:
            for line in f:
                if re.search('Mac OS X', line): osx = True
    except:
        pass

    if osx:
        import MacOSX
        system = MacOSX.MacOSX
    else:
        import Darwin
        system = Darwin.Darwin
else:
    raise NotImplementedError("Your operating system is not supported.")
