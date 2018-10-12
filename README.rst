Introduction
============

DotStarAPA102 is a CircuitPython based driver for Adafruit DotStar strings that use the
APA102/APA102C chip. It was inspired by the
`Adafruit_DotStar_Pi <https://github.com/adafruit/Adafruit_DotStar_Pi>`_
package. By basing the driver on CircuitPython we avoid the need for C/C++ code like
that found in the Adafruit_DotStar_Pi package.

**DotStarAPA102 is specifically designed for the Raspberry Pi.**

.. todo:: Describe what the library does.

Dependencies
=============

This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `SPI Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Since this package uses SPI for driving the DotStar LEDs, you need to make sure that
SPI is enabled. The easiest way to do this is to use the Raspberry Pi desktop.
Find the Preferences|Raspberry Pi Configuration menu item (start with the
Raspberry icon). Choose the Interfaces tab. Click the Enable button for SPI.
Click OK to finish.

An alternative to the desktop method for enabling SPI is raspi-config. See
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-spi.

Wiring Diagram
==============

DotStarAPA102 uses the standard SPI interface on the RPi. The following diagram
shows the basic wiring for an RPi. Note that something like a 74AHCT125 buffer chip
is required to do level shifting from 3.3V to 5V. In this case the SPI_CLK
and SPI_MOSI signals are level shifted. See
https://learn.adafruit.com/adafruit-dotstar-leds for more details on DotStars.

.. image:: ./docs/DotStar-Wiring-Diagram.png
   :alt: DotStar Wiring Diagram


Installing from Source
======================

Here we install the CircuitPython_DotStarAPA102 package into a VENV.

.. code-block:: shell

    workon your-venv-name
    cd ~/CircuitPython_DotStarAPA102
    python setyup.py install

This sequence activates your VEVN, changes into its home directory and runs the
setup.py script.

Usage Example
=============

The examples directory contains test files that serve as coding examples. You
can test your install results as follows. This should work even if you have not
wired up a DotStar string.

.. code-block:: shell

    workon your-venv-name
    cd ~/CircuitPython_DotStarAPA102
    python examples/dotstarapa102_test.py

Sphinx documentation
-----------------------

TBD

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.

Appendices
==========

Building a VENV
---------------
If you aren't very familiar with virtual envionments (venv's), this should help
you get started.

Some useful links:

* https://howchoo.com/g/nwewzjmzmjc/a-guide-to-python-virtual-environments-with-virtualenvwrapper
* https://realpython.com/python-virtual-environments-a-primer/.

Setup virtualenv and virtualenvwrapper
**************************************

The following steps assume that you have installed virtualenv and virtualenvwrapper.
These can be installed system wide as follows.

.. code-block:: shell

    sudo pip3 install virtualenv virtualenvwrapper

Create a directory for your VENVs.

.. code-block:: shell

    mkdir ~/Virtualenvs

Add these lines to the bottom of your ~/.bashrc file.

.. code-block:: shell

    # For virtualenvwrapper
    export WORKON_HOME=~/Virtualenvs
    # this is required to get to the correct version of Python.
    # Otherwise, you will get an error complaining about no virtualenvwrapper module
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    source /usr/local/bin/virtualenvwrapper.sh

Create a VENV
*************

Clone the GitHub repo to a location of your choice (~/CircuitPython_DotStarAPA102
in this example).

.. code-block:: shell

    mkvirtualenv -p /usr/bin/python3 your-venv-name
    cd ~/CircuitPython_DotStarAPA102
    pip install -r requirements.txt

You are now ready to install the CircuitPython_DotStarAPA102 package.
