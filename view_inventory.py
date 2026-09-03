from db import get_connection

def display_inventory():
    conn = get_connection()
    if not conn:
        print("Could not connect to Oracle Database.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT product_id, name, category, price, stock_quantity FROM products ORDER BY product_id")
    rows = cursor.fetchall()

    print("\n--- CURRENT ORACLE INVENTORY TABLE ---")
    print(f"{'ID':<5} | {'NAME':<20} | {'CATEGORY':<15} | {'PRICE ($)':<10} | {'STOCK':<5}")
    print("-" * 65)

    for row in rows:
        print(f"{row[0]:<5} | {row[1]:<20} | {row[2]:<15} | {row[3]:<10.2f} | {row[4]:<5}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    display_inventory()