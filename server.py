"""Server for crawl app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db
import crud
import os
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
    pass




if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)