import Unix
import re
import os
import subprocess

class Linux(Unix.Unix):
    """\
    Linux platform class.
    """

    class Distro(object):

        class DistroBase(object):
            """\
            Object to represent a Linux distribution.
            """

            name = ""
            ascii_art = ""
            lsb = { "distid": "" }
            fallback = { "file": "", "content": "" }

        class UnknownDistro(DistroBase):
            """\
            Object to represent an unknown Linux distribution.
            """

            name = "Unknown Distro"
            ascii_art = "unix_placeholder"

        class ArchLinux(DistroBase):
            """\
            Arch Linux

            LSB: Arch Linux; arch
            Fallback: look for /etc/pacman.d/mirrorlist
            """

            name = "Arch Linux"
            ascii_art = "arch_big"
            lsb = { "distid": "arch" }
            fallback = { "file": "/etc/pacman.d/mirrorlist", "content": "archlinux" }

    show_kernel = True

    def get_distro(self):
        """\
        Return information on the Linux distribution the system is currently running.

        :rtype: `:class: pyFetch.Linux.Distro`
        """

        for d in dir(self.Distro):
            if d[0] == "_": continue
            if d == "DistroBase" or d == "UnknownDistro": continue
            e = eval("self.Distro.%s" % d)
            s = e()

            # LSB search
            try:
                output = subprocess.check_output(["lsb_release", "-sirc"], stderr=subprocess.STDOUT).split('\n')[0].split()
                if output[0] == s.lsb['distid']:
                    return { 'distro': e, 'ver': output[1], 'codename': output[2] if output[2] != "n/a" else '' }

            except:
                pass

            # Fallback
            try:
                with open(s.fallback['file']) as f:
                    for x in f:
                        if s.fallback['content'] in x:
                            return { 'distro': e, 'ver': '', 'codename': '' }

            except IOError:
                pass

            return { 'distro': self.Distro.UnknownDistro, 'ver': '', 'codename': '' }

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
