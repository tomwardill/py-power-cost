import sqlite3

import cctools

import os, sys

# open db connection
# get current dir
current_dir = path.dirname(__file__)
conn = sqlite3.connect(os.path.join(current_dir), 'daemon-data.db'))

# get all the saved data
raw_data = conn.execute(''' select * from powercost ''')

# convert it to the correct form
list_data = raw_data.fetchall()
converted_data = []
for row in list_data:
    converted_data.append(cctools.convert_row_to_dict(row))

# upload it to server
try:
    cctools.bulk_upload_dicts(converted_data)

# if successful, remove from db
    for row in list_data:
        t = (row[0], )
        conn.execute(''' delete from powercost where date = ?''', t)
        conn.commit()

except Exception, err:
    print err
# if not successful, give up (running script again will try again)


