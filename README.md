# Crawl Overview
Crawl is a web app that seamlessly plans food and bar crawls for its users. Using the nearest neighbor algorithm, the app generates an optimized order of crawl stops to minimize backtracking. To build the app, I designed and created a PostreSQL database; built a backend server using Python, Flask, and SQLAlchemy; and rendered the frontend with Jinja and JavaScript. I integrated the Google Places and Geocoding APIs to find places based on user-submitted crawl criteria. I also incorporated Google Directions and Maps APIs to show a map and directions for the optimized crawl routes.


# Crawl Demo
View a demo of the crawl app here: https://youtu.be/vndtpEUeun0


# Structure
- `server.py` contains Flask server setup and all routes
- `navigate.py` contains functions related to creating and optimizing routes
- `model.py` set up of database that stores information like user info, locations, and route info and their relationships
- `crud.py` contains functions for interacting with the PostgreSQL database
- `\static\js\showRoute.js` renders routes on map for route generation page
- `\static\js\showSavedRoute.js` renders saved routes on map on saved routes page

# Running the app

- Set up an activate a python virtual environment:
    * `virtualenv env`
    * `source env/bin/activate`
- Install all dependencies:
    * `pip3 install -r requirements.txt`
- Obtain a Google API Key (free trial is available) and activate for the following four Google APIs: Geocoding, Places, Directions, Maps JavaScript
    * [Click "get started" on this page](https://developers.google.com/maps)
    * Set the following environmental variable to be your Google API Key: `GOOGLE_API_KEY`
- Set up and seed the database
    * run `python3 seed_database.py`
- Start up the server and run the app!
    * run `python3 server.py`
    * Navigate `localhost:5001` to see the app in your browser