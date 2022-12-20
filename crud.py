"""CRUD operations for Fancy Melons application."""

from model import User, Reservation, Melon, Tasting, connect_to_db





def create_user(first_name, last_name, email, password):
    """Create and return a new user."""
    user = User(first_name = first_name, last_name = last_name, email = email, password = password)
    return user





def create_melon(melon_name, melon_price, melon_photo):
    """Create and return a new melon."""
    melon = Melon(melon_name = melon_name, melon_price = melon_price, melon_photo = melon_photo)
    return melon





def create_reservation(user_id, reservation_date, tasting_id):
    """Create and return a new reservation."""
    reservation = Reservation(user_id = user_id, reservation_date = reservation_date, tasting_id = tasting_id)
    return reservation





def create_tasting(tasting_name, tasting_photo):
    """Create and return a new tasting."""
    tasting = Tasting(tasting_name = tasting_name, tasting_photo = tasting_photo)
    return tasting





def all_user_info_by_email(email):
    """Will return all of a user's information, searching by their email."""

    user = User.query.filter(User.email == email).first()

    return user





def all_tastings():
    """Will return all tastings currently available in database."""

    return Tasting.query.all()





def all_reservations():
    """Will return all reservations currently available in database."""

    return Reservation.query.all()






def all_reservations_by_user(user_id):
    """Will return all reservations by user_id."""

    return Reservation.query.filter(Reservation.user_id == user_id).all()





def tasting_details_by_reservation(reservation_id):
    """Will return all reservations by user_id."""

    reservation = Reservation.query.filter(Reservation.reservation_id == reservation_id).first()
    tasting_id = reservation.tasting_id

    return Tasting.query.filter(Tasting.tasting_id == tasting_id).all()





if __name__ == '__main__':
    from server import app
    connect_to_db(app)
