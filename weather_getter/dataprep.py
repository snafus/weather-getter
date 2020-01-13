import json
import datetime
from collections import OrderedDict

def try_retrieve(thedict,key,defaultval):
    """Helper method to return values, else default
    """
    if key not in thedict:
        return defaultval
    else:
        return thedict[key]

def prepare_current_weather(j):
    """Prepare a dict of parameters from the input dict
    """

    d = OrderedDict()
    d['name'] = j['name']
    d['id'  ] = j['id']
    d['tz'  ] = j['timezone']
    d['dt'  ] = datetime.datetime.fromtimestamp(j['dt'])

    if 'wind' in j:
        d['wind_speed'] = try_retrieve(j['wind'],'speed',-1)
        d['wind_dir'  ] = try_retrieve(j['wind'],'deg'  ,-1)
        d['wind_gust' ] = try_retrieve(j['wind'],'gust' ,-1)
    else:
        pass

    d['pressure'  ]   = try_retrieve(j['main'],'pressure',-1)
    d['humidity'  ]   = try_retrieve(j['main'],'humidity',-1)
    d['temp'      ]   = try_retrieve(j['main'],'temp',-999)
    d['feels_like']   = try_retrieve(j['main'],'feels_like',-999)
    d['visibility']   = try_retrieve(j,'visibility',-1)
    d['clouds_all']   = try_retrieve(j['clouds'],'all',-1)

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
        d['wind_speed'] = try_retrieve(l['wind'],'speed',-1)
        d['wind_dir'  ] = try_retrieve(l['wind'],'deg',-1)
        d['wind_gust' ] = try_retrieve(l['wind'],'gust' ,-1)

        d['pressure'  ]   = try_retrieve(l['main']  ,'pressure',-1)
        d['humidity'  ]   = try_retrieve(l['main']  ,'humidity',-1)
        d['temp'      ]   = try_retrieve(l['main']  ,'temp',-999)
        d['feels_like']   = try_retrieve(l['main']  ,'feels_like',-999)
        d['clouds_all']   = try_retrieve(l['clouds'],'all',-1)

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
