import Unix
import re

class Linux(Unix.Unix):
    """\
    Linux platform class.
    """

    class Distro(object):
        """\
        Object to represent a Linux distribution.
        """

        name = ""
        ascii_art = ""

    class UnknownDistro(Distro):
        """\
        Object to represent an unknown Linux distribution.
        """

        name = "Unknown Distro"
        ascii_art = "unix_placeholder"

    def get_distro(self):
        """\
        Return information on the Linux distribution the system is currently running.

        :rtype: `:class: pyFetch.Linux.Distro`
        """

        return self.UnknownDistro

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
