import json
import datetime
from collections import OrderedDict

def prepare_current_weather(j):
    """Prepare a dict of parameters from the input dict
    """

    d = OrderedDict()
    d['name'] = j['name']
    d['id'  ] = j['id']
    d['tz'  ] = j['timezone']
    d['dt'  ] = datetime.datetime.fromtimestamp(j['dt'])

    if 'wind' in j:
        d['wind_speed'] = j['wind']['speed']
        d['wind_dir'  ] = j['wind']['deg']
    else:
        pass

    d['pressure'  ]   = j['main']['pressure']
    d['humidity'  ]   = j['main']['humidity']
    d['temp'      ]   = j['main']['temp']
    d['feels_like']   = j['main']['feels_like']
    d['visibility']   = j['visibility']
    d['clouds_all']   = j['clouds']['all']

    return d

def prepare_current_weather_influx(d):
    """Use prepared intput and create specific version for influxdb
{
"measurement": "brushEvents",
"tags": {
"user": "Carol",
"brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
},
"time": "2018-03-28T8:01:00Z",
"fields": {
"duration": 127
}
    """
    res = {
        'measurement': 'current_weather',
        'tags':{},
        'time':d['dt'].strftime('%Y-%m-%dT%H:%M:%SZ'),
        'fields':{},
    }
    tags = ['name','id']
    for t in tags:
        res['tags'][t] = d[t]
    for t in d.keys():
        if t in tags:
            continue
        if t == 'dt':
            continue
        if t == 'tz':
            res['fields'][t] = int(d[t])
        else:
            res['fields'][t] = float(d[t])
    return res



def prepare_forecast_weather(j):
    """Prepare a dict of parameters from the input dict

        returns a dict with main parameters, and a list of forecasts
    """

    r = OrderedDict()
    r['name'] = j['city']['name']
    r['id'  ] = j['city']['id']
    r['tz'  ] = j['city']['timezone']
    forecasts = []

    for l in j['list']:
        d = OrderedDict(r)
        d['dt'  ] = datetime.datetime.fromtimestamp(l['dt'])
        d['wind_speed'] = l['wind']['speed']
        d['wind_dir'  ] = l['wind']['deg']

        d['pressure'  ]   = l['main']['pressure']
        d['humidity'  ]   = l['main']['humidity']
        d['temp'      ]   = l['main']['temp']
        d['feels_like']   = l['main']['feels_like']
        d['clouds_all']   = l['clouds']['all']

        d['rain_3h' ]    = 0 if not 'rain' in l else l['rain']['3h']
        forecasts.append(d)

    return forecasts


def prepare_forecast_weather_influx(ds):
    """Use prepared intput and create specific version for influxdb

    """
    results = []
    for d in ds:
        res = {
            'measurement': 'forecast_weather',
            'tags':{},
            'time':d['dt'].strftime('%Y-%m-%dT%H:%M:%SZ'),
            'fields':{},
            }
        tags = ['name','id']
        for t in tags:
            res['tags'][t] = d[t]
        for t in d.keys():
            if t in tags:
                continue
            if t == 'dt':
                continue
            if t == 'tz':
                res['fields'][t] = int(d[t])
            else:
                res['fields'][t] = float(d[t])
        results.append(res)
    return results
