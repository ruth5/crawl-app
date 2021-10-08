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
        return f"<User id={self.user_id} email={self.email}>" 

class Route(db.Model):
    """A route"""

    __tablename__ = "routes"

    route_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    total_stops = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates="routes")
    locations = db.relationship('Route_location', back_populates="routes")

    def __repr__(self):
        return f"<Route id={self.route_id} User id={self.user_id} Total stops={self.total_stops}"

# Create an association table to connect locations and features
location_features = db.Table('location_features', 
                        db.Column('location_id', db.ForeignKey('locations.location_id'), primary_key=True),
                        db.Column('route_id', db.ForeignKey('routes.route_id'), primary_key=True)
                        )

class Location(db.Model):
    """A location."""

    __tablename__ = "locations"
    location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    coordinates = db.Column(db.String, nullable=False)
    location_name = db.Column(db.String, nullable=False)
    city = db.Column(db.String)
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(10))
    routes = db.relationship("Route_location", back_populates="locations")
    features = db.relationship("Feature", secondary=location_features)

    def __repr__(self):
        return f"<Location id={self.location_id} Name={self.location_name} City={self.city}>"

class Route_location(db.Model):
    """A route location. Linkage between route and location classes."""

    __tablename__ = "route_locations"

    route_location_id = db.Column(db.Integer,
                                  autoincrement=True,
                                  primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))
    stop_number = db.Column(db.Integer)
    route = db.relationship("Route", back_populates="locations")
    location = db.relationship("Location", back_populates="routes")

    def __repr__(self):
        return f"""<Route location id = {self.route_location_id} Route id = {self.route_id} 
        Location id = {self.location_id} Stop number = {self.stop_number}>"""

class Feature(db.Model):
    """A feature that a location can have. Could be something like restaurant or bar, or could be karaoke, billiards, trendy, etc."""

    __tablename__ = "features"

    feature_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    feature_name = db.Column(db.String)

    def __repr__(self):
        return f"<Feature id = {self.feature_id} feature name={self.feature_name}>"


def connect_to_db(flask_app, db_uri="postgresql:///crawl", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)


