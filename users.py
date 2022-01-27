from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


def login(username, password):
    sql = "SELECT id, password, role FROM users WHERE username=:username"
    user = db.session.execute(sql, {"username":username}).fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["user_role"] = user.role
            return True
        else:
            return False

def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql ="""INSERT INTO users (username, password, role)
                VALUES (:username, :password, :role)"""
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["user_id"]
    del session["username"]
    del session["user_role"]

def get_role(role):
    try:
        return session["user_role"] == role
    except:
        return False