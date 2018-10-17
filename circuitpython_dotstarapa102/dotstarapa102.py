# -*- coding: utf-8 -*-
#
# LED interface driver for APA102/DotStar strips/strings
# Copyright © 2018  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE.md file for more details.
#

from adafruit_bus_device import spi_device

class DotStarAPA102:
    """
    CircuitPython support for APA-102 based Adafruit DotStar LED strips
    on Raspberry Pi (most all variations including Pi Zero and Pi Zero W).

    Prefers standard hardware based SPI as found on the Raspberry Pi,
    but should work with any SPIDevice instance.
    Mostly parallels the Adafruit_Dotstar_Pi package. For circuit diagram see:
    https://github.com/dhocker/CircuitPython_DotStarAPA102

    **Python 3 only.**
    
    Methods from the original Adafruit_Dotstar_Pi package

    * begin (not needed in this implementation and not impemented)
    * clear (resets all pixels)
    * setBrightness (implemented as global_brightness property)
    * set_pixel_color (was setPixelColor)
    * get_pixel_color (was getPixelColor)
    * show (transmits all pixels)
    * color (deprecated and not implemented, use set_pixel_rgb instead)
    * close (not needed and not implemented. Use deinit() from the busio.SPI object)
    
    New Methods

    * set_pixel_rgb (alternative for color method)
    * set_pixel_brgb
    * fill_rgb
    * fill_brgb
    
    New Properties

    * global_brightness (equivalent of setBrightness)
    * num_pixels (numPixels)

    Where reasonable and possible follow Adafruit conventions as documented
    at https://circuitpython.readthedocs.io/en/2.x/docs/design_guide.html 
    """
    def __init__(self, spi, num_px, order='bgr'):
        """
        Initialize an instance of DotStarAPA102

        :param spi: An SPIDevice instance that defines the SPI bus to be used.
        :param num_px: Number of pixels in the SotStar string.
        :param order: Order of the color components.
        """
        # The spi object must be of the correct type
        if not isinstance(spi, spi_device.SPIDevice):
            raise ValueError("spi must be <class 'adafruit_bus_device.spi_device.SPIDevice'>")
        
        self.spi = spi
        self.num_px = num_px
        # Color use determined by observation
        # These are indexes in LED frame (of 4 bytes)
        self.brightness_x = 0 # low order 5 bits, global
        # Implement color order
        self.blue_x = order.find("b") + 1 # blue
        self.green_x = order.find("g") + 1 # green
        self.red_x = order.find("r") + 1 # red
        self.global_brightness_value = 31
       
        # <Start frame> + <LED data> + <end frame>
        # Start frame = 4 bytes all 0's
        # LED data = 4 * pixels bytes
        # End frame = 4 bytes all 1's
        # Others have reported that the end frame is not necessary.
        # This implmentation follows the APA102C specification and
        # includes the end frame.
        self.start_x = 0
        self.body_x = self.start_x + 4
        self.end_x = self.body_x + (4 * self.num_px)
        # Create trasmit buffer
        self.px = bytearray(4 + (4 * self.num_px) + 4)
        # print("Pixel buffer length:", len(self.px))
        # Start and end frames
        for i in range(4):
            self.px[i] = 0
            self.px[i + self.end_x] = 0xFF
        # Global brightness
        for i in range(self.body_x, self.body_x + (self.num_px * 4), 4):
            self.px[i] = 0xE0
    
    @property
    def num_pixels(self):
        """
        Returns the number of pixels in the current DotStar string.

        :return: Number of pixels in string.
        """
        return self.num_px
    
    @property
    def global_brightness(self):
        """
        Sets/returns the brightness for all pixels. Allowable range is 0-31.
        See the APA102 datasheet for a detailed explanation of
        exactly how brightness works.

        :getter: Returns the current global brightness value.
        :setter: Sets the global brightness value.
        """
        return self.global_brightness_value
    
    @global_brightness.setter
    def global_brightness(self, v):
        """
        Setter

        :param v: Brightness value, 0-31.
        :return:
        """
        if v >= 0 and v <= 31:
            self.global_brightness_value = v
        else:
            raise ValueError("Global brightness must be in the range")
        
    def get_pixel_color(self, pixel):
        """
        Returns an RGB 3-tuple representing the color of a given pixel.

        :param pixel: Pixel whose color is to be returned, 0 to num_pixels - 1.
        :return: RGB 3-tuple (r, g, b)
        """
        if pixel >= self.num_pixels:
            raise ValueError("Pixel value out of range")
        pxx = self.body_x + (pixel * 4)
        return self.px[pxx + self.red_x], self.px[pxx + self.green_x], self.px[pxx + self.blue_x]
    
    def set_pixel_color(self, pixel, color):
        """
        Set the color of a given pixel.

        :param pixel: Pixel whose color is to be returned, 0 to num_pixels - 1.
        :param color: A color value in the form 0xRRGGBB.
        :return: None.
        """
        if pixel >= self.num_pixels:
            raise ValueError("Pixel value out of range")
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        # print(r,g,b)
        self.set_pixel_rgb(pixel, r, g, b)
    
    def set_pixel_rgb(self, pixel, r, g, b):
        """
        Set the color of a given pixel.

        :param pixel: Pixel whose color is to be returned, 0 to num_pixels - 1.
        :param r: Red value, 0-255.
        :param g: Green value, 0-255.
        :param b: Blue value, 0-255.
        :return: None.
        """
        if pixel >= self.num_pixels:
            raise ValueError("Pixel value out of range")
        self.set_pixel_brgb(pixel, self.global_brightness, r, g, b)
    
    def set_pixel_brgb(self, pixel, brightness, r, g, b):
        """
        Set the brightness and color of a given pixel. The brightness
        value overrides the global brightness setting.

        :param pixel: Pixel whose color is to be returned, 0 to num_pixels - 1.
        :param brightness: Brightness value for the pixel, 0-31.
        :param r: Red value, 0-255.
        :param g: Green value, 0-255.
        :param b: Blue value, 0-255.
        :return: None.
        """
        if pixel >= self.num_pixels:
            raise ValueError("Pixel value out of range")
        # print(r,g,b)
        pxx = self.body_x + (pixel * 4)
        self.px[pxx + self.brightness_x] = 0xE0 + (brightness & 0x1F) # brightness
        self.px[pxx + self.red_x] = r
        self.px[pxx + self.green_x] = g
        self.px[pxx + self.blue_x] = b
    
    def fill_rgb(self, r, g, b, start=0, end=None):
        """
        Fill a slice of pixels with a color. The default start/end parameters
        define the entire set of pixels.

        :param r: Red value, 0-255.
        :param g: Green value, 0-255.
        :param b: Blue value, 0-255.
        :param start: Starting pixel index, 0 to num_pixels - 1.
        :param end: Ending pixel index. 1 to num_pixels. Works just like range(). A value of None means num_pixels.
        :return: None.
        """
        self.fill_brgb(self.global_brightness, r, g, b, start=start, end=end)
    
    def fill_brgb(self, brightness, r, g, b, start=0, end=None):
        """
        Fill a slice of pixels with a brightness and color. The default start/end parameters
        define the entire set of pixels.

        :param brightness: Brightness value for the pixel, 0-31.
        :param r: Red value, 0-255.
        :param g: Green value, 0-255.
        :param b: Blue value, 0-255.
        :param start: Starting pixel index, 0 to num_pixels - 1.
        :param end: Ending pixel index. 1 to num_pixels. Works just like range(). A value of None means num_pixels.
        :return: None.
        """
        if not end:
            end = self.num_pixels
        for i in range(start, end):
            self.set_pixel_brgb(i, brightness, r, g, b)
            
    def show(self):
        """
        Transmit all pixels to the DotStar string.

        :return: True if successful.
        """
        # print(self.px)
        with self.spi as spi:
            spi.write(self.px, start=0, end=len(self.px))
        return True
    
    def clear(self, show=True):
        """
        Set all pixels to off (brightness = 0, color = 0x000000).

        :param show: If True, transmit cleared pixels.
        :return: True if successful.
        """
        self.fill_brgb(self.global_brightness, 0, 0, 0)
        if show:
            return self.show()
        return True
