"""Server for crawl app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db
import os
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'saddfkjaksdjfka;lsdfzxcjewmr.,9324'
app.jinja_env.undefined = StrictUndefined

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']



@app.route('/')
def show_homepage():
    """View homepage"""
    get_places()


    
    return render_template('index.html', GOOGLE_API_KEY=GOOGLE_API_KEY)

def get_places():
    """Get places from the places API."""
    # Try grabbing locations from the Places API on server side
    import requests
    coordinates = '37.7749%2C-122.4194'
    radius = '200'
    place_type = 'bakery'
    keyword = 'dessert'

    #I think there's a built in method that will construct the query string for me. Should add that in at some point
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={coordinates}&radius={radius}&type={place_type}&keyword={keyword}&key={GOOGLE_API_KEY}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(50 * "*")
    # print(response.text)
    # print(50 * "*")

    place_list = response.text
    print(place_list)
    print(50 * "*")



# refer back to AJAX skills
@app.route('/api/routes/<int:route_id>')
def get_route(route_id):
    """Return a route from the database as JSON."""




if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)