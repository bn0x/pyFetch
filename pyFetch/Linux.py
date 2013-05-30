import Unix
import re
import os
import subprocess


class Linux(Unix.Unix):
    """\
    Linux platform class.
    """

    show_kernel = True
    distroforce = ""
    "Name of distro to force get_distro() to display."

    class Distro(object):
        class Distro(object):
            """\
            Object to represent a Linux distribution.
            """

            name = "Unknown"
            ascii_art = "unix_placeholder"
            lsb = { "distid": "" }
            fallback = { "file": "", "check": [ "exists", "content" ],"content": "" }

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

    def get_distro(self, debug=False):
        """\
        Return information on the Linux distribution the system is currently running.

        :rtype: `:class: pyFetch.Linux.Distro.Distro`
        """

        for d in dir(self.Distro):
            if d[0] == "_":
                continue
            if d == "Distro":
                continue

            e = eval("self.Distro.%s" % d)
            s = e()

            if debug: print "Distro: %s" % d

            # Check if we've been forced.
            if self.distroforce:
                if self.distroforce == d:
                    return { 'distro': e, 'ver': '', 'codename': '' }
                else:
                    continue


            # LSB search
            try:
                if s.lsb['distid'] is False:
                    if debug: print "Skipping LSB check."
                    continue

                output = " ".join([o.strip() for o in subprocess.check_output(["lsb_release", "-sirc"], stderr=subprocess.STDOUT).split("\n")]).strip().split()
                if debug: print "LSB: %s" % output

                if re.search(s.lsb['distid'], output[0]):
                    if debug: print "LSB match."
                    ver = output[1] if output[1].strip() != "rolling" else ''
                    if 'codename' in s.lsb:
                        if re.search(s.lsb['codename'], output[2]):
                            if debug: print "Codename."
                            return { 'distro': e, 'ver': ver, 'codename': output[2] if output[2] != "n/a" else '' }

                    if debug: print "No codename."
                    return { 'distro': e, 'ver': ver, 'codename': '' }

            except:
                pass

        for d in dir(self.Distro):
            if d[0] == "_":
                continue
            if d == "Distro":
                continue

            e = eval("self.Distro.%s" % d)
            s = e()

            if debug: print "Distro: %s" % d

            # Fallback
            try:
                if debug: print "Fallback"
                if "exists" in s.fallback['check'] or "content" in s.fallback['check']:
                    with open(s.fallback['file']) as f:
                        if debug: print "File found."
                        if not "content" in s.fallback['check']:
                            return { 'distro': e, 'ver': '', 'codename': '' }

                        for x in f:
                            if s.fallback['content'] in x:
                                if debug: print "Content match."
                                return { 'distro': e, 'ver': '', 'codename': '' }

            except:
                pass

        if debug: print "Unknown."
        return { 'distro': self.Distro.Distro, 'ver': '', 'codename': '' }

    def default_ascii(self):
        """\
        Return the name of the default ASCII art for this platform.

        :rtype: string
        """

        return self.get_distro()['distro'].ascii_art

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

