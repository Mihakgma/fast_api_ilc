import datetime

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from pydantic import ValidationError

from app.routes.navigate_strategy import navigate_info
from app.models.models import User

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    if name in navigate_info:
        file_path = navigate_info[name]  # Get the path from your dictionary
        # Important: Check if the file exists before trying to serve it
        try:
            with open(file_path, 'r'):
                pass  # Simple file existence check
            return FileResponse(file_path)  # Only serve if the file exists
        except FileNotFoundError:
            return {"error": f"HTML file '{file_path}' not found."}  # Handle file not found
    else:
        out = {"message": f"Hello {name}"}
        return out


@app.post("/hello/calculate")
async def calculate(num1: int = Form(ge=0, lt=111111), num2: int = Form(ge=0, lt=111111)):
    print("num1 =", num1, "   num2 =", num2)
    return {"result": num1 + num2}


@app.post("/hello/create_new_user")
async def create_new_user(first_name: str = Form(),
                          birth_date: str = Form(),
                          phone: str = Form(),):
    try:
        birth_date = datetime.datetime.fromisoformat(birth_date)  # Explicit conversion
        user = User(first_name=first_name, birth_date=birth_date, phone=phone)
        user_info = "   ".join([f"{k}: {v}" for (k, v) in user.dict().items()])
        return {"user_info &#10;": user_info}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))  # Unprocessable Entity
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")  # Bad Request
    except Exception as e:  # Catch other unexpected exceptions
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")  # Internal Server Error
