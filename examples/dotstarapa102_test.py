# -*- coding: utf-8 -*-
#
# Test and example of DotStarAPA102 driver.
# Copyright © 2018  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE.md file for more details.
#

import time
import board
import busio
from adafruit_bus_device import spi_device
from circuitpython_dotstarapa102.dotstarapa102 import DotStarAPA102
try:
    from colorcyclers.sine_color_cycler import SineColorCycler
    color_cycler_present = True
except:
    color_cycler_present = False

def sinewave(spi):
    """
    sinewave [wait=200.0] [iterations=300] [width=127] [center=128]
    :param stmt:
    :return:
    """
    wait_ms = 50.0 / 1000.0
    iterations = 300
    width = 127
    center = 128
    pixels = spi.num_pixels

    color_gen = SineColorCycler()
    # In binary RGB format. May require reordering.
    color_list = color_gen.create_color_list(center=center, width=width, colors=pixels)

    colorx = 0
    for i in range(iterations):
        for cx in range(pixels):
            modx = (colorx + cx) % len(color_list)
            spi.set_pixel_color(cx, color_list[modx])
        spi.show()
        colorx = (colorx + 1) % len(color_list)
        time.sleep(wait_ms)
    spi.clear()

if __name__ == "__main__":
    # Try to create an SPI device for the onboard SPI interface
    # We are using the standard SPI pins
    # SCLK = #23 (clock)
    # MOSI = #19 (data out)
    # MISO = #21 (data in, not used here)
    spi_bus = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
    # Wrap the SPI bus in a context manager
    # The baudrate here is believed to be the maximum for an RPi
    # Reference: https://www.corelis.com/education/tutorials/spi-tutorial/
    # Reference: https://learn.adafruit.com/circuitpython-basics-i2c-and-spi/spi-devices
    # See references for a description of polarity and phase.
    # DotStars were found to work with either polarity=1 and phase=0 (mode 2)
    # or polarity=0 and phase=1 (mode 1). They did not work properly with
    # the default values polarity=0 and phase=0 (mode 0) or with 
    # polarity=1 and phase=1 (mode 3)..
    # Looking at the APA102C datasheet indicates that it samples the data
    # line on the trailing edge of the clock pulse. SPI mode 1 and 2 is set up
    # for the device to sample the data line on the falling edge of the
    # clock which seems to be more compatible with the APA102C.
    spi_dev = spi_device.SPIDevice(spi_bus, baudrate=15000000, polarity=1, phase=0)
    # Create DotStar driver from the context manager
    ds = DotStarAPA102(spi_dev, 30)

    try:
        print("Testing dotstar_apa102 package...")
        ds.show()
        input("Enter to start testing")
        
        # Clear pixels
        ds.global_brightness = 4
        print("Brightness:", ds.global_brightness, "/ 31")
        # ds.clear()
        color = 0
        for i in range(ds.num_pixels):
            ds.clear(show=False)
            color = color >> 8
            if not color:
                color = 0xFF0000
            ds.set_pixel_color(i, color)
            ds.show()
            print("px", i, '%0#8x' % color)
            # input("Enter to continue")
            time.sleep(0.5)
        
        # Fill all pixels with red
        print("All red")
        ds.fill_rgb(255, 0, 0)
        ds.show()
        input("Enter to continue")
        
        # Fill all pixels with green
        print("All green")
        ds.fill_rgb(0, 0xFF, 0)
        ds.show()
        input("Enter to continue")

        # Fill last 5 pixels with blue
        print("Last 5 blue")
        ds.fill_rgb(0, 0, 0xFF, start=ds.num_pixels - 5, end=ds.num_pixels)
        ds.show()
        input("Enter to continue")
        
        # Fill first 5 pixels with red
        print("5 red, 20 green, 5 blue")
        ds.fill_rgb(255, 0, 0, start=0, end=5)
        ds.show()
        input("Enter to continue")
        
        # Fetch some pixels
        print("Retrieve some pixel colors")
        print(ds.get_pixel_color(4))
        print(ds.get_pixel_color(29))
        
        if color_cycler_present:
            # Try an algorithm to see what performance looks like
            print("Running sine wave")
            sinewave(ds)
            ds.global_brightness = 8
            print("Brightness:", ds.global_brightness, "/ 31")
            print("Running sine wave")
            sinewave(ds)

    # ctrl-C exit
    except KeyboardInterrupt:
        print("\nQuiting...")

    ds.clear()
    
    # Not really needed, just here for testing
    spi_bus.deinit()
    
    print("Done!")

