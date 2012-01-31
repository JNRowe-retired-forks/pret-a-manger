#!/usr/bin/env python


from setuptools import setup, find_packages
readme = open('README').read()

long_description = readme

setup(
    name='pret-a-manger',
    version='0.1',
    description='Pret-a-manger is a simple command line tool to list the menu of pret and organizing order.',
    long_description=long_description,
    author='Rachid Belaid',
    author_email='rachid.belaid@gmail.com',
    url='https://github.com/rachid/pret-a-manger',
    packages=find_packages(),
    license = "MIT",
    entry_points={
        'console_scripts': [
            'pret = pret.main:main',
        ]
    },
    install_requires=[
        'BeautifulSoup',
        'termcolor',
        'xmlrpclib',
    ]

)