# coding: utf-8
# 
# A setuptools based setup module. This code was derived from the
# template produced by the Adafruit CookieCutter app. 
#
# See:
# https://packaging.python.org/en/latest/distributing.html
# https://github.com/pypa/sampleproject
#
# Copyright © 2018 Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE.md file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE.md file).  If not, see <http://www.gnu.org/licenses/>.
#
# To build the package
# python setup.py build
#
# To install the package in the current venv
# python setup.py install
#
# To build a source distribution:
# python setup.py sdist
#

# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='circuitpython-dotstarapa102',

    use_scm_version=True,
    setup_requires=['setuptools_scm'],

    description='Adafruit DotStar APA102 based LED string driver.',
    long_description=long_description,
    long_description_content_type='text/x-rst',

    # The project's main homepage.
    url='https://github.com/dhocker/CircuitPython_DotStarAPA102',

    # Author details
    author='Dave Hocker',
    author_email='AtHomeX10@gmail.com',

    install_requires=['Adafruit-Blinka', 'adafruit-circuitpython-busdevice'],

    # Choose your license
    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Hardware',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: Raspbian',
    ],

    # What does your project relate to?
    keywords='adafruit spi circuitpython dotstar APA102',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['circuitpython_dotstarapa102'],
)
