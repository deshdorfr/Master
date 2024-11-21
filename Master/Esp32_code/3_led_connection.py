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

def control_leds(response):
    try:
        data = ujson.loads(response)
        for channel in data:
            name = channel.get("name")
            command = channel.get("command")
            # Define LED pins
            led_pin_18 = Pin(18, Pin.OUT)  # Red LED on pin D18
            input_pin_33 = Pin(33, Pin.IN, Pin.PULL_DOWN)
            
            led_pin_19 = Pin(19, Pin.OUT)  # Yellow LED on pin D19
            input_pin_32 = Pin(32, Pin.IN, Pin.PULL_DOWN)
            
            led_pin_21 = Pin(21, Pin.OUT)  # Green LED on pin D21
            input_pin_35 = Pin(35, Pin.IN, Pin.PULL_DOWN)
            
            # Control LEDs based on the response data
            if name == "red LED":
                led_pin_18.value(1 if command == "On" else 0)  # Red LED
            elif name == "yellow LED":
                led_pin_19.value(1 if command == "On" else 0)  # Yellow LED
            elif name == "green LED":
                led_pin_21.value(1 if command == "On" else 0)  # Green LED
    except ValueError as e:
        print("Error parsing JSON:", e)

# Main code
connect_to_wifi()

old_responce_api = {}
while True:
    response = get_http_response()
    if response and response!=old_responce_api:
        old_responce_api = response
        control_leds(response)
    time.sleep(3)  # Wait for 5 seconds before the next check
