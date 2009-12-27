# Create your views here.

from models import Reading, SensorReading

from datetime import datetime
from django.http import HttpResponse, HttpResponseNotAllowed
import simplejson as json


def default(request):
    return HttpResponse("Whoop")

def upload(request):
    
    if not request.method == 'POST':
        return HttpResponseNotAllowed()
    
    post = request.POST
    
    # upload one reading at a time
    # 1 upload = 1 Reading
    # upload = json dict
    
    if not post.has_key('reading'):
        return HttpResponseNotAllowed()
    
    raw_reading = json.dumps(post['reading'])
    reading = Reading()
    reading.time = datetime(raw_reading['time'])
    reading.temperature = raw_reading['temperature']
    reading.save()
    
    # read sensor data out of sublist of dicts
    # 1 sensor data = 1 SensorReading
    
    for sens in reading['sensors']:
        s = SensorReading()
        s.meter_id = sens['meter_id']
        s.meter_type = sens['meter_type']
        s.wattage = sens['wattage']
        s.reading = reading
        s.save()
    
    return HttpResponse('Upload')