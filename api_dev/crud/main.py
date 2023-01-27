from fastapi import FastAPI, Query, Form, File, UploadFile, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from typing import List, Union
from enum import Enum
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import hashing
import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


class Tags(Enum):
    files = "files"
    security = "security"
    users = "users"


SECRET_KEY = "1d2f8417d0dfdbc7125e023d276c368a7fa7879df299ec87a71267b0386bdac0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


#
# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items


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
    print(f"database: {db}")
    user = crud.get_user_by_email(db, email)
    if not user:
        return False
    if not hashing.verify_password(password, user.hashed_password):
        return False
    return user


@app.post("/token", response_model=schemas.Token)
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
    print(f"Got token: {token}")
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
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Account disabled")
    return current_user


@app.get("/users/me")
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/friends/add/{receiver_email}", response_model=schemas.Friend)  # TODO: Create a friend code system instead of just email
def add_friend(receiver_email: str, current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
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


@app.get("/friends/requests", response_model=List[schemas.Friend])
def read_friend_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    friends = crud.get_friends(db, user_id=2, skip=skip, limit=limit)
    return friends


@app.patch("/friends/accept/{friend_id}", response_model=schemas.Friend)
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


@app.get("/", tags=[Tags.files])
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
