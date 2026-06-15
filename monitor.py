# Created by: Michael Klements
# For Raspberry Pi Desktop Case with OLED Stats Display
# Base on Adafruit Blinka & SSD1306 Libraries
# Installation & Setup Instructions - https://www.the-diy-life.com/add-an-oled-stats-display-to-raspberry-pi-os-bullseye/
import time
import board
import busio
import gpiozero
import os

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess

# Display Parameters
WIDTH = 128
HEIGHT = 32

FONT_SIZE=13
ICON_SIZE=15

# Display Refresh
TIME_SHOW = 1.0
TIME_CLEAR = 10.0

ROW_H=12

class Stats:
    # Define the Reset Pin using gpiozero
    oled_reset = gpiozero.OutputDevice(4, active_high=False)  # GPIO 4 (D4) used for reset

    def clear_screen(self):
        # Reset screen to black for a while to extend lifespan
        self.oled.fill(0)
        self.oled.show()

    def get_data(self):
        # TODO optimise shellouts
        # Shell scripts for system monitoring
        cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
        self.IP = subprocess.check_output(cmd, shell=True)

        #cmd = "top -bn1 | grep load | awk '{printf \"%.2fLA\", $(NF-2)}'"
        cmd = "cat /proc/loadavg |cut -f1 -d ' '"
        self.CPU = subprocess.check_output(cmd, shell=True)

        cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"
        self.MemUsage = subprocess.check_output(cmd, shell=True)

        cmd = "df -h | awk '$NF==\"/\"{printf \"HDD: %d/%dGB %s\", $3,$2,$5}'"
        cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB\", $3,$2}'"
        self.Disk = subprocess.check_output(cmd, shell=True)

        cmd = "cat /sys/class/thermal/thermal_zone*/temp | awk -v CONVFMT='%.1f' '{printf $1/1000}'"
        self.Temperature = subprocess.check_output(cmd, shell=True)

        #print(f"Temp: {self.Temperature}, Memory: {self.MemUsage} | Disk: {self.Disk}, CPU: {self.CPU} | Wifi: {self.IP}")


    def draw_screen(self, x=0):
        self.draw.rectangle((0, 0, WIDTH*2, HEIGHT), outline=0, fill=0) # reset
        self.generate(x)
        self.generate(x+WIDTH)

        # Display image
        self.oled.image(self.image)
        self.oled.show()

    def generate(self, x):
        y = self.top
        self.draw.text((x, y), chr(62609), font=self.icon_font, fill=255) # Icon temp
        self.draw.text((x + 19, y), str(self.Temperature, 'utf-8'), font=self.font, fill=255)

        self.draw.text((x + 65, y), chr(62776), font=self.icon_font, fill=255) # Icon memory
        self.draw.text((x + 87, y), str(self.MemUsage, 'utf-8'), font=self.font, fill=255)

        y += ROW_H
        self.draw.text((x, y), chr(63426), font=self.icon_font, fill=255) # Icon disk
        self.draw.text((x + 19, y), str(self.Disk, 'utf-8'), font=self.font, fill=255)

        self.draw.text((x + 65, y), chr(62171), font=self.icon_font, fill=255) # Icon cpu
        self.draw.text((x + 87, y), str(self.CPU, 'utf-8'), font=self.font, fill=255)

        y += ROW_H
        self.draw.text((x, y), chr(61931), font=self.icon_font, fill=255) # Icon wifi
        self.draw.text((x + 19, y), str(self.IP, 'utf-8'), font=self.font, fill=255)


    def run(self):
        self.setup()
        self.main()

    def setup(self):
        # Use I2C for communication
        i2c = board.I2C()

        # Manually reset the display (high -> low -> high for reset pulse)
        self.oled_reset.on()  # Set the reset pin high
        time.sleep(0.1)  # Delay for a brief moment
        self.oled_reset.off()  # Toggle reset pin low
        time.sleep(0.1)  # Wait for reset
        self.oled_reset.on()  # Turn reset pin back high

        # Create the OLED display object
        self.oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

        # Clear the display
        self.oled.fill(0)
        self.oled.show()

        # Create a blank image and object to draw on
        self.image = Image.new('1', (WIDTH, HEIGHT))
        self.draw = ImageDraw.Draw(self.image)

        padding = -3
        self.top = padding

        # Load default font
        self.font = ImageFont.load_default()
        # Alternatively load a TTF font. Make sure the .ttf font file is in the same directory as the python script!
        self.font = ImageFont.truetype('PixelOperator.ttf', FONT_SIZE)
        self.icon_font = ImageFont.truetype('lineawesome-webfont.ttf', ICON_SIZE)

    def main(self):
        x=0
        while True:
            if x <= -WIDTH:
                x=0
            if x % 10 == 0:
                self.get_data()
            self.draw_screen(x)
            time.sleep(0.1)
            x-=1

            # TODO blank?
            # time.sleep(TIME_SHOW)

stats = Stats()
stats.run()
