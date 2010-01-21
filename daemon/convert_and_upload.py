# Convert a CC msg
# and upload it to webservice

import simplejson as json
from StringIO import StringIO
from lxml import etree
import urllib
import urllib2

server_url = "http://localhost:8000/upload/"
bulk_server_url = "http://localhost:8000/bulk_upload/"

def convert(msg):

    if not msg:
        return None

    io = StringIO(msg)
    data = {}
    
    # parse xml into dict
    tree = etree.parse(io)
    
    # check we have a msg we're interested in
    if not tree.xpath('//tmpr'):
        return None
    
    data['time'] = tree.xpath('//time')[0].text
    data['temperature'] = tree.xpath('//tmpr')[0].text
    data['sensor_id'] = tree.xpath('//id')[0].text
    data['meter_type'] = tree.xpath('//type')[0].text
    
    if tree.xpath('//ch1'):
        data['ch1'] = tree.xpath('//ch1')[0].getchildren()[0].text
    if tree.xpath('//ch2'):
        data['ch2'] = tree.xpath('//ch2')[0].getchildren()[0].text
    if tree.xpath('//ch3'):
        data['ch3'] = tree.xpath('//ch3')[0].getchildren()[0].text
    
    # convert to json
    final = json.dumps(data)
    
    # return data
    return final

def upload(msg, server_url):
    
    values = {'reading': msg}
    data = urllib.urlencode(values)
    req = urllib2.Request(server_url, data)
    response = urllib2.urlopen(req)
    return_values = response.read()
    return return_values

def bulk_upload(data, server_url):


    values = {'data': data}


    send_data = urllib.urlencode(values)
    req = urllib2.Request(server_url, send_data)
    try:
        response = urllib2.urlopen(req)
        return_values = response.read()
        return return_values
    except Exception, err:
        print err
#    f = open('converted.json', 'w')
#    f.write(data)
#    f.close()


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
