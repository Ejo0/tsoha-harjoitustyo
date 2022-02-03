from flask import session
from db import db
import cart

def get_orders(user_id):
    sql = "SELECT * FROM order_details WHERE user_id=:user_id"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def create_order(items, user_id):
    try:
        order_id = _initialize_new_order_detail(user_id)
        _initialize_new_order_items(items, order_id)
        db.session.commit()
        cart.clear_cart(user_id)
        return True
    except:
        return False

def _initialize_new_order_detail(user_id):
    sum = session["cart_sum"]
    sql ="""INSERT INTO order_details (user_id, total_sum, order_state, created_at)
            VALUES (:user_id, :total_sum, :order_state, NOW())
            RETURNING id"""
    return db.session.execute(sql, {"user_id":user_id, "total_sum":sum, "order_state":"created"}).fetchone()[0]

def _initialize_new_order_items(items, order_id):
    for item in items:
            product_id = item["product_id"]
            quantity = item["quantity"]
            unit_price = item["price"]
            sql ="""INSERT INTO order_items (order_id, product_id, quantity, unit_price, created_at)
                    VALUES (:order_id, :product_id, :quantity, :unit_price, NOW())"""
            db.session.execute(sql, {"order_id":order_id, "product_id":product_id, "quantity":quantity, "unit_price":unit_price })
