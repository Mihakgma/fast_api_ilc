import datetime
# import functools
# from typing import Annotated, List, Callable
from typing import Annotated

import uvicorn

from fastapi import (FastAPI, Form, HTTPException, File, UploadFile,
                     BackgroundTasks, Cookie, Response, status, Depends)
from fastapi.responses import FileResponse, JSONResponse
from pydantic import ValidationError

from app.data.fake_dbs import feedbacks_db, fake_db
# from app.models.upload_excel_file import UploadExcelFile
from app.routes.navigate_strategy import navigate_info
from app.models.user import User
from app.models.feedback import Feedback
# from app.funct.test_functions import write_notification

app = FastAPI()


# def check_permissions(required_roles: List[int]) -> Callable:
#     """
#     Decorator to check user permissions based on roles.
#     """
#
#     def decorator(func: Callable):
#         @functools.wraps(func)
#         async def wrapper(*args, **kwargs):
#             session_token = kwargs.get('session_token')  # Get the session token from kwargs if available.
#
#             if not session_token:
#                 raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized: No session token.")
#
#             user = sessions.get(session_token)
#             if not user:
#                 raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                     detail="Unauthorized: Invalid session token.")
#
#             # Check if the user has at least one of the required roles.
#             if not any(role in user.roles for role in required_roles):
#                 raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                                     detail="Forbidden: Insufficient permissions.")
#
#             return await func(*args, **kwargs)
#
#         return wrapper
#
#     return decorator


@app.post('/feedback/')
async def get_feedback(feedback: Feedback) -> JSONResponse:
    feedbacks_db.append(feedback())
    return JSONResponse(content={"message": f"Feedback received. Thank you, {feedback.name}!"})


@app.get('/get_all_feedbacks/')
async def get_all_feedbacks(limit: int = 3) -> list[dict[str, str]]:
    return feedbacks_db[:limit]


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


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


# @app.post("/send-notification/{email}", dependencies=[Depends(check_permissions([4]))])
# async def send_notification(email: str,
#                             background_tasks: BackgroundTasks,
#                             session_token: str = Cookie()):
#     user = sessions.get(session_token)
#     if user:
#         background_tasks.add_task(write_notification, email, message="some notification")
#         return {"message": "Notification sent in the background"}
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}


# НЕОБХОДИМО РАЗОБРАТЬСЯ - КАКОЙ-ТО КОНФЛИКТ СО СХЕМАМИ - ПОДГРУЗКА ФАЙЛА ЧЕРЕЗ
# ПОТОК БАЙТОВЫХ ДАННЫХ ??? ГУГЛИТЬ!!!
# @app.post("/uploadfile/{file}/")
# async def excel_df_info(file: UploadExcelFile):
#     return {"df_info": file.df_info}

# AUTHORIZATION AND AUTENTIFICATION
# имитируем хранилище юзеров
# создали тестового юзера, якобы он уже зарегистрирован у нас
sample_user: dict = {"username": "user123", "password": "password123"}
fake_db: list[User] = [User(**sample_user)]
# имитируем хранилище сессий
# типа Redis
sessions: dict = {}


# основная логика программы
@app.post('/login')
async def login(user: User, response: Response):
    for person in fake_db:  # перебрали юзеров в нашем примере базы данных
        if person.username == user.username and person.password == user.password:  # сверили логин и пароль
            session_token = "abc123xyz456"
            # тут можно использовать модуль uuid (в продакшене),
            # или модуль random (для выполнения задания),
            # или самому написать рандомное значение куки, т.к. это пример тестовый
            sessions[
                session_token] = user
            # сохранили у себя в словаре сессию,
            # где токен - это ключ, а значение - объект юзера
            # тут установили куки с защищенным флагом httponly -
            # недоступны для вредоносного JS; флаг secure означает, что куки идут только по HTTPS
            response.set_cookie(key="session_token", value=session_token,
                                httponly=True)
            return {"message": "куки установлены"}
    return {
        # тут можно вернуть что хотите, в ТЗ не конкретезировалось, что делать, если логин/пароль неправильные
        "message": "Invalid username or password"}


@app.get('/user')
async def user_info(session_token=Cookie()):
    user = sessions.get(
        session_token)  # ищем в сессиях был ли такой токен создан, и если был, то возвращаем связанного с ним юзера
    if user:
        # у pydantic моделей есть метод dict(), который делает словарь из модели.
        # Можно сразу хранить словарь в сессии, не суть.
        # Для Pydantic версии > 2 метод переименован в model_dump()
        return user.dict()
    return {"message": "Unauthorized"}


if __name__ == "main":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True, workers=3)
