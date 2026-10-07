from data import menu


# ==========================================
# 1. FIND FOOD
# ==========================================

def find_food(food_id):

    for food in menu:

        if food["id"] == food_id:

            return food

    return None


# ==========================================
# 2. AVAILABLE FOODS
# ==========================================

def get_available_foods():

    available_foods = []

    for food in menu:

        if food["available"] == True:

            available_foods.append(food)

    return available_foods


# ==========================================
# 3. GET CATEGORIES
# ==========================================

def get_categories():

    category_list = []

    for food in menu:

        category = food["category"]

        if category not in category_list:

            category_list.append(category)

    return category_list


# ==========================================
# 4. FILTER FOOD
# ==========================================

def filter_by_category(category):

    filtered_foods = []

    for food in menu:

        if category == "All":

            filtered_foods.append(food)

        elif food["category"] == category:

            filtered_foods.append(food)

    return filtered_foods


# ==========================================
# 5. SEARCH FOOD
# ==========================================

def search_food(search_text):

    result = []

    search_text = search_text.lower()

    for food in menu:

        name = food["name"].lower()

        category = food["category"].lower()

        if search_text in name or search_text in category:

            result.append(food)

    return result


# ==========================================
# 6. ADD TO CART
# ==========================================

def add_to_cart(cart, food_id, quantity):

    food = find_food(food_id)

    if food is None:

        return cart


    if food["available"] == False:

        return cart


    if quantity <= 0:

        return cart


    for item in cart:

        if item["id"] == food_id:

            item["quantity"] += quantity

            return cart


    cart_item = {

        "id": food["id"],

        "name": food["name"],

        "price": food["price"],

        "quantity": quantity

    }

    cart.append(cart_item)

    return cart


# ==========================================
# 7. INCREASE QUANTITY
# ==========================================

def increase_quantity(cart, food_id):

    for item in cart:

        if item["id"] == food_id:

            item["quantity"] += 1

            return cart

    return cart


# ==========================================
# 8. DECREASE QUANTITY
# ==========================================

def decrease_quantity(cart, food_id):

    for item in cart:

        if item["id"] == food_id:

            if item["quantity"] > 1:

                item["quantity"] -= 1

            return cart

    return cart


# ==========================================
# 9. REMOVE FROM CART
# ==========================================

def remove_from_cart(cart, food_id):

    for item in cart:

        if item["id"] == food_id:

            cart.remove(item)

            return cart

    return cart


# ==========================================
# 10. ITEM AMOUNT
# ==========================================

def calculate_item_amount(price, quantity):

    return price * quantity


# ==========================================
# 11. SUBTOTAL
# ==========================================

def calculate_subtotal(cart):

    subtotal = 0

    for item in cart:

        amount = calculate_item_amount(
            item["price"],
            item["quantity"]
        )

        subtotal += amount

    return subtotal


# ==========================================
# 12. DISCOUNT
# ==========================================

def calculate_discount(subtotal):

    if subtotal >= 500:

        return subtotal * 10 / 100

    elif subtotal >= 300:

        return subtotal * 5 / 100

    else:

        return 0


# ==========================================
# 13. GST
# ==========================================

def calculate_gst(amount):

    return amount * 5 / 100


# ==========================================
# 14. FINAL BILL
# ==========================================

def calculate_bill(cart):

    subtotal = calculate_subtotal(cart)

    discount = calculate_discount(subtotal)

    after_discount = subtotal - discount

    gst = calculate_gst(after_discount)

    total = after_discount + gst


    return {

        "subtotal": subtotal,

        "discount": discount,

        "after_discount": after_discount,

        "gst": gst,

        "total": total

    }


# ==========================================
# 15. GENERATE ORDER ID
# ==========================================

def generate_order_id(order_number):

    return "CAN" + str(order_number)


# ==========================================
# 16. UPDATE ORDER STATUS
# ==========================================

def update_order_status(orders, order_id, new_status):

    for order in orders:

        if order["order_id"] == order_id:

            order["status"] = new_status

            return True

    return False


# ==========================================
# 17. TOTAL SALES
# ==========================================

def calculate_total_sales(orders):

    total_sales = 0

    for order in orders:

        total_sales += order["total"]

    return total_sales