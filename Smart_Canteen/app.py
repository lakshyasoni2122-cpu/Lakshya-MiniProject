from flask import Flask, render_template, request, redirect, url_for

from data import menu, categories, payment_methods, order_statuses

from functions import (
    get_available_foods,
    get_categories,
    filter_by_category,
    search_food,
    add_to_cart,
    increase_quantity,
    decrease_quantity,
    remove_from_cart,
    calculate_bill,
    generate_order_id,
    update_order_status,
    calculate_total_sales
)


# ==========================================
# FLASK APPLICATION
# ==========================================

app = Flask(__name__)


# ==========================================
# CART
# ==========================================

cart = []


# ==========================================
# ORDERS
# ==========================================

orders = []

order_number = 1001


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    available_foods = get_available_foods()

    category_list = get_categories()

    return render_template(
        "index.html",
        menu=available_foods,
        categories=category_list,
        cart=cart
    )


# ==========================================
# SEARCH
# ==========================================

@app.route("/search", methods=["POST"])
def search():

    search_text = request.form.get(
        "search_text",
        ""
    )

    result = search_food(search_text)

    category_list = get_categories()

    return render_template(
        "index.html",
        menu=result,
        categories=category_list,
        cart=cart
    )


# ==========================================
# CATEGORY
# ==========================================

@app.route("/category/<category_name>")
def category(category_name):

    result = filter_by_category(
        category_name
    )

    category_list = get_categories()

    return render_template(
        "index.html",
        menu=result,
        categories=category_list,
        cart=cart
    )


# ==========================================
# ADD TO CART
# ==========================================

@app.route("/add/<int:food_id>", methods=["POST"])
def add(food_id):

    quantity = request.form.get(
        "quantity",
        "1"
    )

    try:

        quantity = int(quantity)

    except ValueError:

        quantity = 1


    add_to_cart(
        cart,
        food_id,
        quantity
    )

    return redirect(
        url_for("home")
    )


# ==========================================
# CART
# ==========================================

@app.route("/cart")
def view_cart():

    bill = calculate_bill(cart)

    return render_template(
        "index.html",
        menu=menu,
        categories=categories,
        cart=cart,
        bill=bill
    )


# ==========================================
# INCREASE
# ==========================================

@app.route("/increase/<int:food_id>")
def increase(food_id):

    increase_quantity(
        cart,
        food_id
    )

    return redirect(
        url_for("view_cart")
    )


# ==========================================
# DECREASE
# ==========================================

@app.route("/decrease/<int:food_id>")
def decrease(food_id):

    decrease_quantity(
        cart,
        food_id
    )

    return redirect(
        url_for("view_cart")
    )


# ==========================================
# REMOVE
# ==========================================

@app.route("/remove/<int:food_id>")
def remove(food_id):

    remove_from_cart(
        cart,
        food_id
    )

    return redirect(
        url_for("view_cart")
    )


# ==========================================
# PLACE ORDER
# ==========================================

@app.route("/place-order", methods=["POST"])
def place_order():

    global order_number


    if len(cart) == 0:

        return redirect(
            url_for("home")
        )


    customer_name = request.form.get(
        "customer_name",
        "Customer"
    )


    payment_method = request.form.get(
        "payment_method",
        "Cash"
    )


    bill = calculate_bill(cart)


    order_id = generate_order_id(
        order_number
    )


    order = {

        "order_id": order_id,

        "customer_name": customer_name,

        "items": cart.copy(),

        "subtotal": bill["subtotal"],

        "discount": bill["discount"],

        "gst": bill["gst"],

        "total": bill["total"],

        "payment_method": payment_method,

        "status": "Preparing"

    }


    orders.append(order)


    order_number += 1


    cart.clear()


    return render_template(
        "index.html",
        menu=menu,
        categories=categories,
        cart=cart,
        order=order
    )


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@app.route("/admin")
def admin():

    total_orders = len(orders)

    total_sales = calculate_total_sales(
        orders
    )


    return render_template(
        "index.html",
        menu=menu,
        categories=categories,
        cart=cart,
        orders=orders,
        admin=True,
        total_orders=total_orders,
        total_sales=total_sales,
        order_statuses=order_statuses
    )


# ==========================================
# UPDATE ORDER STATUS
# ==========================================

@app.route(
    "/update-status/<order_id>",
    methods=["POST"]
)
def change_status(order_id):

    new_status = request.form.get(
        "status"
    )


    if new_status in order_statuses:

        update_order_status(
            orders,
            order_id,
            new_status
        )


    return redirect(
        url_for("admin")
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)