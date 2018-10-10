from adafruit_bus_device import spi_device

class DotStarAPA102:
    """
    CircuitPython support for APA-102 based Adafruit DotStar LED strips
    on Raspberry Pi.
    ***TODO hardware spec url
    Prefers standard hardware based SPI as found on the Raspberry Pi,
    but should work with any SPIDevice instance.
    Mostly parallels the Adafruit_Dotstar_Pi package.
    Python 3 only.
    
    Methods from the original Adafruit_Dotstar_Pi package
    begin (not needed in this implementation and not impemented)
    clear (resets all pixels)
    setBrightness (implemented as global_brightness property)
    set_pixel_color (was setPixelColor)
    get_pixel_color (was getPixelColor)
    show (transmits all pixels)
    color (deprecated and not implemented, use set_pixel_rgb instead)
    close (not needed and not implemented. Use deinit() from the busio.SPI object)
    
    New Methods
    set_pixel_rgb (alternative for color method)
    set_pixel_brgb
    fill_rgb
    fill_brgb
    
    New Properties
    global_brightness (equivalent of setBrightness)
    num_pixels (numPixels)
    
    ***TODO Usage example
    
    Where reasonable and possible follow Adafruit conventions as documented
    at https://circuitpython.readthedocs.io/en/2.x/docs/design_guide.html 
    """
    def __init__(self, spi, num_px, order='bgr'):
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
        return self.num_px
    
    @property
    def global_brightness(self):
        """
        Sets the brightness for all pixels. Allowable range is 0-31.
        See the APA102 datasheet for a detailed explanation of
        exactly how brightness works.
        """
        return self.global_brightness_value
    
    @global_brightness.setter
    def global_brightness(self, v):
        if v >= 0 and v <= 31:
            self.global_brightness_value = v
        else:
            raise ValueError("Global brightness must be in the range")
        
    def get_pixel_color(self, pixel):
        pxx = self.body_x + (pixel * 4)
        return self.px[pxx + self.red_x], self.px[pxx + self.green_x], self.px[pxx + self.blue_x]
    
    def set_pixel_color(self, pixel, color):
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        # print(r,g,b)
        self.set_pixel_rgb(pixel, r, g, b)
    
    def set_pixel_rgb(self, pixel, r, g, b):
        self.set_pixel_brgb(pixel, self.global_brightness, r, g, b)
    
    def set_pixel_brgb(self, pixel, brightness, r, g, b):
        # print(r,g,b)
        pxx = self.body_x + (pixel * 4)
        self.px[pxx + self.brightness_x] = 0xE0 + (brightness & 0x1F) # brightness
        self.px[pxx + self.red_x] = r
        self.px[pxx + self.green_x] = g
        self.px[pxx + self.blue_x] = b
    
    def fill_rgb(self, r, g, b, start=0, end=None):
        self.fill_brgb(self.global_brightness, r, g, b, start=start, end=end)
    
    def fill_brgb(self, brightness, r, g, b, start=0, end=None):
        if not end:
            end = self.num_pixels
        for i in range(start, end):
            self.set_pixel_brgb(i, brightness, r, g, b)
            
    def show(self):
        # print(self.px)
        with self.spi as spi:
            spi.write(self.px, start=0, end=len(self.px))
        return True
    
    def clear(self, show=True):
        self.fill_brgb(0, 0, 0, 0)
        if show:
            return self.show()
        return True
