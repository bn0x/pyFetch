import Unix
import re
import os
import subprocess
import pyFetch.Debug


class Linux(Unix.Unix):
    """\
    Linux platform class.
    """

    show_kernel = True
    distroforce = ""
    "Name of distro to force get_distro() to display."

    def __init__(self):
        self.detected_distro = False

    def collate_data(self, info=False, excludes=[]):
        excludes = ['get_distro', 'force_distro'] + excludes
        return super(self.__class__, self).collate_data(excludes=excludes)

    class Distro:
        class Distro:
            """\
            Object to represent a Linux distribution.
            """

            name = "Unknown"
            ascii_art = "unix_placeholder"
            lsb = { "distid": "" }
            fallback = { "file": "", "check": [ "exists", "content" ], "content": "" }

        class GenericDistro(Distro):
            pass

        class ArchLinux(Distro):
            name = "Arch Linux"
            ascii_art = "arch_big"
            lsb = { "distid": "(arch|archlinux|Arch Linux)" }
            fallback = { "file": "/etc/arch-release", "check": [ "exists" ] }

        class Gentoo(Distro):
            name = "Gentoo"
            ascii_art = "gentoo"
            lsb = { "distid": "gentoo" }
            fallback = { "file": "/etc/gentoo-release", "check": [ "exists" ] }

        class Debian(Distro):
            name = "Debian"
            lsb = { "distid": "[Dd]ebian" }
            fallback = { "file": "/etc/debian_version", "check": [ "exists" ] }

        class Ubuntu(Distro):
            name = "Ubuntu"
            ascii_art = "ubuntu"
            lsb = { "distid": "[Uu]buntu" }

        class LMDE(Distro):
            name = "LMDE"
            lsb = { "distid": "[Mm]int", "codename": "[Dd]ebian" }

        class Mint(Distro):
            name = "Linux Mint"
            lsb = { "distid": "[Mm]int" }

        class CrunchBang(Distro):
            name = "CrunchBang"
            lsb = { "distid": False }
            fallback = { "file": "/etc/crunchbang-lsb-release", "check": [ "exists" ] }

    def force_distro(self, distro):
        """\
        Force the get_distro() function to return the selected distro.

        :param distro: string
        :rtype: None
        """

        global distroforce
        self.distroforce = distro
        return None

    def get_distro(self):
        """\
        Return information on the Linux distribution the system is currently running.

        :rtype: `:class: pyFetch.Linux.Distro.Distro`
        """

        if self.detected_distro:
            pyFetch.Debug.debug("Skipping distro detection because we've been run before this session. self.detected_distro: %s" % str(self.detected_distro['distro']))
            return self.detected_distro

        for d in dir(self.Distro):
            if d[0] == "_":
                continue
            if d == "Distro":
                continue

            e = eval("self.Distro.%s" % d)
            s = e()

            pyFetch.Debug.debug("Distro: %s" % d)

            # Check if we've been forced.
            if self.distroforce:
                if self.distroforce == d:
                    self.detected_distro = { 'distro': e, 'ver': '', 'codename': '' }
                    return self.detected_distro
                else:
                    continue


            # LSB search
            try:
                if s.lsb['distid'] is False:
                    pyFetch.Debug.debug("Skipping LSB check.")
                    raise

                output = " ".join([o.strip() for o in subprocess.check_output(["lsb_release", "-sirc"], stderr=subprocess.STDOUT).split("\n")]).strip().split()
                pyFetch.Debug.debug("Distro %s: LSB should be %s" % (d, str(output)))

                if re.search(s.lsb['distid'], output[0]):
                    pyFetch.Debug.debug("Distro %s: LSB match." % d)
                    ver = output[1] if output[1].strip() != "rolling" else ''
                    if 'codename' in s.lsb:
                        if re.search(s.lsb['codename'], output[2]):
                            pyFetch.Debug.debug("Distro %s: LSB codename found." % d)
                            self.detected_distro = { 'distro': e, 'ver': ver, 'codename': output[2] if output[2] != "n/a" else '' }
                            return self.detected_distro

                    pyFetch.Debug.debug("Distro %s: No codename." % d)
                    self.detected_distro = { 'distro': e, 'ver': ver, 'codename': '' }
                    return self.detected_distro

            except:
                pass

        for d in dir(self.Distro):
            if d[0] == "_":
                continue
            if d == "Distro":
                continue

            e = eval("self.Distro.%s" % d)
            s = e()

            try:
                # Fallback
                pyFetch.Debug.debug("Distro %s: Fallback detection mode" % d)
                if "exists" in s.fallback['check'] or "content" in s.fallback['check']:
                    with open(s.fallback['file']) as f:
                        pyFetch.Debug.debug("Distro %s: File found.")
                        if not "content" in s.fallback['check']:
                            self.detected_distro = { 'distro': e, 'ver': '', 'codename': '' }
                            return self.detected_distro
                        for x in f:
                            if s.fallback['content'] in x:
                                pyFetch.Debug.debug("Distro %s: File content match." % d)
                                self.detected_distro = { 'distro': e, 'ver': '', 'codename': '' }
                                return self.detected_distro

            except:
                pass

        pyFetch.Debug.debug("Unknown distro.")
        self.detected_distro = { 'distro': self.Distro.GenericDistro, 'ver': '', 'codename': '' }
        return self.detected_distro

    def default_ascii(self):
        """\
        Return the name of the default ASCII art for this platform.

        :rtype: string
        """
        distro = self.get_distro()['distro']()
        pyFetch.Debug.debug("Linux default_ascii: getting art for %s" % distro.name)
        return distro.ascii_art

    def os_release(self):
        """\
        Return a human-readable string of the OS release information.

        :rtype: dict
        """

        distro = self.get_distro()
        return { 'name': distro['distro'].name, 'ver': distro['ver'], 'codename': distro['codename'] }
    
    def kernel(self):
        """\
        Return the kernel version.

        :rtype: string
        """

        return " ".join([s.strip() for s in re.sub("Linux", "", Unix.Unix().os_release()['name']).split()])

    def web_browser(self):
        """\
        Get the default webbrowser of the system.

        :rtype: dict
        """

        try:
            output = " ".join([o.strip() for o in subprocess.check_output(["xdg-settings", "get", "default-web-browser"], stderr=subprocess.STDOUT).split(" ")])
            if ".desktop" in output:
                name = re.sub(".desktop", "", output)
                t = []
                for i in [o.strip() for o in name.split("-")]:
                    i = i[0].upper() + i[1:]
                    t.append(i)
                name = " ".join(t)
                return { 'raw': output, 'name': name }
            else:
                return { 'raw': "Unknown", 'name': "Unknown" }
        except:
            return { 'raw': "Unknown", 'name': "Unknown" }

