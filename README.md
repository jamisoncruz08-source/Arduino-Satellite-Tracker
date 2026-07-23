# Satellite Tracker with Arduino & Python

A real-time satellite tracking system that combines **Python**, **Skyfield**, and an **Arduino Uno** with a **16x2 LCD** and **rotary encoder** to browse and track satellites from space.

The tracker downloads satellite orbital data (TLEs) from CelesTrak, calculates each satellite's current position using Skyfield, and displays the information on an LCD connected to an Arduino.

---

## Features

- Real-time satellite tracking
- Browse satellites by category
- Track custom satellites by NORAD Catalog Number
- Rotary encoder navigation
- 16x2 LCD user interface
- Scrolling text for long satellite names and data
- Latitude, Longitude, and Altitude display
- Automatic TLE caching
- Automatic TLE refresh every 24 hours
- Offline operation using cached TLE files

---

## Hardware

- Arduino Uno R3
- 16x2 LCD Display
- Rotary Encoder (KY-040)
- USB connection to PC
- Breadboard and jumper wires

---

## Software

### Python Libraries

- Skyfield
- PySerial

Install with:

```bash
pip install skyfield pyserial
```

---

## Project Structure

```
SPACE_ARDUINO/
│
├── ARDUINO_DATA.py      # Main Python program
├── LCDSAT.py            # Satellite loading and tracking functions
├── Arduino.ino          # Arduino firmware
├── *.tle                # Cached satellite data
└── README.md
```

---

## How It Works

1. Python downloads or loads cached TLE files.
2. Skyfield calculates each satellite's live position.
3. Python sends information over Serial.
4. Arduino receives the data.
5. The LCD displays:
   - Satellite Name
   - Latitude
   - Longitude
   - Altitude
6. The rotary encoder allows the user to browse menus and select satellites.

---
## TLE Caching

To reduce internet requests and prevent rate limiting, the project automatically caches TLE files locally.

- Cached for 24 hours
- Automatically refreshed when expired
- Works offline using cached data

---

## Custom Satellites

Add satellites using their NORAD Catalog Number.

Example:

```python
SATELLITES = [
    {"name": "ISS", "catnr": 25544},
    {"name": "Hubble", "catnr": 20580},
]
```

---

## Future Improvements

- ESP32 standalone version
- Wi-Fi support
- Battery-powered operation
- GPS integration
- Servo-controlled tellyscope tracking
- Pass prediction
- OLED or TFT display
- Weather satellite image decoding
- 3D printed enclosure

---

## Learning Goals

This project demonstrates:

- Python programming
- Arduino programming
- Serial communication
- Object-oriented programming
- APIs and online data
- Skyfield orbital calculations
- Menu-driven embedded interfaces
- Hardware integration
- Real-time systems

---

## Credits

Satellite orbital data provided by **CelesTrak**

Orbital calculations performed using the **Skyfield** Python library.

---

## License
**** MIT
This project is intended for educational and personal use.