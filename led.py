# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
from time import sleep

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D12

# The number of NeoPixels
num_pixels = 22

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB


class LED():
    def __init__(self, num_pixels):
        self.pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.2, auto_write=True, pixel_order=ORDER
        )

    def set_pixel(self, pix):
        # for pix in range(num_pixels)_
        self.pixels.fill([0,0,0])
        self.pixels[pix] = [0,0,200]


if __name__ == '__main__':
    pixel = LED(num_pixels)
    while True:
        for i in range(num_pixels):
            pixel.set_pixel(i, [i*10,(i%2)*125,125])
            print(i)
            sleep(1)



