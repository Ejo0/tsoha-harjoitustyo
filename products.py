from db import db

def get_all_products():
    sql = "SELECT * FROM products"
    return db.session.execute(sql).fetchall()

def add_product(creator_id, name, price, description):
    sql = """INSERT INTO products (creator_id, name, price, description, created_at)
            VALUES (:creator_id, :name, :price, :description, NOW())"""
    try:
        db.session.execute(sql, {"creator_id":creator_id, "name":name, "price":price, "description":description})
        db.session.commit()
        return True
    except:
        return False

def get_product(product_id):
    sql = "SELECT * FROM products WHERE id = :product_id;"
    return db.session.execute(sql, {"product_id": product_id}).fetchone()
