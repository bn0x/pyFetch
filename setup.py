import platform
from setuptools import setup
import pyFetch

requires = [
    'colorama',
]

if platform.system() == "Windows":
    requires += [
        'WMI',
        'PIL',
        'pywin32',
    ]

setup(
    name='pyFetch',
    version=pyFetch.version,
    description='Python system information tool',
    author='bn0x and aki--aki',
    author_email='0_bn0x@hushmail.com',
    url='https://github.com/bn0x/pyFetch',
    packages=['pyFetch', 'pyFetch.ascii'],
    package_data={'pyFetch': ['helpers/macosx/*']},
    classifiers=[
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
    ],
    scripts=['bin/pyfetch'],
    keywords='screenshot system_information',
    license='Public Domain',
    install_requires=requires,
)
