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

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 0
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
DefaultFont = ImageFont.truetype('/home/mid/oled-i2c/04B_08__.TTF',8)
BigFont = ImageFont.truetype('/home/mid/oled-i2c/04B_08__.TTF',14)

startTime = time.time()
timeout = int(sys.argv[1]) # take the command line argument (timeout in seconds)

# Clear display
draw.rectangle((0,0,width,height), outline=0, fill=0)
disp.clear()
disp.display()

while True:

    cmd = "date +'%d.%m.%y %H:%M' | tr -d '\n'"
    Uptim = subprocess.check_output(cmd, shell = True )

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # /var/log/watchdog.atclient columns:
    # 2020-05-12 09:38:55,+41796691039,Swisscom,4G,61%
    #                   1,           2,       3, 4,  5
    
    # time critical commands first!
    cmd = "date +'%d.%m.%y %H:%M' | tr -d '\n'"
    Date = subprocess.check_output(cmd, shell = True )
    
    cmd = "/home/mid/oled-i2c/get-age.sh | tr -d '\n'"
    LastStkHeartbeat = subprocess.check_output(cmd, shell = True )
    
    #cmd = "awk '{printf(\"%02d:%02d\",($1/60/60%24),($1/60%60))}' /proc/uptime | tr -d '\n'"
    cmd = "awk '{printf(\"%03d %02d\",($1/60/60/24),($1/60/60%24))}' /proc/uptime | tr -d '\n'"
    Uptime = subprocess.check_output(cmd, shell = True )
    
    # now do the rest..
    cmd = "hostname -I | cut -d\' \' -f1 | tr -d '\n'"
    IP = subprocess.check_output(cmd, shell = True )
    
    cmd = "hostname | cut -c 9-11 | tr -d '\n'"
    Hostname = subprocess.check_output(cmd, shell = True )

    cmd = "cut -d ',' -f2 /var/log/watchdog.atclient | sed 's/\+//g' | tr -d '\n'"
    MSISDN = subprocess.check_output(cmd, shell = True )
    
    cmd = "cut -d ',' -f4 /var/log/watchdog.atclient | tr -d '\n'"
    RAT = subprocess.check_output(cmd, shell = True )
    
    cmd = "cut -d ',' -f5 /var/log/watchdog.atclient | tr -d '\n'"
    SignalStrengthPercentage = subprocess.check_output(cmd, shell = True )
    
    cmd = "cut -d ',' -f6 /var/log/watchdog.atclient | tr -d '\n'"
    SignalStrengthIcon = subprocess.check_output(cmd, shell = True )
    
    cmd = "cut -d ',' -f3 /var/log/watchdog.atclient | tr -d '\n'"
    Operator = subprocess.check_output(cmd, shell = True )
    
    cmd = "x=80; y=$(if pgrep -x 'sleep' > /dev/null; then ps -p $(pgrep sleep) -o etimes=; else echo ''; fi | xargs echo); res=$((x - y)); echo "$res"| tr -d '\n'"
    SleepAge = subprocess.check_output(cmd, shell = True )

    # Write two lines of text.
    if "n/a" in LastStkHeartbeat:
        draw.text((x, top), "Waiting ATClient... " + str(SleepAge), font=DefaultFont, fill=255)
    else:
        draw.text((x, top), str(RAT) + " " + str(SignalStrengthPercentage) + " " + str(SignalStrengthIcon) + " AGE " + str(LastStkHeartbeat),  font=DefaultFont, fill=255)
    draw.text((x, top+8), str(MSISDN) + " " + str(Operator), font=DefaultFont, fill=255)
    draw.text((x, top+16), "ID=" + str(Hostname) + "  IP=" + str(IP),  font=DefaultFont, fill=255)
    draw.text((x, top+25), str(Date) + " UP " + str(Uptime),  font=DefaultFont, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)
    
    if (time.time() - startTime) > timeout:
        break
    
# Clear display
draw.rectangle((0,0,width,height), outline=255, fill=255)
disp.clear()
disp.display()

# Terminate
sys.exit()
