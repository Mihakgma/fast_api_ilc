import datetime

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from pydantic import ValidationError

from app.routes.navigate_strategy import navigate_info
from app.models.models import User

app = FastAPI()

fake_db = [{"user_name": "vasya", "user_info": "любит колбасу"},
           {"user_name": "katya", "user_info": "любит петь"},
           {"user_name": "gladiko", "user_info": "likes pizza"},
           {"user_name": "ilon musk", "user_info": "likes tesla"},
           {"user_name": "pashka durov", "user_info": "likes telega"}]


@app.get("/users/{user_idx}")
def read_user(user_idx: int):
    if user_idx in [i for i in range(len(fake_db))]:
        return fake_db[user_idx]
    return {"error": f"Sorry. User with index <{user_idx}> has not been found..."}


@app.get('/users')
async def get_all_users(limit: int = 3):
    return fake_db[:limit]


@app.post('/add_user')
async def add_user(user_name: str,
                   user_info: str):
    new_user_info = {"user_name": user_name, "user_info": user_info}
    if new_user_info in fake_db:
        return {"message": f"юзер <{user_name}> УЖЕ СОДЕРЖИТСЯ в базе данных!"}
    fake_db.append(new_user_info)
    return {"message": f"юзер <{user_name}> успешно добавлен в базу данных"}


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
                          phone: str = Form(), ):
    try:
        birth_date = datetime.datetime.fromisoformat(birth_date)  # Explicit conversion
        user = User(first_name=first_name, birth_date=birth_date, phone=phone)
        user_info = "   ".join([f"{k}: {v}" for (k, v) in user.dict().items()])
        return {"user_info: ": user_info}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))  # Unprocessable Entity
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")  # Bad Request
    except Exception as e:  # Catch other unexpected exceptions
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")  # Internal Server Error


if __name__ == "main":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
