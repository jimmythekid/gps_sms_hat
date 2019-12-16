# gps_pynmea.py
# -*- coding: utf-8 -*-
import serial, pynmea2, sys

PORT_DATA = "/dev/ttyUSB1"  # Output of NMEA String via serial port NOT for AT COMMANDS
# http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/serial.inc.php
PORT_COMM = "dev/ttyUSB2" # Comm port for talking to and sending AT Commands to HAT


class GPS_Trace:
  def __init__(self, lat, lat_dir, lon, lon_dir, speed, course):
    self.lat = lat
    self.lat_dir = lat_dir
    self.lon = lon
    self.lon_dir = lon_dir
    self.altitude = altitude
    self.altitude_units = altitude_units
    self.sat_count = sat_count
    self.speed = speed
    self.true_course = true_course
    self.mag_var_dir = mag_var_dir
    self.gps_qual = gps_qual



def parseGPS(data):
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
        stid = msg.ref_station_id
        qual = msg.gps_qual
        #print(msg.__dict__.keys())
        print(("Time(UTC): %s -- Latitude: %s(%s) -- Longitude: %s(%s) -- Altitute: %s -- Sep: %s -- (%s satellites tracking) -- Station ID: %s -- GPS Quality: %s" %(time, lat, dirLat, lon, dirLon, alt,sep, sat, stid, qual)))
        print("Map Readable Coordinates:  " +  ('%02d°%02d′%07.4f″  %02d°%02d′%07.4f″' % (msg.latitude, msg.latitude_minutes, msg.latitude_seconds, msg.longitude, msg.longitude_minutes, msg.longitude_seconds)))
    elif data[0:6] == "$GPRMC":
        msg = pynmea2.parse(data)
        time = msg.timestamp
        lat = decode(msg.lat)
        dirLat = msg.lat_dir
        lon = decode(msg.lon)
        dirLon = msg.lon_dir
        speed = msg.spd_over_grnd
        tc = msg.true_course
        mv = msg.mag_variation
        mvd = msg.mag_var_dir
        print(("Land Speed: %s -- True Course: %s -- Mag Var: %s -- Mag Var Direction: %s " %(speed * 0.514444444, tc, mv, mvd)))
        #print("Map Readable Coordinates:  " +  ('%02d°%02d′%07.4f″  %02d°%02d′%07.4f″' % (msg.latitude, msg.latitude_minutes, msg.latitude_seconds, msg.longitude, msg.longitude_minutes, msg.longitude_seconds)))

def decode(coord):
    # DDDMM.MMMMM -> DD deg MM.MMMMM min
    try:
        v = coord.split(".")
        head = v[0]
        tail =  v[1]
        deg = head[0:-2]
        min = head[-2:]
        return deg + " deg " + min + "." + tail + " min"
    except IndexError:
        print("GPS Data Cannot Be Aquired ... ")
        #sys.exit(0)


ser = serial.Serial(PORT_DATA, baudrate = 115200, timeout = 0.5) #9600
#ser_com = serial.Serial(PORT_COMM, baudrate = 115200, timeout = 0.5)
#ser_com.write("AT+CGPS")

while True:
    data = ser.readline()
    parseGPS(data)
