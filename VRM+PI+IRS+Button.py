#Project: Door Lock System
#Company: Funktional Automation
#Source Code & Library: Github and DFRobot
#Modified by: Prajeet Bohara
#Date: 06/27/24

from __future__ import print_function
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from DFRobot_DF2301Q import *
import RPi.GPIO as GPIO
from time import sleep

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
relay1_pin = 17
button_pin = 27
relay2_pin = 22

GPIO.setup(relay1_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set up button pin as input with pull-down resistor
GPIO.setup(relay2_pin, GPIO.OUT)

# I2C setup
DF2301Q = DFRobot_DF2301Q_I2C(i2c_addr=DF2301Q_I2C_ADDR, bus=1)

# Variable to track last button state for debounce
last_button_state = GPIO.LOW

def setup():
    # Set voice volume
    DF2301Q.set_volume(4) #parameter 1-9

    # Set mute mode
    DF2301Q.set_mute_mode(0)

    # Set wake-up duration
    DF2301Q.set_wake_time(60)

    # Print the current wake-up duration
    print("wake_time = %u\n" % (DF2301Q.get_wake_time()))

def loop():
    global last_button_state

    # Read current button state
    button_state = GPIO.input(button_pin)

    # Check for button press with debounce
    if button_state == GPIO.HIGH and last_button_state == GPIO.LOW:
        GPIO.output(relay2_pin, GPIO.HIGH)  # Turn relay2 on
        print("Relay 2 turned ON")
        sleep(5)  # Relay stays on for 5 seconds
        GPIO.output(relay2_pin, GPIO.LOW)  # Turn relay2 off
        print("Relay 2 turned OFF")

    # Update last button state for next iteration
    last_button_state = button_state

    # Get the recognized command ID
    CMDID = DF2301Q.get_CMDID()
    if CMDID == 5:  # If command ID is 5, turn the relay on
        GPIO.output(relay1_pin, GPIO.HIGH)  # Turn relay1 on
        print("Relay 1 turned ON")
        sleep(5)  # Door keeps open for 20 seconds
        GPIO.output(relay1_pin, GPIO.LOW)  # Turn relay1 off
        print("Relay 1 turned OFF")
    elif CMDID != 0:  # If command ID is not 0 (no command recognized), print the command ID
        print("CMDID = %u\n" % CMDID)

    sleep(0.1)  # Small delay to avoid high CPU usage

if __name__ == "__main__":
    setup()
    while True:
        loop()

