from fastapi import FastAPI, HTTPException, Request, Form
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette import status

app = FastAPI()
users = []
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int = None
    username: str
    age: int = None


@app.get("/")
async def get_user(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get(path="/user/{user_id}")
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        user = next((u for u in users if u.id == user_id), None)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return templates.TemplateResponse("users.html", {"request": request, "user": user})
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/", status_code=status.HTTP_201_CREATED)
async def post_user(request: Request, username: str = Form(...), age: int = Form(...)) -> HTMLResponse:
    if users:
        user_id = max(users, key=lambda u: u.id).id + 1
    else:
        user_id = 0
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.put("/user/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(request: Request, user_id: int, username: str = Form(...), age: int = Form(...)) -> HTMLResponse:
    user = next((u for u in users if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    user.username = username
    user.age = age
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.delete("/user/{user_id}")
async def delete_user(user_id: int) -> str:
    user = next((u for u in users if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    users.remove(user)
    return f"User with ID {user_id} was deleted."
