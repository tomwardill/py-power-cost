# Convert a CC msg
# and upload it to webservice
import sys
try:
    import simplejson as json
except:
    try:
        import json
    except:
        print "No compatible json module, install simplejson"
        sys.exit(0)
from StringIO import StringIO
from lxml import etree
import urllib
import urllib2
from datetime import datetime

server_url = "http://localhost:8000/upload/"
bulk_server_url = "http://howrandom.net/bits/py-power-cost/bulk_upload/"

def convert_row_to_dict(row):
    """ Convert a db row into a dictionary """
    data = {}
    data['time'] = row[0]
    data['temperature'] = float(row[1])
    data['sensor_id'] = str(row[2])
    data['meter_type'] = str(row[3])

    data['ch1'] = float(row[4])
    data['ch2'] = float(row[5])
    data['ch3'] = float(row[6])

    return data

def convert_to_dict(msg):

    """ Convert the xml msg into a python dictionary  """

    if not msg:
        return None

    io = StringIO(msg)
    data = {}
    
    # parse xml into dict
    tree = etree.parse(io)
    
    # check we have a msg we're interested in
    if not tree.xpath('//tmpr'):
        return None
    
    #data['time'] = tree.xpath('//time')[0].text
    data['time'] = datetime.now()
    data['temperature'] = tree.xpath('//tmpr')[0].text
    data['sensor_id'] = tree.xpath('//id')[0].text
    data['meter_type'] = tree.xpath('//type')[0].text
    
    if tree.xpath('//ch1'):
        data['ch1'] = tree.xpath('//ch1')[0].getchildren()[0].text
    if tree.xpath('//ch2'):
        data['ch2'] = tree.xpath('//ch2')[0].getchildren()[0].text
    else:
        data['ch2'] = 0
    if tree.xpath('//ch3'):
        data['ch3'] = tree.xpath('//ch3')[0].getchildren()[0].text
    else:
        data['ch3'] = 0
    
    return data

def bulk_upload(data, server_url):


    values = {'data': data}


    send_data = urllib.urlencode(values)
    req = urllib2.Request(server_url, send_data)
    response = urllib2.urlopen(req)
    return_values = response.read()
    return return_values
#    f = open('converted.json', 'w')
#    f.write(data)
#    f.close()

def bulk_upload_dicts(dicts):

    chunks = []
    ret_vals = []

    # chunk the messages ino groups of 500
    # otherwise we exceed server upload limits
    if len(dicts) > 200:
        count = len(dicts) / 200
        current = 0
        prev = 0
        for x in range(count):
            current = (x + 1) * 200
            chunks.append(dicts[prev:current])
            prev = current
        chunks.append(dicts[current:])
    else:
        chunks.append(dicts)

    # iterate over the chunks and convert to json

    for chunk in chunks:
        data = []
        for msg in chunk:
            converted = json.dumps(msg)
            data.append(converted)
        # convert the final lot and upload
        final = json.dumps(data)
        ret_vals.append(bulk_upload(final, bulk_server_url))

    return ret_vals

def convert_and_upload(msg):
    converted = convert(msg)
    if converted:
        result = upload(converted, server_url)
        return result
    else:
        return None

def bulk_convert_and_upload(msgs):
    data = []
    
    chunks = []

    ret_vals = []

    # chunk msgs
    if len(msgs) > 500:
        count = len(msgs) / 500
        current = 0
        prev = 0
        for x in range(count):
            current = (x + 1) * 500
            chunks.append(msgs[prev:current])
            prev = current
        chunks.append(msgs[current:])
    else:
        chunks.append(msgs)
    
    for chunk in chunks:
        for msg in chunk:

            converted = convert(msg)
            if converted:
                data.append(converted)

        final = json.dumps(data)
        ret_vals.append(bulk_upload(final, bulk_server_url))

    return ret_vals
