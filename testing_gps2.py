import serial, time, pynmea2, re

def serial_def():
    ser = serial.Serial()
    ser.port = "/dev/ttyUSB2"
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    ser.parity = serial.PARITY_NONE #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    ser.timeout = 2              #timeout block read
    ser.xonxoff = False     #disable software flow control
    ser.rtscts = False     #disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
    ser.writeTimeout = 2
    ser.open()

    if ser.isOpen():
         print(ser.name + ' is open...')

    ser.write("AT+CGPSINFO=0"+"\r\n")
    ser.write("ATE1"+"\r\n")
    ser.write("ATI"+"\r\n")
    ser.write("AT+CGPS=1,1"+"\r\n")
    ser.write("AT+CGPSOUT=8"+"\r\n")
    ser.write("AT+CGPSINFO=5"+"\r\n")

    time.sleep(1)
    out=''
    while True:
        out += ser.read(1)
        out2 = ser.readline()
        #print("out1: " + out)
        if re.match(r"CGPSINFO:", out2):
            print("out2: " + out2)
            print(out2.split(","))
            out3 = ((out2.split(",")[0].split(": ")[1:] + out2.split(",")[1:-1] + out2.split(",")[-1].split("\r")[0:]))[0:-1]
            msg = pynmea2.GGA('GP', 'GSV', out3)

            lat = int(str(float(out3[0].strip()[:-1])/100).split(".")[0])
            lng = int(str(float(out3[2].strip()[:-1])/100).split(".")[0])

            latdec = float("." + str(float(out3[0].strip()[:-1])/100).split(".")[1]) * 60
            lngdec = float("." + str(float(out3[2].strip()[:-1])/100).split(".")[1]) * 60

            latmin = int(str(latdec).split(".")[0])
            lngmin = int(str(lngdec).split(".")[0])

            latsec = float("." + str(latdec).split(".")[1]) * 60
            lngsec = float("." + str(lngdec).split(".")[1]) * 60

            print(pynmea2.parse(str(msg)))
            print("Latitude: " + str(lat) + " Degrees " + str(latmin) + " Minutes " + str(latsec) + " Seconds ") #str(msg.lat))
            print("Longitude: " + str(lng) + " Degrees " + str(lngmin) + " Minutes " + str(lngsec) + " Seconds ") #str(msg.lon))
            print("Alt: " + str(msg.altitude) + " Meters")
        #print(pynmea2.parse(out))

    ser.close()

serial_def()
