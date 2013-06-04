import pyFetch.Debug

class PlatformBase(object):
    """\
    Base class for pyFetch platform modules.
    """

    show_kernel = False
    "Whether or not to show the Kernel line in the output."

    def collate_data(self, info=False, excludes=[]):
        """\
        Call every defined function in the platform class and return their
        values in a dictionary, keyed by the function name.
        """

        twist = {}
        excludes = ['collate_data', 'disk_usage', 'screen_shot'] + excludes

        pyFetch.Debug.debug("Starting collate_data (info provided: %s, excludes: %s)" % (bool(info), str(excludes)))

        if not info:
            info = []
            t = []
            for name in dir(self):
                obj = eval("self.%s" % name)
                if not str(type(obj)) == "<type 'instancemethod'>":
                    continue
                if name.startswith('_'):
                    continue
                if name in excludes:
                    continue
                t.append(name)
                info.append((name, obj))

        pyFetch.Debug.debug("collate_data: will get %s" % str(t))

        for name, obj in info:
            try:
                twist[name] = obj()
            except:
                pyFetch.Debug.debug("collate_data: failed in %s, adding 'False' in it's place" % name)
                twist[name] = False
                pass

        pyFetch.Debug.debug("collate_data: done.")
        return twist

    def username(self):
        """\
        Return the name of the currently logged in user.
        """

        return __import__("getpass").getuser()

    def hostname(self):
        """\
        Get the system hostname.
        """

        return __import__("socket").gethostname()

    def default_ascii(self):
        """\
        Return the name of the default ASCII art for this platform.

        :rtype: string
        """

        return "default"

    def disk_usage(self, path):
        """\
        Get disk usage statistics about the given path.
        Returns a dict with items 'total', 'used' and 'free' as bytes.

        :param path: string
        :rtype: dict
        """

        return { 'total': 0, 'used': 0, 'free': 0 }

    def system_disk_usage(self):
        """\
        Returns the `disk_usage(...)` dict for the root filesystem.

        :rtype: dict
        """

        return self.disk_usage("")

    def ram(self):
        """\
        Get RAM statistics.
        Returns a dict with items 'total', 'used' and 'free' as bytes.

        :rtype: dict
        """

        return { 'total': 0, 'used': 0, 'free': 0 }

    def uptime(self):
        """\
        Return the system uptime in seconds.

        :rtype: int
        """

        return float(0)

    def os_release(self):
        """\
        Return a human-readable string of the OS release information.

        :rtype: string
        """

        return { 'name': 'Unknown', 'ver': 'Unknown', 'codename': 'Unknown' }

    def cpu(self):
        """\
        Get information on the system CPU.
        Returns a dict with 'name', 'load_percentage' values.

        :rtype: dict
        """

        return { 'name': "Unknown", 'load_percentage': 0.0 }
    
    def gpu(self):
        """\
        Get the GPU name.

        :rtype: string
        """

        return "Unknown"    

    def screen_resolution(self):
        """\
        Get the current screen resolution as a dict with 'x' and 'y' values.

        :rtype: dict
        """

        return { 'x': 0, 'y': 0 }

    def web_browser(self):
        """\
        Get the default webbrowser of the system.

        :rtype: dict
         """

        return { 'raw': "Unknown", 'name': "Unknown" }

    def screen_shot(self):
        """\
        Take a screenshot of the desktop.
        Returns True on success, False on failure.

        :rtype: bool
        """

        return False

    def window_manager(self): 
        """\
        Get current window manager.

        :rtype: dict
        """

        return { 'raw': "Unknown", 'name': "Unknown" }

    def visual_style(self):
        """\
        Current visual style.

        :rtype: dict
        """
    
        return { 'name': "Unknown" }

    def arch(self):
        """\
        Return platform architecture.
    
        :rtype: dict
        """

        return { 'arch': "unknown" }

