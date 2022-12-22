"""Data model for Fancy Melons application."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    """Table for user information."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)

    #tables using "users" table as foreign key
    reservations = db.relationship("Reservation", back_populates = "user")

    def __repr__(self):
        return f'<User user_id = { self.user_id } email = { self.email }>'



class Reservation(db.Model):
    """Table for reservation information."""

    __tablename__ = "reservations"

    reservation_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    reservation_date = db.Column(db.DateTime, unique = True, nullable = False)
    tasting_id = db.Column(db.Integer, db.ForeignKey("tastings.tasting_id"))

    #foreign keys used by "reservations" table
    user = db.relationship("User", back_populates = "reservations")
    tasting = db.relationship("Tasting", back_populates = "reservations")

    def __repr__(self):
        return f'<Reservation reservation_id = { self.reservation_id }>'



class Melon(db.Model):
    """Table for reservation information."""

    __tablename__ = "melons"

    melon_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    melon_name = db.Column(db.String, unique = True, nullable = False)
    melon_price = db.Column(db.Integer, nullable = False)
    melon_photo = db.Column(db.String, unique = True, nullable = True)

    #tables using "melons" table as foreign key
    tastings = db.relationship("Tasting", back_populates = "melon")

    def __repr__(self):
        return f'<Melon melon_id = { self.melon_id }>'



class Tasting(db.Model):
    """Table for reservation information."""

    __tablename__ = "tastings"

    tasting_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    tasting_name = db.Column(db.String, unique = True, nullable = False)
    tasting_photo = db.Column(db.String, nullable = False)
    melon_id = db.Column(db.Integer, db.ForeignKey("melons.melon_id"))

    #foreign keys used by "tastings" table
    melon = db.relationship("Melon", back_populates = "tastings")

    #tables using "tastings" table as foreign key
    reservations = db.relationship("Reservation", back_populates = "tasting")

    def __repr__(self):
        return f'<Tasting tasting_id = { self.tasting_id } tasting_name = { self.tasting_name }>'







def connect_to_db(flask_app, db_uri="postgresql:///fancy_melons", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://ehqhdsdkvftrad:5ddbe6e977abd2d03ffa56b018fb7e70c83a78d37a0e10ea4a4fbe8d11734239@ec2-34-231-63-30.compute-1.amazonaws.com:5432/d4679k1g46l8f3'
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

if __name__ == "__main__":
    from server import app

    connect_to_db(app)