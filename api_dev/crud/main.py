from fastapi import FastAPI, Query, Form, File, UploadFile, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import List, Union
from enum import Enum
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import hashing
from crud import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


class Tags(Enum):
    users = "Users"
    products = "Products"
    friends = "Friends"
    pins = "Pins"
    security = "Security"


SECRET_KEY = "1d2f8417d0dfdbc7125e023d276c368a7fa7879df299ec87a71267b0386bdac0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(
    title="Lilas",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User, tags=[Tags.users.value])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User], tags=[Tags.users.value])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    print(f"Example Users: {users[0].friends}")
    return users


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(email: str, password: str, db: Session):
    user = crud.get_user_by_email(db, email)
    if not user:
        return False
    if not hashing.verify_password(password, user.hashed_password):
        return False
    return user


@app.post("/token", response_model=schemas.Token, tags=[Tags.security.value])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"Authenticating user with data: {form_data.username} and {form_data.password}")
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError as e:
        print(f"Error check: {e}")
        raise credentials_exception from e
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Account disabled")
    return current_user


@app.get("/users/me", response_model=schemas.User, tags=[Tags.users.value])
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/{user_id}", response_model=schemas.User, tags=[Tags.users.value])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/friends/add/{receiver_email}", response_model=schemas.Friend,
          tags=[Tags.friends.value])  # TODO: Create a friend code system instead of just email
def add_friend(receiver_email: str, current_user: schemas.User = Depends(get_current_active_user),
               db: Session = Depends(get_db)):
    sender_id = current_user.id
    receiver_user = crud.get_user_by_email(db, receiver_email)
    if not receiver_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No users with that Email",
            headers={"WWW-Authenticate": "Bearer"},
        )
    receiver_id = receiver_user.id
    return crud.create_friend(db=db, sender_id=sender_id, receiver_id=receiver_id)


@app.get("/friends/requests", response_model=List[schemas.Friend], tags=[Tags.friends.value])
def read_friend_requests(skip: int = 0, limit: int = 20, current_user: schemas.User = Depends(get_current_active_user),
                         db: Session = Depends(get_db)):
    friend_requests = crud.get_friend_requests(db=db, receiver_id=current_user.id, skip=skip, limit=limit)
    return friend_requests


@app.get("/friends/requests/all", response_model=List[schemas.Friend], tags=[Tags.friends.value])
def read_all_friend_requests(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    friend_requests = crud.get_all_friend_requests(db=db, skip=skip, limit=limit)
    return friend_requests


@app.patch("/friends/accept/{friend_id}", response_model=schemas.Friend, tags=[Tags.friends.value])
def accept_friend(friend_id: int, current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    friendship: schemas.Friend = crud.get_friend_by_id(db, friend_id=friend_id)
    if not friendship:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No pending request from that user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if current_user.id != friendship.receiver:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the receiver of this friend request",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return crud.accept_friend(db=db, friend_id=friend_id)


@app.get("/friends/accepted", response_model=List[schemas.User], tags=[Tags.friends.value])
def read_my_friends(current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    accepted_friend = crud.get_friends(db=db, receiver_id=current_user.id)
    return accepted_friend


# TODO: Everything below this point!

def is_pin_owner(user: schemas.User, pin: schemas.Pin):
    return user.pin_id == pin.id and pin.owner_id == user.id


@app.post("/pins/start", response_model=schemas.Pin, tags=[Tags.pins.value])
def start_pin_session(new_pin: schemas.Pin, current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return crud.create_pin(db=db, user=current_user, pin=new_pin)


@app.patch("/pins/end", response_model=schemas.Pin, tags=[Tags.pins.value])
def end_pin_session(end_time: datetime, current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    pin: schemas.Pin = current_user.pin
    pin.session_end_time = end_time
    if crud.update_pin(db=db, pin=pin):
        print("Updated pin successfully")
    else:
        print("Failed to update pin")
    return current_user.pin


@app.patch("/pins/join/{pin_id}", response_model=schemas.Pin, tags=[Tags.pins.value])
def join_pin_session(pin_id: int, current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    pin: schemas.Pin = crud.get_pin_by_id(db=db, pin_id=pin_id)
    pin.member_count += 1
    crud.update_pin(db=db, pin=pin)
    crud.user_join_pin(db=db, user_id=current_user.id, pin_id=pin_id)
    return crud.get_pin_by_id(db=db, pin_id=pin_id)


@app.patch("/pins/leave", response_model=schemas.Pin, tags=[Tags.pins.value])
def leave_pin_session():
    pass


@app.delete("/pins/delete/{pin_id}", response_model=schemas.Pin, tags=[Tags.pins.value])
def delete_pin_from_history():
    pass


@app.get("/pins/user_id/{user_id}", response_model=schemas.Pin, tags=[Tags.pins.value])
def get_pin_by_user_id():
    pass


@app.get("/pins/pin_id/{pin_id}", response_model=schemas.Pin, tags=[Tags.pins.value])
def get_pin_by_pin_id():
    pass


@app.get("/pins/available", response_model=list[schemas.Pin], tags=[Tags.pins.value])
def get_available_pins():
    pass


@app.get("/pins/me", response_model=schemas.Pin, tags=[Tags.pins.value])
def get_my_active_pin():
    pass


@app.get("/pins/history", response_model=List[schemas.Pin], tags=[Tags.pins.value])
def get_pin_history():
    pass
