from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_connection

app = Flask(__name__)
app.secret_key = "ecommerce_secret_key"

@app.route("/")
def index():
    conn = get_connection()
    if not conn:
        return "Database Connection Error", 500
    
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, name, category, price, stock_quantity FROM products ORDER BY product_id DESC")
    products = cursor.fetchall()
    
    cursor.execute("""
        SELECT o.order_id, o.customer_name, p.name, o.quantity, o.order_date 
        FROM orders o 
        JOIN products p ON o.product_id = p.product_id 
        ORDER BY o.order_id DESC
    """)
    orders = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template("index.html", products=products, orders=orders)

@app.route("/add_product", methods=["POST"])
def add_product():
    name = request.form.get("name")
    category = request.form.get("category")
    price = request.form.get("price")
    stock = request.form.get("stock")

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, category, price, stock_quantity) VALUES (:1, :2, :3, :4)",
            (name, category, float(price), int(stock))
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    return redirect(url_for("index"))

@app.route("/add_order", methods=["POST"])
def add_order():
    customer_name = request.form.get("customer_name")
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity"))

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        # Verify stock before placing order
        cursor.execute("SELECT stock_quantity FROM products WHERE product_id = :1", (product_id,))
        row = cursor.fetchone()
        
        if row and row[0] >= quantity:
            cursor.execute(
                "INSERT INTO orders (customer_name, product_id, quantity) VALUES (:1, :2, :3)",
                (customer_name, product_id, quantity)
            )
            cursor.execute(
                "UPDATE products SET stock_quantity = stock_quantity - :1 WHERE product_id = :2",
                (quantity, product_id)
            )
            conn.commit()
        
        cursor.close()
        conn.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)