from fastapi import FastAPI, Query, Form, File, UploadFile, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from typing import List
from schemas import Item, User, UserInDB
from enum import Enum
from database import fake_users_db


class Tags(Enum):
    files = "files"
    security = "security"
    users = "users"


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


def fake_hash_password(password: str):
    return "fakehashed" + password


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("/files/", tags=[Tags.files])
async def create_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/", tags=[Tags.files])
async def create_upload_files(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.put("/items/")
async def create_item(item: Item, buyer: str = Query(default=None, max_length=50)):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    if buyer:  # This could be a way to state where to put the item we created (ex: under a user's buying history)
        item_dict.update({"last_buyer": buyer})
    return item_dict


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
