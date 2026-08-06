# Import the pySerial library so Python can communicate with the Arduino
import serial,time
from LCDSAT import ( load_satellite_by_catnr, load_satellite_group, get_satellite_position )
# Globals
current_sat = 0      # Browsing with joystick
GROUP_MENU = "GROUP_MENU"
SATELLITE_MENU = "SATELLITE_MENU"
TRACKING = "TRACKING"
PORT = "COM8"
state = GROUP_MENU
def connect_arduino(port):
    arduino = serial.Serial(port, 9600)
    time.sleep(2)
    return arduino
arduino = connect_arduino(PORT)

# A custom List of Satellites
SATELLITES = [
    {"name": "ISS", "catnr": 25544},
    {"name": "Hubble", "catnr": 20580},
    {"name": "Tiangong", "catnr": 48274},
    {"name": "COSMOS 2251", "catnr": 22675},
    {"name": "Iridium 33", "catnr": 24946},
    {"name": "UFO 2 USA 95", "catnr": 22787},
    {"name": "Terra", "catnr": 25994},
    {"name": "Chandra", "catnr": 25867},#CXH
    {"name": "WSF-M, 59481", "catnr": 59481},
    {"name": "NOAA 19", "catnr": 33591}
]

GROUPS = [
    "Stations",
    "Weather",
    "Science",
    "Military",
    "amateur",
    "science"
]

current_group = 0
def load_satellites():
    group = GROUPS[current_group]

    # Load from cache if we've already downloaded this group
    if group in satellite_cache:
        print(f"Using cached group: {group}")
        tracked_objects = satellite_cache[group].copy()

    else:
        print(f"Loading group: {group}")

        tracked_objects = load_satellite_group(group)

        for sat in SATELLITES:
            print(f"Loading {sat['name']} ({sat['catnr']})...")
            tracked_objects.append(load_satellite_by_catnr(sat["catnr"]))

        tracked_objects.append("back")

        # Save a copy in the cache
        satellite_cache[group] = tracked_objects.copy()

    return tracked_objects

satellite = None
try:
    tracked_objects = load_satellites()
except Exception as e:
    print(e)
    tracked_objects = ["back"]
def handle_group_menu(command):
    global current_group
    global current_sat
    global tracked_objects
    global state

    if command == "LEFT":
        current_group = (current_group - 1) % len(GROUPS)

    elif command == "RIGHT":
        current_group = (current_group + 1) % len(GROUPS)

    elif command == "SELECT":
        tracked_objects = load_satellites()
        current_sat = 0
        state = SATELLITE_MENU


def handle_satellite_menu(command):
    global current_sat
    global satellite
    global state

    if command == "LEFT":
        current_sat = (current_sat - 1) % len(tracked_objects)

    elif command == "RIGHT":
        current_sat = (current_sat + 1) % len(tracked_objects)



    elif command == "SELECT":

        if tracked_objects[current_sat] == "back":
            current_sat = 0
            state = GROUP_MENU


        else:

            satellite = tracked_objects[current_sat]

            state = TRACKING

def handle_tracking(command):
    global state
    if command == "SELECT":
        state = SATELLITE_MENU

def update_group_menu():
    return f"GROUP,{GROUPS[current_group]}\n"

def update_tracking():
    info = get_satellite_position(satellite)

    return (
        f"{info['name']},"
        f"{info['latitude']:.2f},"
        f"{info['longitude']:.2f},"
        f"{info['altitude']:.2f},"
        f"{info['azimuth']:.1f},"
        f"{info['elevation']:.1f}\n"
    )

def update_satellite_menu():
    if tracked_objects[current_sat] == "back":
        return  "MENU,Back\n"
    return f"MENU,{tracked_objects[current_sat].name}\n"


def read_joystick():
    if arduino.in_waiting:
        return arduino.readline().decode().strip()

    return None
# Main Program Loop
last_message = ""

while True:
    # Check joystick input
    command = read_joystick()

    if command:

        if state == GROUP_MENU:
            handle_group_menu(command)

        elif state == SATELLITE_MENU:
            handle_satellite_menu(command)

        elif state == TRACKING:
            handle_tracking(command)

    if state == GROUP_MENU:
        message = update_group_menu()

    elif state == SATELLITE_MENU:
        message = update_satellite_menu()

    elif state == TRACKING:
        message = update_tracking()

    # Menus only send when they change
    if state != TRACKING:
        if message != last_message:
            arduino.write(message.encode())
            print(message)
            last_message = message

    # Tracking updates continuously
    else:
        if time.time() - last_update >= 10:
            arduino.write(message.encode())
            print(message)
            last_update = time.time()

    time.sleep(0.1)