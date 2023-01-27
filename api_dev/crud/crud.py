from sqlalchemy.orm import Session
import models
import schemas
import hashing


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_friend_by_id(db: Session, friend_id: int):
    return db.query(models.Friend).filter(models.Friend.id == friend_id).first()


def get_friends(db: Session, receiver_id: int = None, skip: int = 0, limit: int = 100):
    if not receiver_id:
        print(f"Printing ALL friend relationships, this should only be a debug tool!")
        friends = db.query(models.Friend).offset(skip).limit(limit).all()
    else:
        friends = db.query(models.Friend).filter(models.Friend.receiver == receiver_id).offset(skip).limit(limit).all()
    return friends


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


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashing.get_password_hash(user.password)
    db_user = models.User(email=user.email, name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
