from flask import Flask, render_template_string, request, redirect
from kerbian.db.connection import DatabaseConnection
from kerbian.db.models.user import User

app = Flask(__name__)
conn = DatabaseConnection.get_instance("default", "sqlite", path="kerbian.db").conn

TEMPLATE = """
<!doctype html>
<title>Kerbian Admin</title>
<h1>Users</h1>
<ul>
{% for u in users %}
  <li>{{u.id}}: {{u.username}} ({{u.email}})</li>
{% endfor %}
</ul>
<form action="/add" method="post">
  <input name="username" placeholder="Username">
  <input name="email" placeholder="Email">
  <button type="submit">Add</button>
</form>
"""

@app.route("/")
def index():
    users = User.all(conn)
    return render_template_string(TEMPLATE, users=users)

@app.route("/add", methods=["POST"])
def add():
    u = User()
    u.id = None  # auto-increment
    u.username = request.form["username"]
    u.email = request.form["email"]
    u.save(conn)
    return redirect("/")