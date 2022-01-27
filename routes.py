from flask import redirect, render_template, request
from app import app
import users

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        role = "admin" if request.form.get("create_admin") else "customer"
        if password1 != password2:
            return render_template("register.html", error_message = "Tarkista salasana")
        else:
            if users.register(username, password1, role):
                if role == "customer":
                    return redirect("/")
                if role == "admin":
                    return redirect("/admin")
            else:
                return render_template("register.html", error_message = "Käyttäjätunnus ei kelpaa")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("login.html", error_message = "Väärä tunnus tai salasana")
        elif users.get_role("customer"):
            return redirect("/")
        elif users.get_role("admin"):
            return redirect("/admin")

@app.route('/logout')
def logout():
    users.logout()
    return redirect("/")

@app.route('/admin')
def admin_index():
    if users.get_role("admin"):
        return render_template("admin/index.html")
    else:
        return render_template("login.html", error_message = "Adminiin pääsy vain ylläpitäjän tunnuksilla!")
