from fastapi import FastAPI, Query, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from typing import List
from schemas import Item

app = FastAPI()


@app.post("/files/")
async def create_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
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

@app.get("/")
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