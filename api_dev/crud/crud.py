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
