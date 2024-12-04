# from urllib import request

from fastapi import FastAPI, Form
from fastapi.responses import FileResponse

from navigate_strategy import navigate_info

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
def calculate(num1: int = Form(ge=0, lt=111111), num2: int = Form(ge=0, lt=111111)):
    print("num1 =", num1, "   num2 =", num2)
    return {"result": num1 + num2}

# @app.api_route("/hello/calculate", methods=["GET", "POST"])
# async def calculate(request: Request, num1: int = None, num2: int = None):
#     if request.method == "POST":
#         num1 = int(await request.form("num1"))
#         num2 = int(await request.form("num2"))
#     elif request.method == "GET":
#         try:
#             num1 = int(request.query_params["num1"])
#             num2 = int(request.query_params["num2"])
#         except (KeyError, ValueError):
#             raise HTTPException(status_code=400, detail="num1 and num2 are required query parameters for GET requests.")
#     else:
#         raise HTTPException(status_code=405, detail="Method Not Allowed") #Should never get here because of methods = ["GET","POST"] but good practice
#
#     print(f"num1: {num1}, num2: {num2}") # Check values
#     return {"result": num1 + num2}
