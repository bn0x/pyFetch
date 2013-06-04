import Unix
import re
import os
import subprocess
import inspect
import pyFetch.Art
import pyFetch.Debug
import pyFetch.Format
from datetime import datetime
import time

try:
    import lxml.etree
    pyFetch.Debug.debug("lxml successfully imported, will use it to get version")
    lxml_enabled = True
except:
    pyFetch.Debug.debug("can't import lxml, will use fallback_get_version")
    lxml_enabled = False


class MacOSX(Unix.Unix):
    """\
    Mac OS X platform class.
    """

    # We inherit Unix because we're *technically* a Unix OS, and some stuff there
    # will work here. In the future, we should switch to inheriting Darwin and move
    # common things from this class to the Darwin class (ie. non-OS X-specifics like
    # uptime and RAM usage).

    def default_ascii(self):
        """\
        Return the default ASCII module for this platform.
        """

        return pyFetch.Art.macosx

    def uptime(self):
        """\
        Return the system uptime in seconds.

        :rtype: int
        """

        output = subprocess.check_output(['sysctl', '-n', 'kern.boottime']).strip()
        boottime = int(re.search('sec = (\d+),', output).group(1))
        currenttime = int(time.time())
        diff = currenttime - boottime
        pyFetch.Debug.debug("Kernel boot time: %d, current time: %d, %d seconds (%s) since boot" 
            % (boottime, currenttime, diff, pyFetch.Format.time_metric(diff)))
        return diff

    def hostname(self):
        return re.sub('.local$', '', pyFetch.Platform.PlatformBase.PlatformBase().hostname())

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

            t = []
            found = False
            for num, codename in codenames:
                t.append(num)
                if version.startswith(num):
                    found = True
                    break

            pyFetch.Debug.debug("Checking Mac OS X version: %s%s" % (", ".join(t), " okay" if found else " not found"))
            return codenames[len(t) - 1][1]

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
                    pyFetch.Debug.debug("lxml version retrieval succeeded")
                    return t
                else:
                    pyFetch.Debug.debug("lxml version retrieval failed, using fallback_get_version")
                    return fallback_get_version()
            else:
                return fallback_get_version()
        except:
            pyFetch.Debug.debug("Version retrieval failed.")
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

            assert isinstance(browser, str), "browser must be <type: 'str'>, got %s" % type(browser)

            names = [
                ["org.mozilla.firefox", "Firefox"],
                ["org.apple.safari", "Safari"],
                ["com.google.chrome", "Chrome"],
            ]

            t = []
            found = False
            for v, i in names:
                t.append(v)
                if browser.startswith(v):
                    found = True
                    break

            pyFetch.Debug.debug("Searching for default browser: %s%s" % (", ".join(t), " okay" if found else " not found"))
            return names[len(t) - 1][1]

        try:
            pyFetch.Debug.debug("Calling pyfetch_macosx_defbrowser to get default browser...")
            defbrowser = subprocess.check_output(['pyfetch_macosx_defbrowser']).strip()            
            return { 'raw': defbrowser, 'name': get_name(defbrowser) }
        except: 
            pyFetch.Debug.debug("Calling pyfetch_macosx_defbrowser failed")
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
                            pyFetch.Debug.debug("CPU: %s" % z)
                            z = re.sub("% idle", "", z)
                            load_percentage = 100 - float(z.strip())
        except:
            pass

        name = subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string']).strip()
        name = " ".join([s.strip() for s in name.strip().split()])
        pyFetch.Debug.debug("CPU: %s" % name)
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
                    pyFetch.Debug.debug("GPU: %s" % s)
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
                    pyFetch.Debug.debug("SPDisplaysDataType: %s" % s)
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

        total = float(subprocess.check_output(['sysctl', '-n', 'hw.physmem']).strip())
        used = float(subprocess.check_output(['sysctl', '-n', 'hw.usermem']).strip())
        pyFetch.Debug.debug("Memory: %d total, %d used" % (total, used))
        return { 'total': total, 'used': used, 'free': total - used }

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

            pyFetch.Debug.debug("AppleAquaColorVariant = %s (%s)" % (key, friendly[key] if key in friendly else "Unknown"))
            return { 'name': friendly[key] }
        except:
            return { 'name': "Unknown" }

    def screen_shot(self):
        """\
        Take a screenshot of the desktop.
        Returns True on success, False on failure.

        :rtype: bool
        """

        try:
            print "Capturing screenshot in 5 seconds..."
            subprocess.check_output(['screencapture', '-tpng', '-T5', os.path.join(os.environ['HOME'], 'Desktop', 'pyFetch - ' + datetime.now().ctime() + '.png')])
            return True
        except:
            return False
