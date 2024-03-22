
from faker import Faker
import random
import mysql.connector

# Connect to MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="e_commerce"
)
cursor = mydb.cursor()

# Initialize Faker
fake = Faker()

# Generate records for the products table
for _ in range(random.randint(2000, 5000)):
    product_id = fake.uuid4()
    name = fake.word()
    description = fake.sentence()
    color = fake.color_name()
    size = random.choice(['Small', 'Medium', 'Large'])
    price = round(random.uniform(10.0, 100.0), 2)
    attributes = {
        'color': color,
        'size': size,
        'price': price
    }
    attributes_json = json.dumps(attributes)
    cursor.execute("INSERT INTO products (product_id, name, description, attributes) VALUES (%s, %s, %s, %s)", (product_id, name, description, attributes_json))
    mydb.commit()

# Generate records for the orders table
for _ in range(random.randint(1000, 2000)):
    order_id = fake.uuid4()
    customer_id = random.randint(1, 300)  # Assuming you have 300 customers
    order_date = fake.date_time_this_year()
    cursor.execute("INSERT INTO orders (order_id, customer_id, order_date) VALUES (%s, %s, %s)", (order_id, customer_id, order_date))
    mydb.commit()

# Generate records for the order_details table
for _ in range(random.randint(300, 500)):
    detail_id = fake.uuid4()
    order_id = random.randint(1, 2000)  # Assuming you have 2000 orders
    product_id = random.randint(1, 5000)  # Assuming you have 5000 products
    quantity = random.randint(1, 10)
    price = round(random.uniform(10.0, 100.0), 2)
    cursor.execute("INSERT INTO order_details (detail_id, order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s, %s)", (detail_id, order_id, product_id, quantity, price))
    mydb.commit()

# Generate records for the customers table
for _ in range(random.randint(300, 500)):
    customer_id = fake.uuid4()
    firstname = fake.first_name()
    middlename = fake.first_name()
    lastname = fake.last_name()
    address = fake.address()
    cursor.execute("INSERT INTO customers (customer_id, firstname, middlename, lastname, address) VALUES (%s, %s, %s, %s, %s)", (customer_id, firstname, middlename, lastname, address))
    mydb.commit()

# Close the connection
mydb.close()
