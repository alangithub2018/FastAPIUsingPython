from fastapi import FastAPI, status, Request, Response, HTTPException, Depends
from fastapi.responses import PlainTextResponse, JSONResponse
from typing import List, Optional
import jwt
from models.Developer import Developer
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
# from uvicorn import run

app = FastAPI()
developers = []

async def connection():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["developers"]
    return db

users = [
    {
        "id": 1,
        "name": "Juan",
        "password": "1234",
        "age": 25
    },
    {
        "id": 2,
        "name": "Ana",
        "password": "1234",
        "age": 20
    }
]

def verify_token(request: Request):
    token = request.headers.get("Authorization")
    data = jwt.decode(token, "my_secret_key", algorithms=["HS256"])
    for user in users:
        if user["name"] == data["name"] and user["password"] == data["password"]:
            return True
    return False

# is_logged = True

# @app.middleware("http")
# async def check_logged(request: Request, call_next):
#     if not is_logged:
#         return JSONResponse(content={"message": "You are not logged"}, status_code=401)
#     response = await call_next(request)
#     return response

@app.post("/login")
def login(username: str, password: str):
    for user in users:
        if user["name"] == username and user["password"] == password:
            return jwt.encode(user, "my_secret_key", algorithm="HS256")
    return {"message": "Invalid credentials"}

# @app.get("/developers")
# def get_developers(authorized: bool = Depends(verify_token)):
#     if authorized:
#         return developers
#     else:
#         return {"message": "You are not authorized"}

@app.get("/developers")
async def get_developers():
    try:
        db = await connection()
        developers = await db["developers"].find().to_list(1000)
        for developer in developers:
            developer["_id"] = str(developer["_id"])
        return JSONResponse(content={"data": developers}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

# @app.get("/developers/{id}")
# def get_developer(id: int):
#     for developer in developers:
#         if developer.id == id:
#             return developer
#     return {"message": "Developer not found"}

@app.get("/developers/{id}")
async def get_developer(id: str):
    try:
        db = await connection()
        developer = await db["developers"].find_one({"_id": ObjectId(id)})
        if not developer:
            return JSONResponse(content={"message": "Developer not found"}, status_code=404)
        developer["_id"] = str(developer["_id"])
        return JSONResponse(content={"data": developer}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

# @app.get("/developers/{id}/skills")
# def get_skills(id: int):
#     for developer in developers:
#         if developer.id == id:
#             return developer.skills
#     return {"message": "Developer not found"}

@app.get("/developers/{id}/skills")
async def get_skills(id: str):
    try:
        db = await connection()
        developer = await db["developers"].find_one({"_id": ObjectId(id)})
        if not developer:
            return JSONResponse(content={"message": "Developer not found"}, status_code=404)
        developer["_id"] = str(developer["_id"])
        return JSONResponse(content={"data": developer["skills"]}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

# @app.get("/developers/{id}/experience")
# def get_experience(id: int):
#     for developer in developers:
#         if developer.id == id:
#             return developer.experience
#     return {"message": "Developer not found"}

@app.get("/developers/{id}/experience")
async def get_experience(id: str):
    try:
        db = await connection()
        developer = await db["developers"].find_one({"_id": ObjectId(id)})
        if not developer:
            return JSONResponse(content={"message": "Developer not found"}, status_code=404)
        developer["_id"] = str(developer["_id"])
        return JSONResponse(content={"data": developer["experience"]}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

# @app.get("/developers/{id}/languages")
# def get_languages(id: int):
#     for developer in developers:
#         if developer.id == id:
#             return developer.languages
#     return {"message": "Developer not found"}

@app.get("/developers/{id}/languages")
async def get_languages(id: str):
    try:
        db = await connection()
        developer = await db["developers"].find_one({"_id": ObjectId(id)})
        if not developer:
            return JSONResponse(content={"message": "Developer not found"}, status_code=404)
        developer["_id"] = str(developer["_id"])
        return JSONResponse(content={"data": developer["languages"]}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

# @app.post("/developers")
# def create_developer(developer: Developer):
#     if len(developer.name) > 5:
#         raise HTTPException(status_code=400, detail="Name is too long")
#     if developer.age > 100:
#         raise HTTPException(status_code=400, detail="Age is too high")
#     if len(developer.skills) == 0:
#         raise HTTPException(status_code=400, detail="Skills are required")
#     developers.append(developer)
#     return JSONResponse(status_code=201, content={"message": "Developer created"})

@app.post("/developers")
async def create_developer(developer: Developer):
    try:
        db = await connection()
        collection = db["developers"]
        result = await collection.insert_one(jsonable_encoder(developer))
        return JSONResponse(status_code=201, content={"message": "Developer created"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

# @app.put("/developers/{id}")
# def update_developer(data: Developer, id: int):
#     for developer in developers:
#         if developer.id == id:
#             developer.name = data.name
#             developer.country = data.country
#             developer.age = data.age
#             developer.skills = data.skills
#             developer.experience = data.experience
#             developer.languages = data.languages
#             return developers
#     return {"message": "Developer not found"}

@app.put("/developers/{id}")
async def update_developer(data: Developer, id: str):
    try:
        db = await connection()
        developer = await db["developers"].find_one({"_id": ObjectId(id)})
        if not developer:
            return JSONResponse(content={"message": "Developer not found"}, status_code=404)
        await db.developers.update_one({"_id": ObjectId(id)}, {"$set": jsonable_encoder(data)})
        return JSONResponse(content={"message": "Developer updated"}, status_code=201)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

# @app.delete("/developers/{id}")
# def delete_developer(id: int):
#     for developer in developers:
#         if developer.id == id:
#             developers.remove(developer)
#             return developers
#     return {"message": "Developer not found"}

@app.delete("/developers/{id}")
async def delete_developer(id: str):
    try:
        db = await connection()
        developer = await db["developers"].find_one({"_id": ObjectId(id)})
        if not developer:
            return JSONResponse(content={"message": "Developer not found"}, status_code=404)
        await db.developers.delete_one({"_id": ObjectId(id)})
        return JSONResponse(content={"message": "Developer deleted"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

@app.get("/")
def message():
    return {"message": "Hello World!"}

@app.get("/users")
def get_users():
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int, age: int, name: Optional[str] = None):
    if not name:
        print("Name was not provided")

    for user in users:
        if user["id"] == user_id and user["age"] == age:
            return user
    return {"message": "User not found"}

@app.get("/welcome/{name}/{last_name}")
def welcome_message(name: str, last_name: str):
    return {"message": f"Welcome {name.upper()} {last_name}"}

@app.get("/sum/{num1}/{num2}")
def sum(num1: int, num2: int, response: Response):
    addition = num1 + num2
    if addition > 0:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return {"result": addition}

# if __name__ == "__main__":
#     run(app, host="127.0.0.1", port=3000)

