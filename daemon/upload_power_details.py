import psycopg2
import cctools

import os, sys

# open db connection
# get current dir
current_dir = os.path.dirname(__file__)
conn = psycopg2.connect("dbname='powercost' user='powercost' host='localhost' password='costpower'")
cur = conn.cursor()

# get all the saved data
cur.execute(''' select * from powercost ''')
raw_data = cur.fetchall()

# convert it to the correct form
list_data = raw_data
converted_data = []
for row in list_data:
    converted_row = cctools.convert_row_to_dict(row)
    converted_data.append(converted_row)

# upload it to server
try:
    cctools.bulk_upload_dicts(converted_data)

# if successful, remove from db
    for row in list_data:
        sql_string = "delete from powercost where date = '%(date)s'" % {'date': str(row[0])}
        cur.execute(sql_string)
        conn.commit()

except Exception, err:
    print err
    print err.read()
# if not successful, give up (running script again will try again)


