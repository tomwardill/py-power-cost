import psycopg2

conn = psycopg2.connect("dbname='powercost' user='powercost' host='localhost' password='costpower'")
cur = conn.cursor()

try:
    cur.execute(""" create table powercost(date text, temperature numeric, sensor_id integer, meter_type integer, ch1 numeric, ch2 numeric, ch3 numeric  )  """)
    conn.commit()
except Exception, err:
    print err
