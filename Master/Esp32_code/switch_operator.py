import network
import time
import urequests
import ujson
from machine import Pin

# Replace with your WiFi credentials
SSID = "Desh_jio_wifi"
PASSWORD = "desh@123"

# Define the API URL
API_URL = "https://deshdeepak007.pythonanywhere.com/api/channels/14/"

# Pin configuration in JSON format
pin_config = {
    141: {"led_pin": 18, "input_pin": 33},  # Red LED (identification_id 141)
    142: {"led_pin": 19, "input_pin": 32},  # Yellow LED (identification_id 142)
    143: {"led_pin": 21, "input_pin": 35}   # Green LED (identification_id 143)
}

# Dictionary to store pin objects
pins = {}

# Initialize WiFi connection
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)
        start_time = time.ticks_ms()  # Record the start time
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), start_time) > 5000:  # Timeout after 10 seconds
                print("WiFi connection failed. Retrying...")
                return False
            time.sleep(0.5)
    print("Connected to WiFi!")
    print("IP Address:", wlan.ifconfig()[0])
    return True

# Get API response with timeout handling
def get_http_response():
    try:
        response = urequests.get(API_URL, timeout=5)  # 5-second timeout
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to get data from the API, status code:", response.status_code)
            return ""
    except Exception as e:
        print("HTTP request failed:", e)
        return ""
    finally:
        try:
            response.close()
        except:
            pass

# Control LEDs based on the API response
def control_leds_from_api(response):
    try:
        data = ujson.loads(response)
        for channel in data:
            identification_id = channel.get("identification_id")
            command = channel.get("command")  # Command (On/Off)
            if identification_id in pins:
                led = pins[identification_id]["led"]
                led.value(1 if command == "On" else 0)  # Set LED state
    except ValueError as e:
        print("Error parsing JSON:", e)

# Monitor input pins and control associated LEDs
def monitor_input_pins():
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
initialize_pins()
wifi_connected = connect_to_wifi()
old_response_api = ""
last_api_check = time.ticks_ms()

while True:
    # Reconnect WiFi if disconnected
    if not wifi_connected:
        print("Reconnecting to WiFi...")
        wifi_connected = connect_to_wifi()

    # Handle API response every 10 seconds
    if wifi_connected and time.ticks_diff(time.ticks_ms(), last_api_check) > 5000:
        response = get_http_response()
        last_api_check = time.ticks_ms()  # Reset the API check timer
        if response and response != old_response_api:
            print(f"API response changed: {response}")
            old_response_api = response
            control_leds_from_api(response)

    # Monitor input pins continuously
    monitor_input_pins()

    time.sleep(0.1)  # Small delay for loop stability
