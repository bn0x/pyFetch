import Unix
import re
import os
import subprocess
import inspect
from datetime import timedelta

try:
    import lxml.etree
    lxml_enabled = True
except:
    lxml_enabled = False


class MacOSX(Unix.Unix):
    """\
    Mac OS X platform class.

    We inherit Unix because we're *technically* a Unix OS, and some stuff there
    will work here.
    """

    def default_ascii(self):
        """\
        Return the name of the default ASCII art for this platform.

        :rtype: string
        """

        #return "macosx"
        return "unix_placeholder"

    def uptime(self):
        """\
        Return the system uptime in seconds.

        :rtype: int
        """

        output = subprocess.check_output(['sysctl', '-n', 'kern.boottime']).strip()
        boottime = re.search('sec = (\d+),', output).group(1)
        return timedelta(seconds=float(boottime)).seconds

    def os_release(self):
        """\
        Return a human-readable string of the OS release information.

        :rtype: string
        """

        def get_codename(version):
            """\
            Get Mac OS X codename from a version number string.
            """

            assert isinstance(version, str), "Version must be <type: 'str'>, got %s" % typeof(version)

            codenames = [
                ["10.0", "Cheetah"],
                ["10.1", "Puma"],
                ["10.2", "Jaguar"],
                ["10.3", "Panther"],
                ["10.4", "Tiger"],
                ["10.5", "Leopard"],
                ["10.6", "Snow Leopard"],
                ["10.7", "Lion"],
                ["10.8", "Mountain Lion"],
            ]

            for num, codename in codenames:
                if version.startswith(num):
                    return codename

            return ''

        def lxml_get_version():
            """\
            Get Mac OS X version using lxml.
            """

            try:
                systemversion = lxml.etree.parse(open('/System/Library/CoreServices/SystemVersion.plist', 'r'))
                version = systemversion.xpath("//key[text() == 'ProductVersion']")
                return { 'name': 'Mac OS X', 'ver': version, 'codename': get_codename(version) }
            except:
                return None

        def fallback_get_version():
            """\
            Get Mac OS X version using a generic string capture method.
            """

            # don't wrap this in a try/catch so our code below correctly handles
            # it and returns a generic value

            mark = False
            version = ""
            with open('/System/Library/CoreServices/SystemVersion.plist', 'r') as f:
                for line in f:
                    if re.search('ProductVersion', line):
                        mark = True
                    elif mark:
                        version = re.search('<string>(.*)</string>', line.strip()).group(1)
                        break

            return { 'name': 'Mac OS X', 'ver': version, 'codename': get_codename(version) }

        try:
            if lxml_enabled:
                t = lxml_get_version()
                if t:
                    return t
                else:
                    return fallback_get_version()
            else:
                return fallback_get_version()
        except:
            return { 'name': 'Mac OS X', 'ver': '10.x', 'codename': 'Unknown' }

    def web_browser(self):
        """\
        Get the default webbrowser of the system.

        :rtype: dict
        """

        def get_name(browser):
            """\
            Get web browser name from a defbrowser returned key.
            """

            assert isinstance(browser, str), "browser must be <type: 'str'>, got %s" % typeof(browser)

            names = [
                ["org.mozilla.firefox", "Firefox"],
                ["org.apple.safari", "Safari"],
            ]

            for v, i in names:
                if browser.startswith(v):
                    return i

            return browser

        try:
            path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            path = os.path.join(path, "helpers", "macosx", "defbrowser")

            if os.path.isfile(path):
                defbrowser = subprocess.check_output([path]).strip()
                return { 'raw': defbrowser, 'name': get_name(defbrowser) }
            else:
                # we should fallback here somehow
                return { 'raw': 'Unknown', 'name': "Unknown" }
        except: 
            return { 'raw': 'Unknown', 'name': "Unknown" }


    def cpu(self):
        """\
        Get information on the system CPU.
        Returns a dict with 'name', 'load_percentage' values.

        :rtype: dict
        """

        load_percentage = 0.00

        try:
            output = subprocess.check_output(["top", "-l1", "-n1", "-ncols", "1"], stderr=subprocess.STDOUT).split("\n")
            for x in output:
                if 'CPU usage' in x:
                    y = x.split(",")
                    for z in y:
                        if 'idle' in z:
                            z = re.sub("% idle", "", z)
                            load_percentage = 100 - float(z.strip())
        except:
            pass

        name = subprocess.check_output(['sysctl', '-bn', 'machdep.cpu.brand_string']).strip()
        name = " ".join([s.strip() for s in name.split()])
        return { 'name': name, 'load_percentage': load_percentage }
    
    def gpu(self):
        """\
        Get the GPU name.

        :rtype: string
        """

        try:
            output = subprocess.check_output(['/usr/sbin/system_profiler', 'SPDisplaysDataType'])
            for s in [y.strip() for y in output.split('\n')]:
                if s.startswith('Chipset Model'):
                    return s.split(': ')[1]
        except:
            return "Unknown"

    def screen_resolution(self):
        """\
        Get the current screen resolution as a dict with 'x' and 'y' values.

        :rtype: dict
        """

        try:
            output = subprocess.check_output(['/usr/sbin/system_profiler', 'SPDisplaysDataType'])
            for s in [y.strip() for y in output.split('\n')]:
                if s.startswith('Resolution'):
                    s = s.split(': ')[1].split(' x ')
                    return { 'x': s[0], 'y': s[1] }
        except:
            return { 'x': 0, 'y': 0 }

    def ram(self):
        """\
        Get RAM statistics.
        Returns a dict with items 'total', 'used' and 'free' as bytes.

        :rtype: dict
        """

        return { 'total': 0, 'used': 0, 'free': 0 }

    def visual_style(self):
        """\
        Current visual style.

        :rtype: dict
        """
        try:
            path = ['defaults', 'read', '-globalDomain', 'AppleAquaColorVariant']
            key = subprocess.check_output(path).strip()
            friendly = {
                '1': 'Aqua',
                '6': 'Graphite',
            }

            return { 'name': friendly[key] }
        except:
            return { 'name': "Unknown" }
