import random
import time, datetime
import psycopg2
import string

# Time interval
X = 5
print("Uncomment the 3 cur.execute statements if the mangoes are not in the database (See lab4.py) (Too many errors Milan!)")

# Connect to MangoExpress DB
conn = psycopg2.connect(database="MangoExpress", user="ms", password="Ikonkar9831")
cur = conn.cursor()

# Manages random orders
def create_random_order():
    print("Creating Order")
    
    # Create Random customer for every order
    letters = string.ascii_lowercase
    customer_id = random.randint(1,10000)

    # Make sure duplicate customer ID's don't exist
    prev_id = set()
    if customer_id in prev_id:
        create_random_order()
    else:
        prev_id = prev_id.add(customer_id)
        
    name = ''.join(random.choice(letters) for i in range(10))
    email = ''.join(random.choice(letters) for i in range(10)) + "@hofstra.edu"
    address = ''.join(random.choice(letters) for i in range(10)) + "Street"
    cur.execute("INSERT INTO customers (id, name, email, address) VALUES (%s, %s, %s, %s)", (customer_id, name, email, address))
    conn.commit()
    # Ensure previous order id is not copied
    prev_order = set()
    order_id = random.randint(1, 10000)
    if order_id in prev_order:
        print("Mango Passport is invalid! Fabricating new one... (non-unique order_id)")
        create_random_order()
    else:
        print("Mango Passport passed through border patrol (unique order_id)")
        prev_order = prev_order.add(order_id)

    # Generate a random list from these mangoes, and don't try to create tables if already in database
    print("Creating mangoes outta thin air...")
   # cur.execute("INSERT INTO products (id, name, description, price) VALUES ('7','Honey','Sweet','1')")
   # cur.execute("INSERT INTO products (id, name, description, price) VALUES ('10','Keitt','Spicy','1')")
   # cur.execute("INSERT INTO products (id, name, description, price) VALUES ('11','Kent','Warm','1')")
   # cur.execute("INSERT INTO products (id, name, description, price) VALUES ('8','Francis','Nutty','1')")
   # cur.execute("INSERT INTO products (id, name, description, price) VALUES ('9','Haden','Fibry','1')")
   # cur.execute("INSERT INTO products (id, name, description, price) VALUES ('12','Atkins','Worst','1')")
    product_types = random.sample(["7", "8", "9", "10", "11", "12"], random.randint(1, 6))

    # Generate number of products for each product type (Price for each product is $1 (It's a mango...))
    product_amounts = {}
    for product_type in product_types:
        product_amounts[product_type] = random.randint(1, 1000)
        
    current_date = datetime.date.today()
    current_time = datetime.date.today()
    price = random.randint(1, 10000)

    cur.execute("Select number FROM stock")
    productStock = [row[0] for row in cur.fetchall()]
    print("")
    print("Mango Stock: ")
    print(productStock)
    print("")
    # Create a new order record in the database
    cur.execute("INSERT INTO orders (id, customer_id, order_date, shipped_date, total_price, status) VALUES (%s, %s, %s, %s, %s, 'Pending')", (order_id , customer_id, current_date, current_time, price))
    
    # Mango Stock Check
    for i in productStock:
        if i <= 0:
            print("Some mangoes are out of stock, cannot commit to the order")
            return 0


    # Create a new order line record for each product type
    for product_type, product_amount in product_amounts.items():
        cur.execute("INSERT INTO unit_order (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)", (order_id, product_type, product_amount,(price/6) ))
        
        # Mango Erasure
        print("Clearing mangos from our stock server")
        cur.execute("UPDATE stock SET number = number - %s WHERE product_id = %s", (product_amount, product_type))

    conn.commit()
    print("Order Created")

# Start the loop to create random orders
while True:

    create_random_order()

    time.sleep(X)

