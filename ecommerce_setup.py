import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='use you password here',
    database='ecommerce_analysis'
)
cursor = conn.cursor()

# Load cleaned files
orders = pd.read_csv('orders_cleaned.csv')
order_items = pd.read_csv('order_items_cleaned.csv')
payments = pd.read_csv('payments_cleaned.csv')
products = pd.read_csv('products_cleaned.csv')
customers = pd.read_csv('customers_cleaned.csv')
sellers = pd.read_csv('sellers_cleaned.csv')

def clean_df(df):
    return df.where(pd.notnull(df), None)

orders = clean_df(orders)
order_items = clean_df(order_items)
payments = clean_df(payments)
products = clean_df(products)
customers = clean_df(customers)
sellers = clean_df(sellers)

# Import Customers first (referenced by orders)
print("Importing customers...")
for _, row in customers.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO customers
        (customer_id, customer_unique_id,
         customer_city, customer_state)
        VALUES (%s,%s,%s,%s)
    """, tuple(row))
conn.commit()
print(f"✅ Customers done: {len(customers)} rows")

# Import Sellers
print("Importing sellers...")
for _, row in sellers.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO sellers
        (seller_id, seller_city, seller_state)
        VALUES (%s,%s,%s)
    """, tuple(row))
conn.commit()
print(f"✅ Sellers done: {len(sellers)} rows")

# Import Products
print("Importing products...")
for _, row in products.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO products
        (product_id, product_category_name,
         product_weight_g, product_length_cm,
         product_height_cm, product_width_cm,
         product_category_name_english)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, tuple(row))
conn.commit()
print(f"✅ Products done: {len(products)} rows")

# Import Orders
print("Importing orders... (takes 2-3 mins)")
for _, row in orders.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO orders
        (order_id, customer_id, order_status,
         order_purchase_timestamp, order_approved_at,
         order_delivered_carrier_date,
         order_delivered_customer_date,
         order_estimated_delivery_date,
         order_year, order_month, order_month_name,
         order_day, order_quarter,
         delivery_days, estimated_days, delivery_status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, tuple(row))
conn.commit()
print(f"✅ Orders done: {len(orders)} rows")

# Import Order Items
print("Importing order items... (takes 2-3 mins)")
for _, row in order_items.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO order_items
        (order_id, order_item_id, product_id,
         seller_id, shipping_limit_date,
         price, freight_value, total_price)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, tuple(row))
conn.commit()
print(f"✅ Order items done: {len(order_items)} rows")

# Import Payments
print("Importing payments... (takes 2-3 mins)")
for _, row in payments.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO payments
        (order_id, payment_sequential, payment_type,
         payment_installments, payment_value)
        VALUES (%s,%s,%s,%s,%s)
    """, tuple(row))
conn.commit()
print(f"✅ Payments done: {len(payments)} rows")

cursor.close()
conn.close()
print("\n✅ All done! E-Commerce database ready.")