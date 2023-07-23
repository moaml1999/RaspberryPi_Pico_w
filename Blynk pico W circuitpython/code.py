"""
DESCRIPTION:
This example code will uses Robo Pico and Raspberry Pi Pico W to :
1) Send value to Blnyk App
2) Read data from Blynk App
3) Control Virtual LED on Blynk App using Button 20 on Robo Pico

AUTHOR  : Cytron Technologies Sdn Bhd
WEBSITE  : www.cytron.io
EMAIL    : support@cytron.io

REFERENCE:
Code adapted from 2023 peppe80, Personal IoT App with Blynk and Raspberry PI:
https://peppe8o.com/personal-iot-with-blynk-on-raspberry-pi/
"""

import os
import ipaddress
import wifi
import socketpool
import time
import microcontroller
import board
import digitalio
import simpleio
import adafruit_requests
import ssl
import random


# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("All secret keys are kept in secrets.py, please add them there!")
    raise

# Get wifi and blynk token details from a settings.toml file
blynkToken = "gAY4Ain2FXXpQq-XDa1dQGvwhEnof0yZ"


# Initialize LED and button.
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


# Write API
def write(token,pin,value):
        api_url = "https://blynk.cloud/external/api/update?token="+token+"&"+pin+"="+value
        response = requests.get(api_url)
        if "200" in str(response):
                print("Value successfully updated")
        else:
                print("Could not find the device token or wrong pin format")
# Read API
def read(token,pin):
        api_url = "https://blynk.cloud/external/api/get?token="+token+"&"+pin
        response = requests.get(api_url)
        return response.content.decode()

# Connect to Wi-Fi AP

print(f"Initializing...")
while not wifi.radio.ipv4_address or "0.0.0.0" in repr(wifi.radio.ipv4_address):
    print(f"Connecting to WiFi...")
    wifi.radio.connect(ssid=secrets["ssid"], password=secrets["password"])
print("IP Address: {}".format(wifi.radio.ipv4_address))

pool = socketpool.SocketPool(wifi.radio)
print("Connecting to WiFi '{}' ...\n".format(secrets["ssid"]), end="")
requests = adafruit_requests.Session(pool, ssl.create_default_context())


while True:
    try:
        while not wifi.radio.ipv4_address or "0.0.0.0" in repr(wifi.radio.ipv4_address):
            print(f"Reconnecting to WiFi...")
            wifi.radio.connect(ssid=secrets["ssid"], password=secrets["password"])

        # Write Blynk virtual pin V0
        # V0 can be assigned to Virtual Pin Widget on Blynk App
        # Send random number
        valV0 = str(round(random.uniform(0,250),2))
        write(blynkToken,"V0",valV0)
        print(f"Write to V0: {valV0}")

        # Read Blynk virtual pin V1
        # V1 can be assigned to Button Widget on Blynk App
        button = read(blynkToken,"V1")
        print(f"Read V1: {button}")
        if (button == "1"):
            led.value = True
        else:
            led.value = False

        # Write Blynk virtual pin V2
        # V2 can be assigned to LED Widget on Blynk App
        # If the button 20 pressed it will update on the LED on Blynk App

        print("")
        time.sleep(2)

    except OSError as e:
        print("Failed!\n", e)
        microcontroller.reset()

