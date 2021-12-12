"""Server for crawl app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify, send_from_directory)
from model import db, connect_to_db
import crud
from navigate import (get_coordinates, get_places, make_nearest_neighbor_route, calc_duration)
import os
import requests
import json
from jinja2 import StrictUndefined
from ast import literal_eval

app = Flask(__name__)
app.secret_key = 'saddfkjaksdjfka;lsdfzxcjewmr.,9324'
app.jinja_env.undefined = StrictUndefined

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']




@app.route('/')
def show_homepage():
    """View homepage"""

    if "user_id" in session:
        return redirect("my-crawl")

    
    return render_template('index.html', GOOGLE_API_KEY=GOOGLE_API_KEY)

@app.route('/my-crawl')
def show_crawl():

    if "user_id" not in session:
        return redirect('/')

    return render_template('my-crawl.html', GOOGLE_API_KEY=GOOGLE_API_KEY)

@app.route('/log-out')
def clear_session():

    if "user_id" in session:
        session.clear()
        flash("You have been logged out.")

    return redirect('/')

@app.route('/my-crawl', methods = ['POST'])
def save_crawl():
    """Gets the crawl name from the saving route forms and adds the crawl name 
    and the id of the current user to the route in the database."""

    crawl_route_name = request.form.get('crawl-name')
    user = crud.get_user_by_id(session["user_id"])
    route = crud.get_route_by_id(session['current_route_id'])
    # can move to crud file if desired
    route.user_id = int(session["user_id"])
    # can move to crud file if desired
    route.description = crawl_route_name
    db.session.commit()

    # route_locations = route.route_locations
    # for route_location in route_locations:
    #     print(route_location.location)
    flash('Thanks for saving your route!')
    return redirect('/my-crawl')


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
            session['user_id'] = user.user_id
            # flash(f"{user.email}, you're logged in!")
        else:
            flash("The password you provided is not correct")

    return redirect('/')




@app.route('/api/routes')
def generate_route():
    """Generates a route based on user inputed location such as zip code or city name."""

    crawl_start_location = request.args.get('location')
    radius_in_miles = float(request.args.get('radius'))
    radius_in_meters = radius_in_miles * 1609.34

    place_type = request.args.get('place_type')

    keyword = request.args.get('keyword')
    num_stops = int(request.args.get('stops'))
    coordinates = get_coordinates(crawl_start_location)
    route_info = make_nearest_neighbor_route(get_places(coordinates = coordinates, num_stops = num_stops, radius = str(radius_in_meters), place_type = place_type, keyword = keyword))
    locations = route_info["locations_in_order"]
    route = route_info["route"]
    location_info = []
    
    
    if locations:
        session['current_route_id'] = route.route_id
        for location in locations:
            location_info.append({"place_id": location.google_place_id, "coords": literal_eval(location.coordinates), "name": location.location_name})
        return jsonify({
            'locations': location_info
        })
    else:
        return jsonify({'status': 'error',
                        'message': 'No places found for your criteria'})

@app.route('/my-saved-routes')
def show_saved_routes_by_user():
    """Show the saved routes for the user who is currently logged in."""

    if "user_id" not in session:
        return redirect('/')
    else:
        print(session["user_id"])
        current_user = crud.get_user_by_id(session["user_id"])
        print(current_user)
        user_routes = current_user.routes
        print(user_routes)
        for route in user_routes:
            print(route.description)
            print(route.route_locations)

    return render_template('my-saved-routes.html', routes = user_routes, GOOGLE_API_KEY=GOOGLE_API_KEY)

@app.route('/api/saved-routes/<route_id>')
def get_saved_route(route_id):
    """Returns location info for a saved route"""
    #Need to add in a way for users to identify their route - they should enter a name so this shows on the saved routes page. 
    locations = []
    route = crud.get_route_by_id(route_id)
    for route_location in route.route_locations:
        locations.append(route_location.location)
    location_info = []
    
    
    if locations:
        session['current_route_id'] = route.route_id
        for location in locations:
            location_info.append({"place_id": location.google_place_id, "coords": literal_eval(location.coordinates), "name": location.location_name})
        return jsonify({
            'locations': location_info
        })
    else:
        return jsonify({'status': 'error',
                        'message': 'No places found for your criteria'})






if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app, echo=False)
    app.run(host="0.0.0.0", debug=True, port=5001)