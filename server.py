"""Server for crawl app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db
import crud
import os
import requests
import json
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'saddfkjaksdjfka;lsdfzxcjewmr.,9324'
app.jinja_env.undefined = StrictUndefined

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']



@app.route('/')
def show_homepage():
    """View homepage"""

    
    return render_template('index.html', GOOGLE_API_KEY=GOOGLE_API_KEY)

@app.route('/users', methods=['POST'])
def create_account():
    """Create a user with email and password."""

    email = request.form.get('email')
    password = request.form.get('password')

    if crud.get_user_by_email(email):
        flash("An account already exists for that email address")
    else:
        crud.create_user(email, password)
        flash("Your account has been created.")
    
    return redirect("/")

@app.route('/login', methods=['POST'])
def login_user():
    """Logs a user in."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if not user:
        flash("We don't have an account associated with that email")
    else: 
        if password == user.password:
            session['logged_in_user_id'] = user.user_id
            flash(f"{user.email}, you're logged in!")
        else:
            flash("The password you provided is not correct")

    return redirect('/')

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




@app.route('/api/routes/<int:route_zip_code>')
def generate_route(route_zip_code):
    """Generates a route based on user inputed zip code."""
    # print("8" *50)
    # print(route_zip_code)
    coordinates = get_coordinates(route_zip_code)
    places = get_places(coordinates)
    # print(50 * ">")
    # print(places)

    num_stops = 3
    place_ids = []

    for i in range(num_stops):
        place_ids.append(places['results'][i]['place_id'])
        print(places['results'][i]['name'])
    
    print("8" *50)

    print(place_ids)
    
    
    if places:
        return jsonify({
            'place_ids': place_ids
        })
    else:
        return jsonify({'status': 'error',
                        'message': 'No places found for your criteria'})






if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)