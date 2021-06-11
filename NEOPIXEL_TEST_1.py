#!/usr/bin/env python
# -*- coding: utf-8 -*-  

# This is a script to run Adafruit NeoPixel Diffused with WS2812 RGB controller

HOST = "localhost"
#HOST = "192.168.10.59"
PORT = 4223
UID_LED = "jHd"
UID_AIN = "9zb"
UID_ILU = "uLh"

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_led_strip import LEDStrip
from tinkerforge.bricklet_ambient_light_v2 import BrickletAmbientLightV2
from tinkerforge.bricklet_analog_in import BrickletAnalogIn
import time


NUM_LED = 11
dim = 0.5

r = ([0]*16)
g = ([0]*16)
b = ([0]*16)

        
# Für den gesamten Regenbogen gibt es 6 max/min-Farbwerte (R, G, B) von rot bis violett: 1 0 0 / 1 1 0 / 0 1 0 / 0 1 1 / 0 0 1 / 1 0 1. 
# Der Einfachheit halber wurde der Regenbogen mit 1280 Farbwerten definiert (5 x 256).
# Innerhalb der 5 Bereiche wechselt jeweils eine Farbe von min nach max bzw. von max nach min.


def change_colour(number, dim):

    illu = al.get_illuminance()/100
    print(str(illu))
    dim = illu/3000
    if dim > 1:
        dim = 1
    print(str(dim))
        
    if number >= 1 and number < 256:
        r = ([int(255*dim)]*16)
        g = ([int(number*dim)]*16)
        b = ([0]*16)
        
        ind = 0
        lng = NUM_LED
        led.set_rgb_values(ind, lng, r, g, b)

    elif number >= 256 and number < 512:
        r = ([int((511-number)*dim)]*16)
        g = ([int(255*dim)]*16)
        b = ([0]*16)
        
        ind = 0
        lng = NUM_LED//2
        led.set_rgb_values(ind, lng, r, g, b)

        ind = round(NUM_LED/2)
        lng = NUM_LED-ind
        led.set_rgb_values(ind, lng, r, g, b)

    elif number >= 512 and number < 768:
        r = ([0]*16)
        g = ([int(255*dim)]*16)
        b = ([int((number-512)*dim)]*16)
        
        ind = 0
        lng = NUM_LED//2
        led.set_rgb_values(ind, lng, r, g, b)

        ind = round(NUM_LED/2)
        lng = NUM_LED-ind
        led.set_rgb_values(ind, lng, r, g, b)

    elif number >= 768 and number < 1024:
        r = ([0]*16)
        g = ([int((1023-number)*dim)]*16)
        b = ([int(255*dim)]*16)
        
        ind = 0
        lng = NUM_LED//2
        led.set_rgb_values(ind, lng, r, g, b)

        ind = round(NUM_LED/2)
        lng = NUM_LED-ind
        led.set_rgb_values(ind, lng, r, g, b)

    elif number >= 1024 and number < 1280:
        r = ([int((number-1024)*dim)]*16)
        g = ([0]*16)
        b = ([int(255*dim)]*16)

        ind = 0
        lng = NUM_LED//2
        led.set_rgb_values(ind, lng, r, g, b)

        ind = round(NUM_LED/2)
        lng = NUM_LED-ind
        led.set_rgb_values(ind, lng, r, g, b)

    time.sleep(0.01)

if __name__ == "__main__":
    ipcon = IPConnection()
    ipcon.connect(HOST, PORT)

    led = LEDStrip(UID_LED, ipcon) 
    ai = BrickletAnalogIn(UID_AIN, ipcon)
    al = BrickletAmbientLightV2(UID_ILU, ipcon)
    
    led.set_chip_type(2812)

    led.set_rgb_values(0, NUM_LED, r, g, b)

    time.sleep(1)

for number in range(1280):
    change_colour(number, dim)

led.set_rgb_values(0, NUM_LED, r, g, b)
