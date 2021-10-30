""" CRUD operations."""

from model import db, User, Route_location, Route, Location, Type, connect_to_db

connect_to_db

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


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
