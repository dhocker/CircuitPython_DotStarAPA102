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
    spi_bus = busio.SPI(board.SCLK, board.MOSI, board.MISO)
    # Wrap the SPI bus in a context manager
    # The baudrate here is believed to be the maximum for an RPi
    spi_dev = spi_device.SPIDevice(spi_bus, baudrate=15000000)
    # Create DotStar driver from the context manager
    ds = DotStarAPA102(spi_dev, 30)

    try:
        print("Testing dotstar_apa102 package...")
        # Clear pixels
        ds.global_brightness = 4
        print("Brightness:", ds.global_brightness)
        ds.clear()
        
        # Fill all pixels
        ds.fill_rgb(0xFF, 0, 0)
        # Fill last 5 pixels
        ds.fill_rgb(0, 0, 0xFF, start=ds.num_pixels - 5, end=ds.num_pixels)
        ds.show()
        print("Waiting 5 sec")
        time.sleep(5.0)
        
        # Fill first 5 pixels
        ds.fill_rgb(0, 0xFF, 0, start=0, end=5)
        ds.show()
        print("Waiting 5 sec")
        time.sleep(5.0)
        
        # Fetch some pixels
        print(ds.get_pixel_color(4))
        print(ds.get_pixel_color(29))
        
        if color_cycler_present:
            # Try an algorithm to see what performance looks like
            sinewave(ds)
            ds.global_brightness = 8
            print("Brightness:", ds.global_brightness)
            sinewave(ds)

    # ctrl-C exit
    except KeyboardInterrupt:
        print("\nQuiting...")

    ds.clear()
    
    # Not really needed, just here for testing
    spi_bus.deinit()
    
    print("Done!")

