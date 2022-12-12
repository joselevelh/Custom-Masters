from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas import ImagePost, User

post_db = {
    "josb": ["Tests", "test2"],
    "ceylan": ["test3"],
    "bongo": [],
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


# --------------------------------------------------
@app.get("/test")
async def get_test(username: str, post_id: int):
    return f"{username}, {str(post_id)} success!"


@app.get("/test2/{username}/{post_id}")
async def get_test(username: str, post_id: int):
    return f"{username}, {str(post_id)} success!"


@app.post("/post/")
async def create_image_post(post: ImagePost):
    if post.username in post_db:
        post_db[post.username].append(post)
        return post
    else:
        print("ERROR should be returned since username does not exist in db")
        return post


@app.get("/post/submit")
async def get_image_post(username: str, post_id: int):
    if username in post_db:
        post = post_db[username][post_id]  # TODO: Will throw error if doesnt exist, we should fix that
        return post
    else:
        print("ERROR should be returned since username does not exist in db")
        return "error"
