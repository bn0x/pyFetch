import Unix
import re
import os
import subprocess

class Linux(Unix.Unix):
    """\
    Linux platform class.
    """

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

        class CrunchBang(Distro):
            name = "CrunchBang"
            fallback = { "file": "/etc/crunchbang-lsb-release", "check": [ "exists" ] }

        class Debian(Distro):
            name = "Debian"
            lsb = { "distid": "[Dd]ebian" }
            fallback = { "file": "/etc/debian_version", "check": [ "exists" ] }

        class Ubuntu(Distro):
            name = "Ubuntu"
            lsb = { "distid": "[Uu]buntu" }

    show_kernel = True

    def get_distro(self):
        """\
        Return information on the Linux distribution the system is currently running.

        :rtype: `:class: pyFetch.Linux.Distro.Distro`
        """

        for d in dir(self.Distro):
            if d[0] == "_": continue
            if d == "Distro": continue
            e = eval("self.Distro.%s" % d)
            s = e()

            # LSB search
            try:
                output = subprocess.check_output(["lsb_release", "-sirc"], stderr=subprocess.STDOUT).split('\n')[0].split()
                if re.search(s.lsb['distid'], output[0]):
                    ver = output[1] if output[1].strip() != "rolling" else ''
                    return { 'distro': e, 'ver': ver, 'codename': output[2] if output[2] != "n/a" else '' }

            except:
                pass

            # Fallback
            try:
                if "exists" in s.lsb['check'] or "content" in s.lsb['check']:
                    with open(s.fallback['file']) as f:
                        if not "content" in s.lsb['check']:
                            return { 'distro': e, 'ver': '', 'codename': '' }

                        for x in f:
                            if s.fallback['content'] in x:
                                return { 'distro': e, 'ver': '', 'codename': '' }

            except IOError:
                pass

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
        return { 'name': " ".join([distro['distro']().name, distro['ver'], distro['codename']]) }

    def kernel(self):
        """\
        Return the kernel version.

        :rtype: string
        """

        return " ".join([s.strip() for s in re.sub("Linux", "", Unix.Unix().os_release()['name']).split()])
