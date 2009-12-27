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
    
    raw_reading = json.loads(post['reading'])
    reading = Reading()
    reading.time = datetime(raw_reading['time'])
    reading.temperature = raw_reading['temperature']
    reading.meter_id = raw_reading['sensor_id']
    reading.meter_type = raw_reading['meter_type']
    reading.ch1_wattage = raw_reading['ch1']
    reading.ch2_wattage = raw_reading['ch2']
    reading.ch3_wattage = raw_reading['ch3']
    
    reading.save()
    
    return HttpResponse('Upload')