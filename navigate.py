import os
import requests
import json
from model import db, User, Route_location, Route, Location, Type, connect_to_db


GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

def get_coordinates(location):
    """Get coordinates for a given location."""

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    payload = {'address': location, 'key': GOOGLE_API_KEY}
    req = requests.get(url, params=payload)
    req_info = req.json()
    coordinates = req_info["results"][0]["geometry"]["location"]

    formatted_coords = f"""{coordinates['lat']},{coordinates['lng']}"""


    return formatted_coords


def get_places(coordinates = '37.7749%2C-122.4194'):
    """Get places from the places API."""
    # Try grabbing locations from the Places API on server side

    radius = '1500'
    place_type = 'bakery'
    keyword = 'dessert'

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    payload = {'location': coordinates, 'radius': radius, 'type': place_type, 'keyword': keyword, 'key': GOOGLE_API_KEY}

    req = requests.get(url, params=payload)
    print(req.url)

    place_list = req.json()

    return place_list

def make_nearest_neighbor_route(locations_set):
    current_stop = locations_set.pop()
    stop_number = 1
    #add current stop as route location to database

    min_duration = 100000
    while len(locations_set) > 1:
        for location in locations_set:
            duration = calc_duration(current_stop.google_place_id, location.google_place_id)
            if min_duration > duration:
                min_duration = duration
                nearest_neighbor = location
        current_stop = nearest_neighbor
        stop_number += 1
        #add current stop as route location to database
        locations_set.remove(current_stop)
    final_stop = locations_set.pop()
    stop_number+= 1
    # add final stop to db


    pass


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

