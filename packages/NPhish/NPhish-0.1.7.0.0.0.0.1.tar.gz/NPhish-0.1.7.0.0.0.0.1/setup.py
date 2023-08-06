from setuptools import setup

long_description = open('README.md').read()

setup(name = "NPhish",
version = "0.1.7.0.0.0.0.1",
license = 'LICENCE',
description = "Ultimate Phishing Tool in Python",
long_description = long_description,
long_description_content_type = 'text/markdown',
author = "Nishant",
url = 'https://github.com/Nishant2009/NPhish/',
scripts = ['NPhish'],
install_requires = ['colourfulprint==1.5', 'colorama==0.4.5', 'requests==2.28.1', 'wget==3.2'],
classifiers = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
], )
