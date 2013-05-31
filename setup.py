import platform
from setuptools import setup

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
    version='0.1.0',
    description='Python system information tool',
    author='bn0x and aki--aki',
    author_email='0_bn0x@hushmail.com',
    url='https://github.com/bn0x/pyFetch',
    packages=['pyFetch', 'pyFetch.ascii'],
    package_data={'pyFetch': ['helpers/macosx/*']},
    classifiers=[
        "License :: The Beer-ware Licence (Revision 44)",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
    ],
    scripts=['bin/pyfetch'],
    keywords='screenshot system_information',
    license='The Beer-Ware Licence (Revision 44)',
    install_requires=requires,
)
