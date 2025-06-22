from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.sessions import SessionMiddleware
from kerbian.db.models.user import User
from kerbian.db.connection import DatabaseConnection
import secrets

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32))

def get_db():
    return DatabaseConnection.get_instance("default", "sqlite", path="kerbian.db").conn

def is_logged_in(request: Request):
    return request.session.get("user_id") is not None

@app.get("/admin/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return """
    <form method="post" action="/admin/login">
      <input name="username" placeholder="Username">
      <input name="password" type="password" placeholder="Password">
      <button type="submit">Login</button>
    </form>
    """

@app.post("/admin/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = get_db()
    users = User.all(conn)
    user = next((u for u in users if u.username == username and u.password == password), None)
    if user:
        request.session["user_id"] = user.id
        return RedirectResponse("/admin", status_code=302)
    return HTMLResponse("Invalid credentials", status_code=401)

@app.get("/admin")
async def admin_home(request: Request):
    if not is_logged_in(request):
        return RedirectResponse("/admin/login")
    # Render admin dashboard here
    return HTMLResponse(f"<h1>Welcome user {request.session['user_id']}!</h1>")