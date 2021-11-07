"""Server for crawl app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db
import crud
from navigate import (get_coordinates, get_places)
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