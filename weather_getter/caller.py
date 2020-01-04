from urllib.request import Request,urlopen
from urllib.parse import urlencode
import json

def request_coords(request_mode, lat,lon,apikey):
    """Retrieve for given coordinate.
        input: request_mode - 'weather' for current,
                              'forecast' for future
               lat - latitude as float
               lon - longitute as float
        returns:
            dictionary object from parsed json response
        raises:
           HTTPError: for bad request (e.g. if coordinates are out of range)
           #FIXME
        """
    #FIXME - safer way to encode
    url = f'https://api.openweathermap.org/data/2.5/{request_mode}?lat={lat}&lon={lon}&appid={apikey}&units=metric'
    r   = Request(url)
    with urlopen(r) as f:
        js = json.loads(f.read().decode('utf-8'))
    return js


def current_weather_by_coor(lat,lon,apikey):
    """Retrieve current weather for a given coordinate.

        No range validation checking, etc. is applied here
        input: lat - latitude as float
               lon - longitute as float

        returns:
           dictionary object from parsed json response

        raises:
           #FIXME
    """
    return request_coords('weather',lat,lon,apikey)


def forecast_weather_by_coor(lat,lon,apikey):
    """Retrieve forecast weather for a given coordinate.

        No range validation checking, etc. is applied here
        input: lat - latitude as float
               lon - longitute as float

        returns:
           dictionary object from parsed json response

        raises:
           HTTPError: for bad request (e.g. if coordinates are out of range)
           #FIXME
    """
    return request_coords('forecast',lat,lon,apikey)
