from flask import redirect, render_template, request
from app import app
from services import users, products, cart, orders, reviews

@app.route("/")
def index():
    product_list = products.get_active_products()
    return render_template("index.html", products=product_list)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        role = "admin" if request.form.get("create_admin") else "customer"
        if len(username) not in range(1,21):
            return render_template("register.html",
                                   error_message="Käyttäjätunnuksen tulee olla 1-20 merkkiä pitkä")
        if password1 != password2:
            return render_template("register.html", error_message="Salasanat eivät täsmää")
        if len(password1) not in range(5,51):
            return render_template("register.html",
                                   error_message="Salasanan tulee olla 5-50 merkkiä pitkä")

        if users.register(username, password1, role):
            if role == "customer":
                return redirect("/")
            if role == "admin":
                return redirect("/admin")
            return render_template("register.html", error_message="Tunnuksella löytyy jo käyttäjä")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("login.html", error_message="Väärä tunnus tai salasana")
        if users.get_role() == "customer":
            return redirect("/")
        if users.get_role() == "admin":
            return redirect("/admin")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/product/<int:product_id>")
def show_product(product_id):
    product = products.get_product(product_id)
    if not product or not product.active:
        return redirect("/")
    reviews_list = reviews.get_reviews(product_id)
    avg_grade = reviews.get_average_grade(product_id)
    review_count = reviews.get_review_count(product_id)
    return render_template("product.html", product=product, reviews_list=reviews_list,
                           avg_grade=avg_grade, review_count=review_count)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    users.check_csrf()

    product_id = request.form["product_id"]
    try:
        quantity = int(request.form["quantity"])
    except:
        return redirect("/product/" + product_id)

    if not products.is_active(product_id) or quantity not in range(1, 51):
        return redirect("/")

    cart.add_to_cart(users.get_user_id(), product_id, quantity)
    return redirect("/product/" + product_id)

@app.route("/user/<int:user_id>")
def user(user_id):
    users.require_role("customer")
    users.confirm_id(user_id)

    items = cart.get_cart_items(user_id)
    order_list = orders.get_orders(user_id)
    return render_template("user.html", items=items, order_list=order_list)

@app.route("/user/<int:user_id>/checkout", methods=["GET", "POST"])
def checkout(user_id):
    users.require_role("customer")
    users.confirm_id(user_id)

    items = cart.get_cart_items(user_id)
    if request.method == "GET":
        return render_template("checkout.html", items=items)
    if request.method == "POST":
        users.check_csrf()

        if items and str(items) == request.form["items"]:
            orders.create_order(items, user_id)
        return redirect(f"/user/{user_id}")

@app.route("/delete_cart_item", methods=["POST"])
def delete_cart_item():
    users.check_csrf()

    cart.delete_cart_item(request.form["cart_item_id"])
    return redirect(f"/user/{users.get_user_id()}")

@app.route("/add_review", methods=["POST"])
def add_review():
    users.check_csrf()

    product_id = request.form["product_id"]
    content = request.form["content"]
    try:
        grade = int(request.form["grade"])
        if grade in [1,2,3,4,5] and len(content) in range(1,501) and products.is_active(product_id):
            reviews.add_review(product_id, grade, content)
    except:
        pass
    return redirect(f"/product/{product_id}")

@app.route("/admin", methods=["GET", "POST"])
def admin_products():
    if not users.get_role() == "admin":
        return render_template("login.html",
                               error_message="Adminiin pääsy vain ylläpitäjän tunnuksilla!")

    product_list = products.get_all_products()
    def render_with_error(error_message):
        return render_template("admin/index.html", products=product_list,
                               error_message=error_message)

    if request.method == "GET":
        return render_template("admin/index.html", products=product_list)

    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        if len(name) not in range(1, 31):
            return render_with_error("Nimen tulee olla 1-30 merkkiä pitkä")

        try:
            price = float(request.form["price"])
        except:
            return render_with_error("""Hinnan tulee olla kokonais- tai
                                     desimaaliluku pisteellä eroteltuna""")
        if price <= 0 or price > 1_000_000:
            return render_with_error("Hinnan tulee olla positiivinen ja korkeintaan miljoona")

        description = request.form["description"]
        if len(description) not in range(1, 500):
            return render_with_error("Kuvauksen tulee olla 1-500 merkkiä pitkä")

        if products.add_product(users.get_user_id(), name, price, description):
            return redirect("/admin")
        else:
            return render_with_error(f"Tuote '{name}' on jo verkkokaupassa")

@app.route("/admin/orders", methods=["GET", "POST"])
def admin_orders():
    if not users.get_role() == "admin":
        return render_template("login.html",
                               error_message="Adminiin pääsy vain ylläpitäjän tunnuksilla!")

    orders_list = orders.get_orders()
    if request.method == "GET":
        return render_template("admin/orders.html", order_list=orders_list)

    if request.method == "POST":
        users.check_csrf()

        order_id = request.form["order_id"]
        orders.process_order(order_id)
        return redirect("/admin/orders")

@app.route("/admin/product/<int:id>")
def admin_product(id):
    if not users.get_role() == "admin":
        return render_template("login.html",
                               error_message="Adminiin pääsy vain ylläpitäjän tunnuksilla!")
    return _admin_product_with_message(id, None)

@app.route("/admin/product/<int:id>/update", methods=["POST"])
def admin_product_update(id):
    users.check_csrf()
    if not users.get_role() == "admin":
        return render_template("login.html",
                               error_message="Adminiin pääsy vain ylläpitäjän tunnuksilla!")

    product = products.get_product(id)
    if not product:
        return redirect("/admin")

    new_name = request.form["name"] if request.form["name"] else product.name
    if len(new_name) > 30:
        return _admin_product_with_message(id, "Nimen tulee olla korkeintaan 30 merkkiä pitkä")

    new_description = request.form["description"] if request.form["description"] else product.description
    if len(new_description) > 500:
        return _admin_product_with_message(id, "Kuvauksen tulee olla korkeintaan 500 merkkiä")

    new_price = request.form["price"] if request.form["price"] else product.price
    try:
        new_price = float(new_price)
    except:
        return _admin_product_with_message(id, "Hinnan tulee olla desimaaliluku")
    if new_price < 0 or new_price > 1_000_000:
        return _admin_product_with_message(id,"""Hinnan tulee olla positiivinen
                                           ja korkeintaan miljoona euroa""")

    is_active = "active" in request.form
    if products.edit_product(product.id, new_name, new_price, new_description, is_active):
        return redirect(f"/admin/product/{id}")
    return _admin_product_with_message(id, f"Tuote {new_name} on jo verkkokaupassa")

def _admin_product_with_message(id, message):
    product = products.get_product(id)
    if not product:
        return redirect("/admin")
    avg_grade = reviews.get_average_grade(id)
    review_count = reviews.get_review_count(id)
    return render_template("admin/product.html", product=product, avg_grade=avg_grade,
                           review_count=review_count, error_message=message)
