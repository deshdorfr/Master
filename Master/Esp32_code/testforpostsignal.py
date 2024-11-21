import network
import time
import urequests
import ujson
from machine import Pin

# Replace with your WiFi credentials
SSID = "Desh 4G"
PASSWORD = "12345678"

# Define the API URL
API_URL = "https://deshdeepak007.pythonanywhere.com/api/channels/14/"

# Pin configuration in JSON format
pin_config = {
    5: {"led_pin": 18, "input_pin": 33},  # Red LED
    8: {"led_pin": 19, "input_pin": 32},  # Yellow LED
    10: {"led_pin": 21, "input_pin": 35}  # Green LED
}

# Dictionary to store pin objects
pins = {}

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
            print("Waiting for connection...")
    print("Connected to WiFi!")
    print("IP Address:", wlan.ifconfig()[0])

def get_http_response():
    try:
        response = urequests.get(API_URL)
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to get data from the API, status code:", response.status_code)
            return ""
    except Exception as e:
        print("HTTP request failed:", e)
        return ""
    finally:
        response.close()

def control_leds_from_api(response):
    """
    Controls LEDs based on the API response.
    """
    try:
        data = ujson.loads(response)
        for channel in data:
            pin_id = channel.get("id")  # Use 'id' from API response
            command = channel.get("command")  # Command (On/Off)
            if pin_id in pins:
                led = pins[pin_id]["led"]
                led.value(1 if command == "On" else 0)  # Set LED state
    except ValueError as e:
        print("Error parsing JSON:", e)

def monitor_input_pins():
    """
    Monitors input pins and controls associated LEDs.
    """
    for pin_id, pin_set in pins.items():
        input_pin = pin_set["input"]
        led_pin = pin_set["led"]
        new_state = input_pin.value()
        if pin_set["state"] != new_state:
            print(f"Input pin {pin_id} changed to {new_state}")
            led_pin.value(new_state)  # Update LED state
            pin_set["state"] = new_state  # Update the tracked state

# Initialize pins based on JSON configuration
def initialize_pins():
    for pin_id, config in pin_config.items():
        pins[pin_id] = {
            "led": Pin(config["led_pin"], Pin.OUT),
            "input": Pin(config["input_pin"], Pin.IN, Pin.PULL_DOWN),
            "state": 0  # Track previous state of input pin
        }
    print("Pins initialized:", pins)

# Main code
connect_to_wifi()
initialize_pins()

old_response_api = ""

while True:
    # Handle API response
    response = get_http_response()
    if response and response != old_response_api:
        print(f"API response changed: {response}")
        old_response_api = response
        control_leds_from_api(response)
    
    # Monitor input pins
    monitor_input_pins()

    time.sleep(0.1)  # General loop delay

