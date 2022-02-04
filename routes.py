from flask import redirect, render_template, request
from app import app
import users
import products
import cart
import orders

@app.route('/')
def index():
    product_list = products.get_all_products()
    return render_template("index.html", products = product_list)

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

@app.route('/product/<int:product_id>')
def show_product(product_id):
    product = products.get_product(product_id)
    return render_template("product.html", product = product)

@app.route('/add_to_cart', methods=["POST"])
def add_to_cart():
    user_id = request.form["user_id"]
    product_id = request.form["product_id"]
    quantity = request.form["quantity"]
    cart.add_to_cart(user_id, product_id, quantity)
    return redirect("/product/" + product_id)

@app.route('/user/<int:user_id>')
def user(user_id):
    if not users.get_role("customer") or users.get_user_id() != user_id:
        return redirect("/")
    else:
        items = cart.get_cart_items(user_id)
        order_list = orders.get_orders(user_id)
        return render_template("user.html", items = items, order_list = order_list)

@app.route('/user/<int:user_id>/checkout', methods=["GET", "POST"])
def checkout(user_id):
    if not users.get_role("customer") or users.get_user_id() != user_id:
        return redirect("/")
    items = cart.get_cart_items(user_id)
    if request.method == "GET":
        return render_template("checkout.html", items = items)
    if request.method == "POST":
        if items and str(items) == request.form["items"]:
            orders.create_order(items, user_id)
        return redirect(f"/user/{user_id}")

@app.route('/delete', methods=["POST"])
def delete():
    cart.delete_cart_item(request.form["cart_item_id"])
    return redirect("user/" + request.form["user_id"])

@app.route('/admin')
def admin_index():
    if users.get_role("admin"):
        return render_template("admin/index.html")
    else:
        return render_template("login.html", error_message = "Adminiin pääsy vain ylläpitäjän tunnuksilla!")

@app.route('/admin/products', methods=["GET", "POST"])
def admin_products():
    if not users.get_role("admin"):
        return render_template("login.html", error_message = "Adminiin pääsy vain ylläpitäjän tunnuksilla!")
    product_list = products.get_all_products()
    if request.method == "GET":
        return render_template("admin/products.html", products = product_list)
    elif request.method == "POST":
        creator_id = int(request.form["user_id"])
        name = request.form["name"]
        price = float(request.form["price"])
        description = request.form["description"]
        if products.add_product(creator_id, name, price, description):
            return redirect("/admin/products")
        else:
            return render_template("/admin/products.html", products = product_list, error_message = "Tarkista syöte!")

@app.route('/admin/orders', methods=["GET", "POST"])
def admin_orders():
    if not users.get_role("admin"):
        return render_template("login.html", error_message = "Adminiin pääsy vain ylläpitäjän tunnuksilla!")
    orders_list = orders.get_orders()
    if request.method == "GET":
        return render_template("admin/orders.html", order_list = orders_list)
    if request.method == "POST":
        order_id = request.form["order_id"]
        orders.process_order(order_id)
        return redirect("/admin/orders")