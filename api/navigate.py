import os
import requests
import json
import crud
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


def get_places(coordinates = '37.7749,-122.4194', num_stops = 6):
    """Get places from the places API given coordinates and number of stops. Saves the stops to the database as locations. Returns a list of location objects"""

    radius = '1500'
    place_type = 'bakery'
    keyword = 'dessert'

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    payload = {'location': coordinates, 'radius': radius, 'type': place_type, 'keyword': keyword, 'key': GOOGLE_API_KEY}

    req = requests.get(url, params=payload)


    places = req.json()['results']

    if len(places) < num_stops:
        return None

    locations = []
    for i in range(num_stops):
        place_id = places[i]['place_id']
        if crud.get_location_by_place_id(place_id):
            locations.append(crud.get_location_by_place_id(place_id))
        else:
            new_location = crud.create_location(place_id, coordinates=f"{places[i]['geometry']['location']['lat']},{places[i]['geometry']['location']['lng']}", location_name=places[i]['name'])
            locations.append(new_location)
            # eventually should make locations a set
    return locations

def calc_duration(location1, location2):
    """Takes in two location objects and returns the time it takes (in seconds) to drive between those two locations"""

    url = "https://maps.googleapis.com/maps/api/directions/json"
    payload = {'origin': f'place_id:{location1.google_place_id}', 'destination': f'place_id:{location2.google_place_id}', 'key': GOOGLE_API_KEY}
    req = requests.get(url, params=payload)

    duration = req.json()["routes"][0]["legs"][0]["duration"]["value"]    
    # time it takes in seconds to drive betwen locations
    return duration

def make_nearest_neighbor_route(locations_set):
    current_stop = locations_set.pop()
    stop_number = 1
    #add current stop as route location to database

    min_duration = 1000000
    while len(locations_set) > 1:
        for location in locations_set:
            duration = calc_duration(current_stop, location)
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
    connect_to_db(app, echo=False)

