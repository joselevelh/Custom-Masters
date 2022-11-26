from fastapi import FastAPI
from schemas import ImagePost


post_db = {
    "josb": ["Tests", "test2"],
    "ceylan": ["test3"],
    "bongo": [],
}

app = FastAPI()


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
