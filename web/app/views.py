from models import Reading

from datetime import datetime
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Avg, Min

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
    return render_to_response('week_graph.html',
                                {'mode': 'week'},
                                context_instance = RequestContext(request))
def month(request):
    return render_to_response('month_graph.html',
                                {'mode': 'month'},
                                context_instance = RequestContext(request))


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
    temp_data = [[time.mktime(k.time.timetuple()) * 1000, float(k.temperature)] for k in data]
    json_data = json.dumps([graph_data, temp_data])
    
    return HttpResponse(json_data)

def data_day(request):
    now = datetime.now()
    previous_hour = now - timedelta(days = 1)

    data = Reading.objects.filter(time__range = (previous_hour, now)).order_by('time')

    averaged_data = []

    for i in range(int(len(data) / 10)):
        average_range = data[i*10:(i+1)*10]
        d = {}
        d['time'] = data[i*10].time
        for a in average_range:
            if d.has_key('watt'):
                d['watt'] += a.ch1_wattage
            else:
                d['watt'] = a.ch1_wattage

            # add average temperature
            if d.has_key('temp'):
                d['temp'] += a.temperature
            else:
                d['temp'] = a.temperature
        
        # perform the averages
        d['watt'] = d['watt'] / 10
        d['temp'] = d['temp'] / 10
        averaged_data.append(d)
    

    graph_data = [[time.mktime(k['time'].timetuple()) * 1000, float(k['watt'])] for k in averaged_data]
    temp_data = [[time.mktime(k['time'].timetuple()) * 1000, float(k['temp'])] for k in averaged_data]
    json_data = json.dumps([graph_data, temp_data])
    
    return HttpResponse(json_data)
def data_week(request):
    now = datetime.now()
    previous_week = now - timedelta(days = 7)

    averaged_data = []

    while previous_week < now:
        previous_plus_hour = previous_week + timedelta(hours = 1)
        data = Reading.objects.filter(time__range = (previous_week, previous_plus_hour)).aggregate(temp_average = Avg('temperature'), hour_average = Avg('ch1_wattage'), first_time = Min('time'))
        averaged_data.append(data)
        previous_week = previous_plus_hour

    graph_data = [[time.mktime(k['first_time'].timetuple()) * 1000, float(k['hour_average'])] for k in averaged_data if k['first_time']]
    temp_data = [[time.mktime(k['first_time'].timetuple()) * 1000, float(k['temp_average'])] for k in averaged_data if k['first_time']]
    json_data = json.dumps([graph_data, temp_data])

    return HttpResponse(json_data)

def data_month(request):
    now = datetime.now()
    previous_month = now - timedelta(days = 30)

    averaged_data = []

    while previous_month < now:
        previous_plus_day = previous_month + timedelta(days = 1)
        data = Reading.objects.filter(time__range = (previous_month, previous_plus_day)).aggregate(day_average = Avg('ch1_wattage'), first_time = Min('time'))
        averaged_data.append(data)
        previous_month = previous_plus_day

    graph_data = [[time.mktime(k['first_time'].timetuple()) * 1000, float(k['day_average'])] for k in averaged_data if not k['first_time'] is None]
    json_data = json.dumps(graph_data)

    return HttpResponse(json_data)



def data_all_time(request):
    pass
