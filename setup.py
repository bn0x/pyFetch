import os
import pyFetch
import platform
from setuptools import setup
from setuptools.command.install import install as _install

requires = [
    'colorama',
]

scripts = [
    'bin/pyfetch',
]

if platform.system() == "Windows":
    requires += [
        'WMI',
        'PIL',
        'pywin32',
    ]
elif platform.system() == "Darwin":
    scripts += [
        'bin/pyfetch_macosx_defbrowser',
    ]

setup(
    name='pyFetch',
    version=pyFetch.version,
    description='Python system information tool',
    author='bn0x and aki--aki',
    author_email='0_bn0x@hushmail.com',
    url='https://github.com/bn0x/pyFetch',
    packages=['pyFetch', 'pyFetch.ascii'],
    classifiers=[
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
    ],
    scripts=scripts,
    keywords='screenshot system_information',
    license='Public Domain',
    install_requires=requires,
)
