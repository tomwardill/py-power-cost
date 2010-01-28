import psycopg2
import serial

import cctools

ser = serial.Serial('/dev/tty.usbserial', 57600, timeout = 1)

conn = psycopg2.connect("dbname='powercost' user='powercost' host='localhost' password='costpower'")
cur = conn.cursor()

while True:
    reading = ser.readline()

    if reading and reading.startswith('<'):
        converted = cctools.convert_to_dict(reading)
        if not converted:
            continue
        cur.execute("""insert into powercost values('%s','%s','%s','%s','%s','%s','%s')""" % (converted['time'], converted['temperature'], converted['sensor_id'], converted['meter_type'], converted['ch1'], converted['ch2'], converted['ch3']))

    conn.commit()
