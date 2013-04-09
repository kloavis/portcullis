'''
' datastreams/views/get_data.py
' Contributing Authors:
'    Jeremiah Davis (Visgence, Inc)
'
' (c) 2013 Visgence, Inc.
'''

# System imports
from django.http import HttpResponse
from django.template import RequestContext, loader
try:
    import simplejson as json
except ImportError:
    import json


# Local imports
def get_data_by_ds_column(request):
    '''
    ' This view will take a column name/value and a time range (in epoch secs),
    ' and return a json response containing all the matching sensor data points.
    '
    ' returns - HttpResponse containing jsondata {ds_id: [(timestamp, value), ...], ... }
    '''
    # TODO: Check perms, etc.

    jsonData = request.REQUEST.get('jsonData', None)
    if jsonData is None:
        error = 'Error: No jsonData received.'
        return HttpResponse(json.dumps({'errors': error}), mimetype='application/json')
    try:
        jsonData = json.loads(jsonData)
    except Exception as e:
        error = 'Error: Invalid JSON: ' + str(e)
        return HttpResponse(json.dumps({'errors': error}, mimetype='application/json'))

    try:
        column = jsonData['column']
        value = jsonData['value']
        time_start = jsonData['start']
        time_end = jsonData['end']
    except KeyError as e:
        error = 'Error: KeyError: %s' + str(e)
        return HttpResponse(json.dumps({'errors': error}, mimetype='application/json'))

    # TODO: Scrub column, so it is safe to use in query

    data_points = SensorReading.objects.filter(
        timestamp__gte=time_start,
        timestamp__lte=time_end
        ).extra(
        where=['portcullis_sensorreading.datastream_id IN (SELECT portcullis_datastream.id FROM portcullis_datastream WHERE portcullis_datastream.' + column + ' LIKE %s )'], params=['%' + value + '%'])

    data = {}
    for point in data_points:
        if point.datastream.id not in data:
            data[point.datastream.id] = []
        data[point.datastream.id].append((point.timestamp, point.value))

    return HttpResponse(json.dumps(data), mimetype='application/json')
