import sqlite3
import serial

import cctools

ser = serial.Serial('/dev/tty.usbserial', 57600, timeout = 1)

conn = sqlite3.connect('daemon-data.db')


while True:
    reading = ser.readline()

    if reading and reading.startswith('<'):
        converted = cctools.convert_to_dict(reading)
        if not converted:
            continue
        reading_list = [converted['time'], converted['temperature'], converted['sensor_id'], converted['meter_type'], converted['ch1'], converted['ch2'], converted['ch3']]
        conn.execute("""insert into powercost values(?,?,?,?,?,?,?)""", reading_list)

    data = conn.execute(""" select * from powercost  """)
    conn.commit()
