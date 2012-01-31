#!/usr/bin/env python


from setuptools import setup, find_packages
from projrest.version import get_version
readme = open('README').read()

long_description = readme

setup(
    name='pret-a-manger',
    version=get_version('short'),
    description='Pret is a simple command line tool to list the menu of pret and organizing order.',
    long_description=long_description,
    author='Rachid Belaid',
    author_email = "rachid@ironbraces.com",
    url='https://github.com/rachid/pret',
    packages=find_packages(),
    license = "MIT",
    entry_points={
        'console_scripts': [
            'pret = pret.main:main',
        ]
    },
    requires=[
        'BeautifulSoup',
        'termcolor',
        'xmlrpclib',
    ],
    install_requires=[
        'BeautifulSoup',
        'termcolor',
        'xmlrpclib'
    ]
)