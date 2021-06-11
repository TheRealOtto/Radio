#!/usr/bin/env python
# -*- coding: utf-8 -*-  

# This is a script to run Adafruit NeoPixel Diffused with WS2812 RGB controller

HOST = "localhost"
#HOST = "192.168.10.59"
PORT = 4223
UID_LED = "jHd"
UID_RE = 
UID_IO = 


from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_led_strip import BrickletLEDStrip
from tinkerforge.bricklet_io16 import BrickletIO16
from tinkerforge.bricklet_rotary_encoder import BrickletRotaryEncoder

import time

NUM_LED = 11

dim = 1
ind = 0
lng = NUM_LED
drc = 1
spd = 0


r = ([0]*NUM_LED)
g = ([0]*NUM_LED)
b = ([0]*NUM_LED)

        
# Für den gesamten Regenbogen gibt es 6 max/min-Farbwerte (R, G, B) von rot bis violett: 1 0 0 / 1 1 0 / 0 1 0 / 0 1 1 / 0 0 1 / 1 0 1. 
# Der Einfachheit halber wurde der Regenbogen mit 1280 Farbwerten definiert (5 x 256).
# Innerhalb der 5 Bereiche wechselt jeweils eine Farbe von min nach max bzw. von max nach min.

# Rotary Encoder to determine Color Number
# IO_16 to determine LED pattern


def change_colour(dim):
    
    color = rotenc.get_count(false)
    if color > 1280: 
        color = 1280
    
    if rotenc.is_pressed():
        color = 0
        
    if color >= 1 and color < 256:
        r = ([int(255*dim)]*NUM_LED)
        g = ([int(color*dim)]*NUM_LED)
        b = ([0]*NUM_LED)

    elif color >= 256 and color < 512:
        r = ([int((511-color)*dim)]*NUM_LED)
        g = ([int(255*dim)]*NUM_LED)
        b = ([0]*NUM_LED)

    elif color >= 512 and color < 768:
        r = ([0]*NUM_LED)
        g = ([int(255*dim)]*NUM_LED)
        b = ([int((color-512)*dim)]*NUM_LED)

    elif color >= 768 and color < 1024:
        r = ([0]*NUM_LED)
        g = ([int((1023-color)*dim)]*NUM_LED)
        b = ([int(255*dim)]*NUM_LED)

    elif color >= 1024 and color < 1280:
        r = ([int((color-1024)*dim)]*NUM_LED)
        g = ([0]*NUM_LED)
        b = ([int(255*dim)]*NUM_LED)

    time.sleep(0.01)
    return r, g, b;

def pattern(r, g, b, ind, lng):
# pattern: Index (ind), Length (lng), Direction (drc), Speed (spd)
        
    valmask_a = io16.get_port('a')
    valmask_b = io16.get_port('b')
    valmask = valmask_a + valmask_b
    
    if valmask = 1:
        ind = 0
        lng = NUM_LED
        led.set_rgb_values(ind, lng, r, g, b)
        
    elif valmask = 2:
        ind = round(NUM_LED/2)
        lng = NUM_LED-ind
        led.set_rgb_values(ind, lng, r, g, b)
        
    elif valmask = 4:
        ind = NUM_LED
        lng = 1
        led.set_rgb_values(ind, lng, r, g, b)
        

if __name__ == "__main__":
    ipcon = IPConnection()
    ipcon.connect(HOST, PORT)

    led = BrickletLEDStrip(UID_LED, ipcon) 
    rotenc = BrickletRotaryEncoder(UID_RE, ipcon)
    io16 = BrickletIO16(UID_IO, ipcon)
    
    led.set_chip_type(2812)
    
    # led.set_rgb_values(0, NUM_LED, r, g, b)
    
    while True:
        change_colour(dim)
    
        r, g, b = change colour()

        pattern(r, g, b, ind, lng)

        time.sleep(1)
