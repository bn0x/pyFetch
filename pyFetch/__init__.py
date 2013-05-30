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
    raise NotImplementedError("Your operating system is not supported.")
