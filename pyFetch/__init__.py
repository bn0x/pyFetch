import platform
import format

if platform.system() == "Windows":
    import win32 as system
elif platform.system() == "Linux":
    import unix as system