from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test/{test_id}")
def read_item(test_id: int, paramstr: Union[str, None] = None):
    return {"test_id": test_id, "paramstr": paramstr}