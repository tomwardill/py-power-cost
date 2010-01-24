import sqlite3

conn = sqlite3.connect('daemon-data.db')

conn.execute(""" create table powercost(date text, temperature numeric, sensor_id integer, meter_type integer, ch1 numeric, ch2 numeric, ch3 numeric  )  """)

