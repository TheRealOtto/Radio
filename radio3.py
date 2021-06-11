#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a script to run Adafruit 'NeoPixel Diffused' with WS2812 RGB controller

HOST = "localhost"
PORT = 4223
UID_LED = "jHd"
UID_RE = "kL6"
UID_IO = "7zY"


from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_led_strip import BrickletLEDStrip
from tinkerforge.bricklet_io16 import BrickletIO16
from tinkerforge.bricklet_rotary_encoder import BrickletRotaryEncoder

from time import strftime, sleep

NUM_LED = 11

dim = 1          # Brightness
ind = 0          # Index
lng = NUM_LED    # Zahl leuchtender LED
drc = 1          # Laufrichtung
spd = 0          # Laufgeschwindigkeit
clr_fctr = 9     # color factor (to come into range 0 - 1280)

r = ([0]*16)
g = ([0]*16)
b = ([0]*16)


# Für den gesamten Regenbogen gibt es 6 max/min-Farbwerte (R, G, B) von rot bis violett: 1 0 0 / 1 1 0 / 0 1 0 / 0 1 1 / 0 0 1 / 1 0 1. 
# Der Einfachheit halber wurde der Regenbogen mit 1280 Farbwerten definiert (5 x 256).
# Innerhalb der 5 Bereiche wechselt jeweils eine Farbe von min nach max bzw. von max nach min.

# Time of day to determine Color Number
# IO_16 to determine LED pattern


def change_colour(dim):

    hour = int(strftime("%H"))
    minute = int(strftime("%M"))
    tme = hour*100+int(minute*1.666666)

    if tme < 1200:
        color = int((tme/100)**2*clr_fctr)
    elif tme >= 1200:
        color = int((24 - (tme/100))**2*clr_fctr)

    if color > 1279:
        color = 1279
    if color < 1:
        color = 1

    if rotenc.is_pressed():
        color = 1

    if color >= 1 and color < 256:
        r = ([int(255*dim)]*16)
        g = ([int(color*dim)]*16)
        b = ([0]*16)

    elif color >= 256 and color < 512:
        r = ([int((511-color)*dim)]*16)
        g = ([int(255*dim)]*16)
        b = ([0]*16)

    elif color >= 512 and color < 768:
        r = ([0]*16)
        g = ([int(255*dim)]*16)
        b = ([int((color-512)*dim)]*16)

    elif color >= 768 and color < 1024:
        r = ([0]*16)
        g = ([int((1023-color)*dim)]*16)
        b = ([int(255*dim)]*16)

    elif color >= 1024 and color < 1280:
        r = ([int((color-1024)*dim)]*16)
        g = ([0]*16)
        b = ([int(255*dim)]*16)

    led.set_rgb_values(ind, lng, r, g, b)

    return r, g, b;


def brightness():
    global dim

    valmask_a = io16.get_port('a')
    valmask_b = io16.get_port('b')

    # selector switch has 12 positions
    factor = (12**-1)

    valmask = valmask_a + valmask_b
    if valmask_a == 255:
        valmask = valmask_b

    if valmask == 509:
        step = 12
    elif valmask == 508:
        step = 11
    elif valmask == 506:
        step = 10
    elif valmask == 502:
        step = 9
    elif valmask == 494:
        step = 8
    elif valmask == 478:
        step = 7
    elif valmask == 446:
        step = 6
    elif valmask == 382:
        step = 5
    elif valmask == 254:
        step = 4
    elif valmask == 253:
        step = 3
    elif valmask == 251:
        step = 2
    elif valmask == 247:
        step = 1

    # dim range is 0 .. 1. Squaring lets the value rise as a parabolic curve.
    dim = (step*factor)**2

    return dim

if __name__ == "__main__":
    ipcon = IPConnection()
    ipcon.connect(HOST, PORT)

    led = BrickletLEDStrip(UID_LED, ipcon)
    rotenc = BrickletRotaryEncoder(UID_RE, ipcon)
    io16 = BrickletIO16(UID_IO, ipcon)

    led.set_chip_type(2812)
    led.set_channel_mapping(6)
    led.set_rgb_values(0, NUM_LED, r, g, b)

    sleep(5)

    while True:
        dim = brightness()

        change_colour(dim)
        r, g, b = change_colour(dim)
        brightness()

        sleep(10)
