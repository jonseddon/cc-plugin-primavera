from __future__ import with_statement
import sys

from setuptools import setup, find_packages

from cc_plugin_primavera import __version__

def readme():
    with open('README.md') as f:
        return f.read()

reqs = [line.strip() for line in open('requirements.txt')]

setup(name                 = "cc-plugin-primavera",
    version              = __version__,
    description          = "Compliance Checker PRIMAVERA plugin",
    long_description     = readme(),
    license              = 'BSD License',
    author               = "Jon Seddon",
    author_email         = "jon.seddon@metoffice.gov.uk",
    url                  = "https://github.com/jonseddon/cc-plugin-primavera",
    packages             = find_packages(),
    install_requires     = reqs,
    classifiers          = [
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering',
        ],
    entry_points         = {
        'compliance_checker.suites': [
            'primavera = cc_plugin_primavera.primavera:PrimCheck',
        ]
    }
)

