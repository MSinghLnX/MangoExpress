import psycopg2
import random
import time

# Connect to the MangoExpress database
conn = psycopg2.connect(database="MangoExpress", user="ms", password="Ikonkar9831")
cur = conn.cursor()

interval = 10


while True:
    print("MangoExpress needs Mangos! Executing order...")

    # Get product number and choose products to update
    cur.execute("SELECT product_id from stock")
    products = [row[0] for row in cur.fetchall()]
    toUpdate = random.randint(1, len(products))
    
    # Commit Updates
    for i in range(toUpdate):
        # Choose a random product and update its stock
        product_id = random.choice(products)
        stock_update = random.randint(1, 1000)
        cur.execute( "UPDATE stock SET number = number + %s WHERE product_id = %s", (stock_update, product_id))
        conn.commit()
    print("Mangos are here! Lets get them on the shelves")    
    # Wait x seconds
    time.sleep(interval)


# Close the cursor and database connection
cur.close()
conn.close()
