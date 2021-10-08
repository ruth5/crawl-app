"""Data models for Crawl app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    route = db.relationship('Route', back_populates="users")

    def __repr__(self):
        return f"<User id={self.user_id} email={self.email}> 

class Route(db.Model):
    """A route"""

    __tablename__ = "routes"

    route_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    total_stops = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates="routes")

    def __repr__(self):
        return f"<Route id={self.route_id} User id={self.user_id} Total stops={self.total_stops}"

class Location_type(db.Model):
    """The type of location"""

    __tablename__ = 

class Location(db.Model):
    """A location."""

    __tablename__ = "locations"
    location_id = db.Column(db.Integer, autoincrement=true, primary_key=true)


class Route_location(db.Model):
    """A route location. Linkage between route and location classes."""

    __tablename__ = "route_locations"

    route_location_id = db.Column(db.Integer,
                                  autoincrement=true,
                                  primary_key=true)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))
    location_id = db.Column(db)




