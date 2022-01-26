from flask import redirect, render_template, request
from app import app
import users

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", error_message="Väärä tunnus tai salasana")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        role = request.form["role"]
        if password1 != password2:
            return render_template("register.html", error_message="Tarkista salasana")
        else:
            if users.register(username, password1, role):
                return redirect("/")
            else:
                return render_template("register.html", error_message="Käyttäjätunnus ei kelpaa")

@app.route('/logout')
def logout():
    users.logout()
    return redirect("/")
