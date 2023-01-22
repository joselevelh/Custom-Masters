from sqlalchemy.orm import Session
import models
import schemas
import hashing


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_friends(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    # Todo: Limit query to relationships where the user is involved
    return db.query(models.Friend).offset(skip).limit(limit).all()


def create_friend(db: Session, sender_id: int, receiver_id: int):
    # Todo: Creates friendship in table and returns the ID
    pass


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashing.get_password_hash(user.password)
    db_user = models.User(email=user.email, name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
