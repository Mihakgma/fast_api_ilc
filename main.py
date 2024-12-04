from fastapi import FastAPI
from fastapi.responses import FileResponse

from navigate_strategy import navigate_info

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    if name in navigate_info:
        return FileResponse(navigate_info[name])
    else:
        out = {"message": f"Hello {name}"}
        return out
