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
            lsb = { "distid": "", "description": "" }
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
            lsb = { "distid": "arch", "description": "Arch Linux" }
            fallback = { "file": "/etc/pacman.d/mirrorlist", "content": "archlinuix" }

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
                output = subprocess.check_output(["lsb_release", "-a"], stderr=subprocess.STDOUT).split('\n')
                for line in output:
                    line = " ".join([g.strip() for g in line.split()])
                    if "Distribution ID: %s" % s.lsb['distid'] in line:
                        return e
                    elif "Description: %s" % s.lsb['description'] in line:
                        return e
            except:
                pass

            # Fallback
            try:
                with open(s.fallback['file']) as f:
                    for x in f:
                        if s.fallback['content'] in x:
                            return e
            except IOError:
                pass

            return self.Distro.UnknownDistro

    def default_ascii(self):
        """\
        Return the name of the default ASCII art for this platform.

        :rtype: string
        """

        return self.get_distro().ascii_art

    def os_release(self):
        """\
        Return a human-readable string of the OS release information.

        :rtype: string
        """

        inherit = re.sub("Linux", "", Unix.Unix().os_release()).strip()
        return { 'name': "%s %s" % (self.get_distro().name, inherit) }
