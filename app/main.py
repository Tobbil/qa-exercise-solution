from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "exercise-secret-key"

PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "price": 79.99, "stock": 10, "category": "Electronics"},
    {"id": 2, "name": "Running Shoes", "price": 49.99, "stock": 5, "category": "Footwear"},
    {"id": 3, "name": "Coffee Mug", "price": 12.99, "stock": 0, "category": "Kitchen"},
    {"id": 4, "name": "Yoga Mat", "price": 29.99, "stock": 8, "category": "Sports"},
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_cart():
    return session.get("cart", {})

def save_cart(cart):
    session["cart"] = cart

def _build_cart_payload():
    """Return a JSON-serialisable dict describing the current cart state."""
    cart = get_cart()
    items = []
    total = 0.0
    for pid, qty in cart.items():
        product = next((p for p in PRODUCTS if p["id"] == int(pid)), None)
        if product:
            subtotal = round(product["price"] * qty, 2)
            total += subtotal
            items.append({**product, "quantity": qty, "subtotal": subtotal})
    return {
        "cart": cart,
        "items": items,
        "total": round(total, 2),
        "item_count": sum(cart.values()),
    }


# ---------------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return render_template("404.html"), 404
    return render_template("product.html", product_id=product_id)

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/checkout")
def checkout():
    if not get_cart():
        return redirect(url_for("cart"))
    return render_template("checkout.html", error=None)

@app.route("/order-confirmed")
def order_confirmed():
    name = session.pop("confirmed_name", None)
    if not name:
        return redirect(url_for("home"))
    return render_template("confirmation.html", name=name)


# ---------------------------------------------------------------------------
# API – health
# ---------------------------------------------------------------------------

@app.route("/api/health")
def api_health():
    return jsonify({"status": "ok"}), 200


# ---------------------------------------------------------------------------
# API – products
# ---------------------------------------------------------------------------

@app.route("/api/products")
def api_products():
    return jsonify(PRODUCTS)

@app.route("/api/products/<int:product_id>")
def api_product(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


# ---------------------------------------------------------------------------
# API – cart
# ---------------------------------------------------------------------------

@app.route("/api/cart", methods=["GET"])
def api_cart():
    return jsonify(_build_cart_payload())

@app.route("/api/cart/<int:product_id>", methods=["POST"])
def api_cart_add(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    cart = get_cart()
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    save_cart(cart)
    return jsonify(_build_cart_payload()), 200

@app.route("/api/cart/<int:product_id>", methods=["DELETE"])
def api_cart_remove(product_id):
    cart = get_cart()
    if str(product_id) not in cart:
        return jsonify({"error": "Item not in cart"}), 404
    del cart[str(product_id)]
    save_cart(cart)
    return jsonify(_build_cart_payload()), 200


# ---------------------------------------------------------------------------
# API – checkout
# ---------------------------------------------------------------------------

@app.route("/api/checkout", methods=["POST"])
def api_checkout():
    if not get_cart():
        return jsonify({"error": "Cart is empty"}), 400
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    address = data.get("address", "").strip()
    if not name or not address:
        return jsonify({"error": "All fields are required."}), 422
    save_cart({})
    session["confirmed_name"] = name
    return jsonify({"success": True, "name": name}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5050)
