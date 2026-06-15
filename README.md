# Raspberry Pi OLED status screen

A fairly simple python script to drive a 0.91" 128x32 I2C OLED (SSD1306 driver) screen as a system status screen. Primarily built for a raspberry pi

Features:
* scrolling to hopefully reduce oled burn-in
* icon display
* system stats:
    * temperature
    * memory usage
    * disk usage
    * system load
    * ip address

Very strongly inspired by https://github.com/FlantasticDan/oled-status

## Wiring

TBC

## Installation
run install.sh, or read it and do all the steps by hand (does invoke sudo for installing).
I wanted it running as a systemd service, so it will install that too.


### See also

https://github.com/mklements/OLED_Stats was also of note during discovery
