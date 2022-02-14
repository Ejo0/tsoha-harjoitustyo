from db import db
from flask import session

def add_review(product_id, grade, content):
    user_id = session["user_id"]
    sql ="""INSERT INTO reviews (user_id, product_id, grade, content, created_at)
            VALUES (:user_id, :product_id, :grade, :content, NOW())"""
    try:
        db.session.execute(sql, {"user_id":user_id, "product_id":product_id, "grade":grade, "content":content})
        db.session.commit()
        return True
    except:
        return False

def get_reviews(product_id):
    sql ="""SELECT id, user_id, product_id, grade, content, created_at
            FROM reviews
            WHERE product_id=:product_id"""
    return db.session.execute(sql, {"product_id":product_id}).fetchall()
