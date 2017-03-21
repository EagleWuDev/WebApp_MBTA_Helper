import urllib.request   # urlencode function
import urllib.parse
import json
from datetime import datetime
from pprint import pprint


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_BASE_URL_STOPTYPE = "http://realtime.mbta.com/developer/api/v2/routesbystop"
MBTA_BASE_URL_STOPPRED = "http://realtime.mbta.com/developer/api/v2/predictionsbystop"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    q = {"address": place_name}
    qencoded = urllib.parse.urlencode(q)
    query = GMAPS_BASE_URL + '?' + qencoded
    ret = get_json(query)
    return ret["results"][0]['geometry']['location']['lat'], ret["results"][0]['geometry']['location']['lng']


def get_nearest_stations(latitude, longitude, typeTrans):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.
    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    q = {"api_key": MBTA_DEMO_API_KEY, "lat": latitude, "lon": longitude, "format": "json"}
    qencoded = urllib.parse.urlencode(q)
    query = MBTA_BASE_URL + '?' + qencoded
    ret = get_json(query)
    arr = []
    for stop in ret['stop']:
        ret1 = get_stop_type(stop["stop_id"], typeTrans)
        if ret1:
            ret2 = get_stop_sched(stop['stop_id'])
            arr.append({"stop_id" : stop["stop_id"], "name": stop["stop_name"], "distance": round(float(stop["distance"]), 2), "time": ret2})
    return arr


def get_stop_type(stop_id, type):
    q = {"api_key": MBTA_DEMO_API_KEY, "stop" : stop_id, "format": "json"}
    qencoded = urllib.parse.urlencode(q)
    query = MBTA_BASE_URL_STOPTYPE + '?' + qencoded
    ret = get_json(query)

    if ret['mode'][0]['mode_name'] == type:
        return True
    else:
        return False
    
def get_stop_sched(stop_id):
    q = {"api_key": MBTA_DEMO_API_KEY, "stop": stop_id, "format": "json"}
    qencoded = urllib.parse.urlencode(q)
    query = MBTA_BASE_URL_STOPPRED+ '?' + qencoded
    ret = get_json(query)
    print(ret['mode'][0]['route'][0]['direction'][0]['trip'][0]['pre_dt'])
    timestamp = int(ret['mode'][0]['route'][0]['direction'][0]['trip'][0]['pre_dt'])
    awaySecs = int(ret['mode'][0]['route'][0]['direction'][0]['trip'][0]['pre_away'])
    value = datetime.fromtimestamp(timestamp)
    d = value.strftime("%I:%M %p")
    away = str(int(awaySecs/60)) + " minutes " + str(awaySecs%60) + " seconds"
    return {"arrival": d, "away": away}



def find_stop_near(place_name, typeTrans):
    """
    Given a place name or address, return the nearest MBTA stop and the 
    distance from the given place to that stop.
    """
    lat,long = get_lat_long(place_name)
    return get_nearest_stations(lat, long, typeTrans)

