from sqlalchemy.orm import Session
import models
import schemas
import hashing


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).get(user_id)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_friend_by_id(db: Session, friend_id: int):
    return db.query(models.Friend).filter(models.Friend.id == friend_id).first()


def get_friends(db: Session, receiver_id: int):
    receiver: schemas.User = get_user_by_id(db, receiver_id)
    accepted_friends: list[schemas.User] = receiver.friends
    return accepted_friends


def get_friend_requests(db: Session, receiver_id: int, skip: int = 0, limit: int = 20):
    friend_requests = db.query(models.Friend).filter(models.Friend.receiver == receiver_id) \
        .filter(models.Friend.accepted == False).offset(skip).limit(limit).all()
    return friend_requests


# TODO: 'get_all_friend_requests' is for debug and should not enter production
def get_all_friend_requests(db: Session, skip: int = 0, limit: int = 20):
    friend_requests = db.query(models.Friend).filter(models.Friend.accepted == False).offset(skip).limit(limit).all()
    return friend_requests


def create_friend(db: Session, sender_id: int, receiver_id: int):
    new_friend = models.Friend(sender=sender_id, receiver=receiver_id)
    db.add(new_friend)
    db.commit()
    db.refresh(new_friend)
    print(f"Friendship created: {new_friend}")
    return new_friend


def accept_friend(db: Session, friend_id: int):
    # Assumes valid ID (verified before calling)
    friendship = db.query(models.Friend).filter(models.Friend.id == friend_id).first()
    if friendship:
        friendship.accepted = True
        db.commit()
        db.refresh(friendship)
    return friendship


def remove_friend(db: Session, friend_id: int):
    # Assumes valid ID (verified before calling)
    friendship = db.query(models.Friend).filter(models.Friend.id == friend_id).first()
    if friendship:
        # Delete Friendship
        db.delete(friendship)  # Use delete instead of commit to remove the friendship from the database
        db.commit()
        return True  # Indicate successful deletion
    return False  # Indicate friendship not found


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashing.get_password_hash(user.password)
    db_user = models.User(email=user.email, name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_pin_by_id(db: Session, pin_id):
    """Return the pin that matches the pin_id"""
    pin = db.query(models.Pin).filter(models.Pin.id == pin_id)
    return pin


def get_all_pins(db: Session, active_only: bool = False, skip: int = 0, limit: int = 20):
    """Return all pins in db (Debug only)"""
    if active_only:
        all_pins = db.query(models.Pin).filter(models.Pin.is_active)
    else:
        all_pins = db.query(models.Pin)
    #  Todo: Include filtering by user id to get a user's pin history as well or in new get function
    return all_pins


def create_pin(db: Session, user: schemas.User, pin: schemas.PinBase):
    """Add this Pin to db"""
    new_pin = models.Pin(
        session_start_time=pin.session_start_time,
        location_long=pin.location_long,
        location_lat=pin.location_lat,
        description=pin.description,
        owner_id=user.id,
    )
    db.add(new_pin)
    db.commit()
    db.refresh(new_pin)
    print(f"Pin created: {new_pin}")
    return new_pin


def update_pin(db: Session, pin: schemas.Pin):
    """Updates pin to match pin argument, returns status of change in db object"""
    pin_in_db = db.query(models.Pin).filter(models.Pin.id == pin.id).first()
    if pin_in_db:
        for key, value in pin.dict().items():
            setattr(pin_in_db, key, value)
        db.commit()
    new_pin_in_db = db.query(models.Pin).filter(models.Pin.id == pin.id).first()  # Check for change
    return new_pin_in_db == pin


def user_join_pin(db: Session, user_id: int, pin_id: int):
    """Updates user in db's joined_pin attribute with passed pin_id"""
    joined_user = db.query(models.User).filter(models.User.id == user_id).first()
    if joined_user:
        joined_user.joined_pin_id = pin_id
        db.commit()
        db.refresh(joined_user)
    return joined_user


def delete_pin(db: Session, pin_id: int):
    """Removed Pin from db (should not be used to end pin Sessions) Returns True if pin is no longer in db"""
    pin_in_db = db.query(models.Pin).filter(models.Pin.id == pin_id).first()
    if pin_in_db:
        db.delete(pin_in_db)
        db.commit()
        pin_check = db.query(models.Pin).filter(models.Pin.id == pin_id).first()
        # If the pin_check is None, it means the pin was successfully deleted
        return pin_check is None
    # If the pin doesn't exist, return True to indicate that it's effectively "deleted"
    return True
