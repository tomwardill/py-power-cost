# Create your views here.

from models import Reading

from datetime import datetime
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import RequestContext
from django.shortcuts import render_to_response
import simplejson as json
from decimal import Decimal
from dateutil import parser
import simplejson as json
from datetime import datetime, timedelta
import time


def default(request):
    return HttpResponse("Whoop")

def upload(request):
    

    
    if not request.method == 'POST':
        return HttpResponse('NoData')
    
    post = request.POST
    
    # upload one reading at a time
    # 1 upload = 1 Reading
    # upload = json dict
    
    if not post.has_key('reading'):
        return HttpResponse('NoData')
    
    raw_reading = json.loads(post['reading'])
    
    reading_date = parser.parse(raw_reading['time'])
    try:
        Reading.objects.get(time = reading_date)
        return HttpResponse('Duplicate')
    except:
        pass


    reading = Reading()
    reading.time = reading_date
    reading.temperature = Decimal(raw_reading['temperature'])
    reading.meter_id = raw_reading['sensor_id']
    reading.meter_type = int(raw_reading['meter_type'])
    reading.ch1_wattage = Decimal(raw_reading['ch1'])
    if raw_reading.has_key('ch2'):
        reading.ch2_wattage = Decimal(raw_reading['ch2'])
    if raw_reading.has_key('ch3'):
        reading.ch3_wattage = Decimal(raw_reading['ch3'])
    
    reading.save()

    return HttpResponse('Upload')

def raw_view(request):
    
    items = Reading.objects.all()
    
    return render_to_response('raw.html', 
                              {'items': items}, 
                              context_instance = RequestContext(request))

def hour(request):
    
    return render_to_response('graph.html',
                              {'mode': 'hour'},
                              context_instance = RequestContext(request))
    
def day(request):
    return render_to_response('graph.html',
                              {'mode': 'day'},
                              context_instance = RequestContext(request))
def week(request):
    pass
def month(request):
    pass
def all_time(request):
    pass

def data_hour(request):
    
    previous_hour = datetime.now() - timedelta(hours = 1)
    
    data = Reading.objects.filter(time__range = (previous_hour, datetime.now()))
    graph_data = [[time.mktime(k.time.timetuple()) * 1000, float(k.ch1_wattage)] for k in data]
    json_data = json.dumps(graph_data)
    
    return HttpResponse(json_data)
    
def data_day(request):
    previous_hour = datetime.now() - timedelta(days = 1)
    
    data = Reading.objects.filter(time__range = (previous_hour, datetime.now()))
    graph_data = [[time.mktime(k.time.timetuple()) * 1000, float(k.ch1_wattage)] for k in data]
    json_data = json.dumps(graph_data)
    
    return HttpResponse(json_data)
def data_week(request):
    pass
def data_month(request):
    pass
def data_all_time(request):
    pass