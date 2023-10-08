import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
from decouple import config


def connect_to_db(host='localhost', user='root', db_name='sales_database'):
    """
    Connect to the MySQL database.
    If the specified database doesn't exist, create it.
    """
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password = config('DB_PASSWORD'),
            auth_plugin='mysql_native_password'
        )

        # Create the database if it doesn't exist
        create_database(conn, db_name)

        # Set the database to the created/found one
        conn.database = db_name

        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)  # Exit the program with an error code


def create_database(conn, db_name='sales_database'):
    """
    Create the database if it doesn't exist.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)


def populate_database_from_csv(conn, host='localhost',
                               user='root', db_name='sales_database'):
    """
    Populate the MySQL database with data from CSV files.
    """
    password = config('DB_PASSWORD')
    # Define the connection string and create the engine
    conn_string = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
    engine = create_engine(conn_string)

    # Load datasets from CSV into DataFrame
    customers = pd.read_csv('data/customers.csv')
    orders = pd.read_csv('data/orders.csv')
    order_details = pd.read_csv('data/order_details.csv')
    products = pd.read_csv('data/products.csv')

    # Store data from DataFrame into MySQL database using the engine
    customers.to_sql('customers', engine, if_exists='replace', index=False)
    orders.to_sql('orders', engine, if_exists='replace', index=False)
    order_details.to_sql('order_details', engine,
                         if_exists='replace', index=False)
    products.to_sql('products', engine, if_exists='replace', index=False)


def execute_query(conn):
    """
    Execute the complex SQL query and return the results.
    """
    cursor = conn.cursor()
    query = """
    SELECT 
        c.customer_name, 
        o.order_date, 
        p.product_name, 
        SUM(od.quantity) AS total_ordered_quantity, 
        SUM(od.quantity * p.price) AS total_order_value
    FROM 
        customers c
    JOIN 
        orders o ON c.customer_id = o.customer_id
    JOIN 
        order_details od ON o.order_id = od.order_id
    JOIN 
        products p ON od.product_id = p.product_id
    WHERE 
        o.order_date BETWEEN '2022-01-01' AND '2022-12-31'
    GROUP BY 
        c.customer_name, 
        o.order_date, 
        p.product_name
    HAVING 
        SUM(od.quantity) > 10
    ORDER BY 
        total_order_value DESC, 
        c.customer_name ASC;
    """
    cursor.execute(query)
    return cursor.fetchall()


def display_results(results):
    """
    Display the query results in a formatted manner.
    """
    print("| Customer Name  | Order Date | Product Name "
          "| Quantity Ordered | Total Order Value |")
    print("|----------------|------------|--------------"
          "|------------------|-------------------|")

    for row in results:
        print("| {0:14} | {1:10} | {2:12} | {3:16} | {4:17} "
              "|".format(row[0], row[1], row[2], row[3], row[4]))


if __name__ == "__main__":
    conn = connect_to_db()
    create_database(conn)
    populate_database_from_csv(conn)
    results = execute_query(conn)
    display_results(results)
    conn.close()
