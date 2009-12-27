# Convert a CC msg
# and upload it to webservice

import simplejson as json
from StringIO import StringIO
from lxml import etree
import urllib
import urllib2

server_url = "http://localhost:8000/upload/"

def convert(msg):

    io = StringIO(msg)
    data = {}
    
    # parse xml into dict
    tree = etree.parse(io)
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

def convert_and_upload(msg):
    converted = convert(msg)
    result = upload(converted, server_url)
    return result

