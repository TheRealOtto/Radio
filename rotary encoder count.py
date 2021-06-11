#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "XYZ" # Change XYZ to the UID of your Rotary Encoder Bricklet 2.0

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_rotary_encoder_v2 import BrickletRotaryEncoder

UPPER_LIMIT = 10
LOWER_LIMIT = -10

last_count = None
limited_count = None

# Callback function for count callback
def cb_count(count):
    global last_count
    global limited_count

    if last_count == None:
        last_count = count

    if limited_count == None:
        limited_count = count

    limited_count += count - last_count
    last_count = count

    if limited_count < LOWER_LIMIT:
        limited_count = LOWER_LIMIT
    elif limited_count > UPPER_LIMIT:
        limited_count = UPPER_LIMIT
    
    print("Count: " + str(count))
    print("Limited Count: " + str(limited_count))
    print("")

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    re = BrickletRotaryEncoder(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register count callback to function cb_count
    re.register_callback(re.CALLBACK_COUNT, cb_count)

    # Set period for count callback to 50ms without a threshold
    re.set_count_callback_configuration(50, True, "x", 0, 0)

    input("Press key to exit\n") # Use raw_input() in Python 2
    ipcon.disconnect()
