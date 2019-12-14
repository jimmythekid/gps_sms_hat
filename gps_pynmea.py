# Serial4.py

import serial, pynmea2

port = "/dev/ttyUSB1"  # Output of NMEA String via serial port NOT for AT COMMANDS
# http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/serial.inc.php





def parseGPS(data):
#    print "raw:", data
    if data[0:6] == "$GPGGA":
        msg = pynmea2.parse(data)
        time = msg.timestamp
        lat = decode(msg.lat)
        dirLat = msg.lat_dir
        lon = decode(msg.lon)
        dirLon = msg.lon_dir
        alt = str(msg.altitude) + " " +  str(msg.altitude_units)
        sat = msg.num_sats
        sep = str(msg.geo_sep) + " " + str(msg.geo_sep_units)
        print("Time(UTC): %s -- Latitude: %s(%s) -- Longitude: %s(%s) -- Altitute: %s -- Sep: %s --(%s satellites tracking)" %(time, lat, dirLat, lon, dirLon, alt,sep, sat))

def decode(coord):
    # DDDMM.MMMMM -> DD deg MM.MMMMM min
    v = coord.split(".")
    head = v[0]
    tail =  v[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"

ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
while True:
    data = ser.readline()
    parseGPS(data)
