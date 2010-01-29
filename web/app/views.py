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
    return render_to_response('main.html', context_instance = RequestContext(request))

def _process_message(data):
    """ Process a data message and save it """


    reading_date = parser.parse(data['time'])
    try:
        # Check if the reading for this time already exists (ignore if so)
        Reading.objects.get(time = reading_date)
        return False
    except:
        pass

    # Save the reading into the DB
    reading = Reading()
    reading.time = reading_date
    reading.temperature = Decimal(str(data['temperature']))
    reading.meter_id = data['sensor_id']
    reading.meter_type = int(data['meter_type'])
    reading.ch1_wattage = Decimal(str(data['ch1']))
    if data.has_key('ch2'):
        reading.ch2_wattage = Decimal(str(data['ch2']))
    if data.has_key('ch3'):
        reading.ch3_wattage = Decimal(str(data['ch3']))
    
    reading.save()

def bulk_upload(request):
    """ Receive and process a large amount of power messages at once """

    if not request.method == 'POST':
        return HttpResponse('NoData')

    post = request.POST

    # unpack the data
    raw_data = json.loads(post['data'])

    # assume that the data is a list/something iterable
    for data in raw_data:
        # process and save each one in the list
        _process_message(json.loads(data))

    return HttpResponse('Upload')

def upload(request):   
    """ Receive and process a single message """
    
    if not request.method == 'POST':
        return HttpResponse('NoData')
    
    post = request.POST
    
    # upload one reading at a time
    # 1 upload = 1 Reading
    # upload = json dict
    
    if not post.has_key('reading'):
        return HttpResponse('NoData')
    
    raw_reading = json.loads(post['reading'])
    
    if _process_message(raw_reading):
        return HttpResponse('Upload')
    return HttpResponse('Duplicate')

def raw_view(request):
    
    items = Reading.objects.all()
    
    return render_to_response('raw.html', 
                              {'items': items}, 
                              context_instance = RequestContext(request))

def data(request):
    return HttpResponse('data')

def hour(request, hours = None):
    
    return render_to_response('hour_graph.html',
                              {'mode': 'hour',
                              'hours': hours},
                              context_instance = RequestContext(request))
    
def day(request):
    return render_to_response('day_graph.html',
                              {'mode': 'day'},
                              context_instance = RequestContext(request))
def week(request):
    pass
def month(request):
    pass
def all_time(request):
    pass

def data_hour(request, hours = None):
    
    try:
        hours = int(hours)
    except:
        hours = None
    
    if not hours:
        previous_hour = datetime.now() - timedelta(hours = 1)
        current_hour = datetime.now()
    else:
        previous_hour = datetime.now() - timedelta(hours = 1 + hours)
        current_hour = datetime.now() - timedelta(hours = hours)
    
    data = Reading.objects.filter(time__range = (previous_hour, current_hour)).order_by('time')
    graph_data = [[time.mktime(k.time.timetuple()) * 1000, float(k.ch1_wattage)] for k in data]
    json_data = json.dumps(graph_data)
    
    return HttpResponse(json_data)
    
def data_day(request):
    previous_hour = datetime.now() - timedelta(days = 1)
    
    data = Reading.objects.filter(time__range = (previous_hour, datetime.now())).order_by('time')
    graph_data = [[time.mktime(k.time.timetuple()) * 1000, float(k.ch1_wattage)] for k in data]
    json_data = json.dumps(graph_data)
    
    return HttpResponse(json_data)
def data_week(request):
    pass
def data_month(request):
    pass
def data_all_time(request):
    pass
