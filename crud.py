""" CRUD operations."""

from model import db, User, Route_location, Route, Location, Type, connect_to_db


def create_user(email, password, first_name=None, last_name=None, home_zip_code=None):
    """Create and return a new user."""

    user = User(email=email, password=password, first_name=first_name, last_name=last_name, home_zip_code=home_zip_code)

    db.session.add(user)
    db.session.commit()

    return user

def create_route(total_stops, user_id=None):
    """Create and return a new route."""

    route = Route(user_id=user_id, total_stops=total_stops)

    db.session.add(route)
    db.session.commit()

    return route

def create_location(google_place_id, coordinates=None, location_name=None, city=None, state=None, zipcode=None):
    """Creates and returns a location."""
    
    location = Location(google_place_id=google_place_id, coordinates=coordinates, location_name=location_name, city=city, state=state, zipcode=zipcode)

    db.session.add(location)
    db.session.commit()

    return location


def create_route_location(route_id, location_id, stop_number):
    """Creates and returns a route location. This connects routes and locations and also records the stop number."""

    route_location = Route_location(route_id=route_id, location_id=location_id, stop_number=stop_number)

    db.session.add(route_location)
    db.session.commit()

    return route_location

def create_type(type_name):
    """Creates and returns a type"""

    type_ = Type(type_name=type_name)

    db.session.add(type_)
    db.session.commit()

    return type_

def get_user_by_email(email):
    """Returns a user with that email if it exists, otherwise return None."""
    
    return User.query.filter_by(email=email).first()

def get_user_by_id(user_id):
    """Returns a user with that id if it exists, otherwise return None."""
    
    return User.query.filter_by(user_id=user_id).first()

def get_location_by_place_id(google_place_id):
    """Returns a location with that Google place_id if it exists, otherwise return None."""

    return Location.query.filter_by(google_place_id=google_place_id).first()

def get_route_by_id(route_id):
    """Returns the route with the given route id, otherwise return None."""

    return Route.query.filter_by(route_id=route_id).first()

def get_stops_in_order_by_route_id(route_id):
    """Returns route locations in order for the route with the given route id."""

    route_locations = Route_location.query.filter_by(route_id=route_id).order_by(Route_location.stop_number)
    return route_locations

def save_route_to_user_profile(route, user_id, description):
    """Associate a user id and the user's entered description."""

    route.user_id = user_id
    route.description = description
    db.session.commit()

if __name__ == '__main__':
    from server import app
    connect_to_db(app, echo=False)