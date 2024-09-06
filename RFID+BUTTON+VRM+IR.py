from __future__ import print_function
import sys
import os
import threading
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from DFRobot_DF2301Q import *
import RPi.GPIO as GPIO
from time import sleep
from mfrc522 import SimpleMFRC522

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
relay1_pin = 17
button_pin = 27
relay2_pin = 22
rfid_gpio_pin = 23  # GPIO pin for RFID control

GPIO.setup(relay1_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set up button pin as input with pull-down resistor
GPIO.setup(relay2_pin, GPIO.OUT)
GPIO.setup(rfid_gpio_pin, GPIO.OUT)
GPIO.output(rfid_gpio_pin, GPIO.LOW)  # Ensure the RFID GPIO pin starts low (off)

# Initialize the RFID reader
reader = SimpleMFRC522()

# I2C setup
DF2301Q = DFRobot_DF2301Q_I2C(i2c_addr=DF2301Q_I2C_ADDR, bus=1)

# Variable to track last button state for debounce
last_button_state = GPIO.LOW

def setup():
    # Set voice volume
    DF2301Q.set_volume(4)

    # Set mute mode
    DF2301Q.set_mute_mode(0)

    # Set wake-up duration
    DF2301Q.set_wake_time(10)

    # Print the current wake-up duration
    print("wake_time = %u\n" % (DF2301Q.get_wake_time()))

def handle_button():
    global last_button_state

    while True:
        try:
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
            sleep(0.1)  # Small delay to avoid high CPU usage
        except Exception as e:
            print("Error in handle_button:", e)
        
def handle_voice():
    while True:
        try:
            # Get the recognized command ID
            CMDID = DF2301Q.get_CMDID()
            if CMDID == 5:  # If command ID is 5, turn the relay on
                GPIO.output(relay1_pin, GPIO.HIGH)  # Turn relay1 on
                print("Relay 1 turned ON")
                sleep(5)  # Door keeps open for 5 seconds
                GPIO.output(relay1_pin, GPIO.LOW)  # Turn relay1 off
                print("Relay 1 turned OFF")
            elif CMDID != 0:  # If command ID is not 0 (no command recognized), print the command ID
                print("CMDID = %u\n" % CMDID)
            sleep(0.1)  # Small delay to avoid high CPU usage
        except Exception as e:
            print("Error in handle_voice:", e)
            
def handle_rfid():
    while True:
        try:
            # RFID reader functionality
            id, text = reader.read()

            # Control GPIO based on tag ID
            if id == 527893793396:
                GPIO.output(rfid_gpio_pin, GPIO.HIGH)  # Turn GPIO pin on
                print("RFID GPIO Pin {} turned ON".format(rfid_gpio_pin))
                sleep(5)  # Wait for 5 seconds
                GPIO.output(rfid_gpio_pin, GPIO.LOW)   # Turn GPIO pin off
                print("RFID GPIO Pin {} turned OFF".format(rfid_gpio_pin))
            else:
                GPIO.output(rfid_gpio_pin, GPIO.LOW)   # Ensure GPIO pin is off if ID does not match
        except Exception as e:
            print("Error in handle_rfid:", e)
        sleep(0.5)  # Small delay to avoid high CPU usage and reduce interference

if __name__ == "__main__":
    setup()

    # Create and start threads
    button_thread = threading.Thread(target=handle_button)
    voice_thread = threading.Thread(target=handle_voice)
    rfid_thread = threading.Thread(target=handle_rfid)

    button_thread.start()
    voice_thread.start()
    rfid_thread.start()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("\nCtrl+C captured, ending program.")
        GPIO.cleanup()  # Clean up GPIO settings on program exit
        button_thread.join()
        voice_thread.join()
        rfid_thread.join()
