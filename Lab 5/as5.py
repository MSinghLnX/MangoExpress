import psycopg2
import time

# Connect to the MangoExpress database
conn = psycopg2.connect(database="MangoExpress", user="ms", password="Ikonkar9831")
cur = conn.cursor()


def getSales():
    # Get mangos sold
    total_revenue = 0
    cur.execute("SELECT product_id, quantity FROM unit_order")
    products_sold = cur.fetchall()

    # Calculate total revenue from sales of each product
    product_revenue = {}
    for product_id, quantity in products_sold:
        cur.execute("SELECT price FROM products WHERE id = %s", (product_id,))
        price = cur.fetchone()[0]

        total_revenue += price * quantity
        product_revenue[product_id] = total_revenue

    # Sort products by total revenue, then units sold, then alphabetically by product name, descending
    product_revenue_sorted = sorted(product_revenue.items(), key=lambda x: (-x[1], x[0], x[1]), reverse=False)

    # Generate a sales report
    sales_report = []
    for product_id, total_revenue in product_revenue_sorted:
        cur.execute("SELECT name FROM products WHERE id = %s", (product_id,))
        product_name = cur.fetchone()[0]

        sales_report.append(f"{product_name} sold {products_sold[product_id][1]} total rev ${total_revenue}")
    return sales_report

while True:
    sales_report = getSales()
    print("Sales Report:")
    for line in sales_report:
        print(line)

    # Wait for 1 second
    time.sleep(1)
    print("\n")
# Close the cursor and database connection
cur.close()
conn.close()
