import pandas as pd
from faker import Faker
import pymysql  # Or your MySQL connector

# Database connection details (replace with your actual credentials)
host = "localhost"
user = "root"
password = ""
database = "e_commerce"

# Generate Faker instance
fake = Faker()

# Define record ranges
products_count = fake.pyint(min_value=2000, max_value=5000)
orders_count = fake.pyint(min_value=1000, max_value=2000)
customers_count = fake.pyint(min_value=300, max_value=500)

# Generate dummy data for Products table
product_data = {
    "name": [list(fake.product_name() for _ in range(products_count))],
    "description": [fake.text(max_nb_chars=200) for _ in range(products_count)],
    "attributes": [fake.json() for _ in range(products_count)],
}


products_df = pd.DataFrame(product_data)

# Generate dummy data for Orders table
order_data = {
    "customer_id": [fake.random_int(min=1, max=customers_count) for _ in range(orders_count)],
    "order_date": [fake.date() for _ in range(orders_count)],
}

orders_df = pd.DataFrame(order_data)

# Generate dummy data for Order Details table (assuming foreign keys are set)
order_details_data = []
for _ in range(orders_count):
    # Generate random number of products per order (between 1 and 5)
    num_products = fake.pyint(min_value=1, max_value=5)
    for _ in range(num_products):
        order_details_data.append({
            "order_id": fake.random_int(min=1, max=orders_count),
            "product_id": fake.random_int(min=1, max=products_count),
            "quantity": fake.pyint(min_value=1, max_value=10),
            "price": fake.pydecimal(positive=True, min_value=10, max_value=100),
        })

order_details_df = pd.DataFrame(order_details_data)

# Generate dummy data for Customers table
customer_data = {
    "firstname": [fake.first_name() for _ in range(customers_count)],
    "middlename": [fake.optional().text(max_nb_chars=50) for _ in range(customers_count)],  # Optional middle name
    "lastname": [fake.last_name() for _ in range(customers_count)],
    "address": [fake.address() for _ in range(customers_count)],
}

customers_df = pd.DataFrame(customer_data)

# Connect to database
connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cursor = connection.cursor()


def execute_insert_query(table_name, data_frame):
    """Executes INSERT statements for a given table and DataFrame"""
    columns = ", ".join(data_frame.columns)
    placeholders = ", ".join("%s" for _ in range(len(data_frame.columns)))
    sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"

    for index, row in data_frame.iterrows():
        cursor.execute(sql, tuple(row.values))


# Insert data into tables
execute_insert_query("products", products_df)
execute_insert_query("orders", orders_df)
execute_insert_query("order_details", order_details_df)
execute_insert_query("customers", customers_df)

connection.commit()
cursor.close()
connection.close()

print("Dummy data generation and insertion completed!")
