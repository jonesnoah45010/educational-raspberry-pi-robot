import asyncio
import threading
from evdev import InputDevice, categorize, ecodes, list_devices


## RUN THIS TO FIGURE OUT KEYBOARD_DEVICE IF YOURS WONT CONNECT
devices = [InputDevice(path) for path in list_devices()]
for dev in devices:
    print(f"{dev.path}: {dev.name}")



keyboard_device="/dev/input/event9" # UPDATE THIS LINE IF YOU ARE USING DIFFERENT DEVICE
current_key = None
key_lock = threading.Lock()



async def monitor_keyboard(device_path=keyboard_device):
    """ Asynchronously monitor keyboard input and update `current_key`. """
    global current_key
    device = InputDevice(device_path)

    print(f"Listening for keyboard events on {device_path}...")

    async for event in device.async_read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            with key_lock:
                if key_event.keystate == 1:  # Key Pressed
                    current_key = key_event.keycode
                elif key_event.keystate == 0:  # Key Released
                    current_key = None
            # print(f"Received key: {current_key}")

def get_current_key():
    """ Returns the latest key pressed or None if no key is currently held. """
    with key_lock:
        return current_key

def start_keyboard_monitor(device_path=keyboard_device):
    """ Starts the keyboard monitoring in a background thread. """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    loop.run_until_complete(monitor_keyboard(device_path))

# Start the monitoring in a separate thread
thread = threading.Thread(target=start_keyboard_monitor, daemon=True)
thread.start()
