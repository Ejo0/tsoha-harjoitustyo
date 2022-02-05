from flask import redirect, render_template, request
from app import app
import users
import products
import cart
import orders

@app.route('/')
def index():
    product_list = products.get_active_products()
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
        elif users.get_role() == "customer":
            return redirect("/")
        elif users.get_role() == "admin":
            return redirect("/admin")

@app.route('/logout')
def logout():
    users.logout()
    return redirect("/")

@app.route('/product/<int:product_id>')
def show_product(product_id):
    product = products.get_product(product_id)
    if not product.active:
        return redirect('/')
    return render_template("product.html", product = product)

@app.route('/add_to_cart', methods=["POST"])
def add_to_cart():
    users.check_csrf()

    quantity = request.form["quantity"]
    product_id = request.form["product_id"]
    if not products.is_active(product_id):
        return redirect('/')

    cart.add_to_cart(users.get_user_id(), product_id, quantity)
    return redirect("/product/" + product_id)

@app.route('/user/<int:user_id>')
def user(user_id):
    users.require_role("customer")
    users.confirm_id(user_id)
    
    items = cart.get_cart_items(user_id)
    order_list = orders.get_orders(user_id)
    return render_template("user.html", items = items, order_list = order_list)

@app.route('/user/<int:user_id>/checkout', methods=["GET", "POST"])
def checkout(user_id):
    users.require_role("customer")
    users.confirm_id(user_id)

    items = cart.get_cart_items(user_id)
    if request.method == "GET":
        return render_template("checkout.html", items = items)
    if request.method == "POST":
        users.check_csrf()

        if items and str(items) == request.form["items"]:
            orders.create_order(items, user_id)
        return redirect(f"/user/{user_id}")

@app.route('/delete_cart_item', methods=["POST"])
def delete_cart_item():
    users.check_csrf()

    cart.delete_cart_item(request.form["cart_item_id"])
    return redirect("user/" + request.form["user_id"])

@app.route('/admin', methods=["GET", "POST"])
def admin_products():
    if not users.get_role() == "admin":
        return render_template("login.html", error_message = "Adminiin pääsy vain ylläpitäjän tunnuksilla!")

    product_list = products.get_all_products()
    if request.method == "GET":
        return render_template("admin/index.html", products = product_list)

    elif request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        price = float(request.form["price"])
        description = request.form["description"]
        if products.add_product(users.get_user_id(), name, price, description):
            return redirect("/admin")
        else:
            return render_template("admin/index.html", products = product_list, error_message = "Tarkista syöte!")

@app.route('/admin/orders', methods=["GET", "POST"])
def admin_orders():
    if not users.get_role() == "admin":
        return render_template("login.html", error_message = "Adminiin pääsy vain ylläpitäjän tunnuksilla!")

    orders_list = orders.get_orders()
    if request.method == "GET":
        return render_template("admin/orders.html", order_list = orders_list)

    if request.method == "POST":
        users.check_csrf()

        order_id = request.form["order_id"]
        orders.process_order(order_id)
        return redirect("/admin/orders")

@app.route('/admin/product/<int:id>', methods=["GET", "POST"])
def admin_product(id):
    if not users.get_role() == "admin":
        return render_template("login.html", error_message = "Adminiin pääsy vain ylläpitäjän tunnuksilla!")

    product = products.get_product(id)
    if request.method == "GET":
        return render_template("admin/product.html", product = product)

    if request.method == "POST":
        users.check_csrf()
        new_name = request.form["name"]
        new_price = request.form["price"]
        new_description = request.form["description"]
        is_active = "active" in request.form
        if not new_name: new_name = product.name
        if not new_price: new_price = product.price
        if not new_description: new_description = product.description
        if products.edit_product(product.id, new_name, new_price, new_description, is_active):
            return redirect(f'/admin/product/{id}')
        else:
            return render_template('admin/product.html', product = product, error_message = "Tarkista syöte!")
