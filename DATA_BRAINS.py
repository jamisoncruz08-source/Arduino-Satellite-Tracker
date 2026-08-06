
from skyfield.api import load, wgs84
import time
import os

ts = load.timescale()


def load_satellite_by_catnr(catnr):
    url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={catnr}&FORMAT=tle"

    filename = f"{catnr}.tle"

    reload_file = True

    if os.path.exists(filename):
        age = time.time() - os.path.getmtime(filename)

        if age < 24 * 60 * 60:
            reload_file = False

    satellites = load.tle_file(
        url,
        filename=filename,
        reload=reload_file
    )

    if len(satellites) == 0:
        raise ValueError(f"No satellite found for CATNR {catnr}")

    return satellites[0]
def load_satellite_group(group_name):
    url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group_name}&FORMAT=tle"

    filename = f"{group_name}.tle"

    # Assume we need to download
    reload_file = True

    # If the file already exists, check its age
    if os.path.exists(filename):
        age = time.time() - os.path.getmtime(filename)

        # Use the cached file if it's less than 24 hours old
        if age < 24 * 60 * 60:
            reload_file = False

    satellites = load.tle_file(
        url,
        filename=filename,
        reload=reload_file
    )

    if len(satellites) == 0:
        raise ValueError(f"No satellites found for group {group_name}")

    return satellites
def get_satellite_position(satellite):
    t = ts.now()

    observer = wgs84.latlon(38.8339, -104.8214)

    difference = satellite - observer
    topocentric = difference.at(t)

    alt, az, distance = topocentric.altaz()

    geocentric = satellite.at(t)
    subpoint = wgs84.subpoint(geocentric)

    return {
        "name": satellite.name,
        "latitude": subpoint.latitude.degrees,
        "longitude": subpoint.longitude.degrees,
        "altitude": subpoint.elevation.km,
        "azimuth": az.degrees,
        "elevation": alt.degrees
    }
def print_mars_position():
    t = ts.now()

    planets = load("de421.bsp")
    earth, mars = planets["earth"], planets["mars"]

    astrometric = earth.at(t).observe(mars)
    ra, dec, distance = astrometric.radec()

    print(
        f"Mars | "
        f"RA: {ra}, "
        f"Dec: {dec}, "
        f"Distance: {distance}"
    )

if __name__ == "__main__":

    SATELLITES = [
        {"name": "ISS", "catnr": 25544},
        {"name": "Hubble", "catnr": 20580},
        {"name": "Tiangong", "catnr": 48274},
        {"name": "COSMOS 2251", "catnr": 22675},
        {"name": "Iridium 33", "catnr": 24946},
        {"name": "UFO 2 USA 95", "catnr": 22787},
        {"name": "Terra", "catnr": 25994},
        {"name": "Chandra", "catnr": 25867},  # CXH
        {"name": "WSF-M, 59481", "catnr": 59481},
    ]
    tracked_objects =[]

    for sat in SATELLITES:
        tracked_objects.append(load_satellite_by_catnr(sat["catnr"]))


    stations = load_satellite_group("stations")
    print(f"Loaded {len(stations)} stations")

    print_mars_position()
    gps = load_satellite_group("gps-ops") # GPS
    while True:
        print("----- update -----")

        for satellite in tracked_objects:
           info = get_satellite_position(satellite)

           print(
               f"{info['name']} | "
               f"Lat: {info['latitude']:.2f}, "
               f"Lon: {info['longitude']:.2f}, "
               f"Alt: {info['altitude']:.1f} km"
           )
        #print("----- Starlink sample -----")

        #for satellite in stations[:10]:
            #print_satellite_position(satellite)

        print("----GPS sample ------")
        for satellite in gps[:10]:
            get_satellite_position(satellite)

        time.sleep(10000)
