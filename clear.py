import time
import sys
sys.path.append('/home/mid/oled-i2c/drive')
import SPI
import SSD1305

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 24
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = SSD1305.SSD1305_128_32(rst=RST)

# Initialize library.
disp.begin()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Clear display
draw.rectangle((0,0,width,height), outline=255, fill=255)
disp.clear()
disp.display()

# Terminate
sys.exit()
