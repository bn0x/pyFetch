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
elif platform.system() == "Darwin":
    # we're assuming Darwin means Mac OS X here.
    # sorry, Darwin guys.
    import MacOSX
    system = MacOSX.MacOSX
else:
    raise NotImplementedError("Your operating system is not supported.")
