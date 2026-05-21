import pandas as pd

# ── Load all files ──
customers = pd.read_csv('olist_customers_dataset.csv')
order_items = pd.read_csv('olist_order_items_dataset.csv')
payments = pd.read_csv('olist_order_payments_dataset.csv')
orders = pd.read_csv('olist_orders_dataset.csv')
products = pd.read_csv('olist_products_dataset.csv')
sellers = pd.read_csv('olist_sellers_dataset.csv')
category_translation = pd.read_csv('product_category_name_translation.csv')

print("All files loaded!")
print(f"Customers: {len(customers)} rows")
print(f"Order Items: {len(order_items)} rows")
print(f"Payments: {len(payments)} rows")
print(f"Orders: {len(orders)} rows")
print(f"Products: {len(products)} rows")
print(f"Sellers: {len(sellers)} rows")

# ══════════════════════════════════
# CLEAN ORDERS
# ══════════════════════════════════

# Convert date columns to datetime
date_columns = [
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
]
for col in date_columns:
    orders[col] = pd.to_datetime(orders[col])

# Extract useful date parts from purchase date
orders['order_year'] = orders['order_purchase_timestamp'].dt.year
orders['order_month'] = orders['order_purchase_timestamp'].dt.month
orders['order_month_name'] = orders[
    'order_purchase_timestamp'].dt.strftime('%B')
orders['order_day'] = orders[
    'order_purchase_timestamp'].dt.day_name()
orders['order_quarter'] = orders[
    'order_purchase_timestamp'].dt.quarter

# Calculate delivery time in days
orders['delivery_days'] = (
    orders['order_delivered_customer_date'] -
    orders['order_purchase_timestamp']
).dt.days

# Calculate if delivered early or late
orders['estimated_days'] = (
    orders['order_estimated_delivery_date'] -
    orders['order_purchase_timestamp']
).dt.days

orders['delivery_status'] = orders.apply(
    lambda x: 'Early' if x['delivery_days'] < x['estimated_days']
    else 'Late', axis=1
)

# Keep only delivered orders for analysis
orders_delivered = orders[orders['order_status'] == 'delivered'].copy()

print(f"\nOrders after filtering delivered only: {len(orders_delivered)}")
print(f"Null delivery dates: {orders_delivered['delivery_days'].isnull().sum()}")

# ══════════════════════════════════
# CLEAN ORDER ITEMS
# ══════════════════════════════════

# Calculate total price per item
order_items['total_price'] = (
    order_items['price'] + order_items['freight_value']
)

# Convert shipping date
order_items['shipping_limit_date'] = pd.to_datetime(
    order_items['shipping_limit_date']
)

print(f"\nOrder Items nulls:\n{order_items.isnull().sum()}")

# ══════════════════════════════════
# CLEAN PRODUCTS
# ══════════════════════════════════

# Merge with English category names
products = products.merge(
    category_translation,
    on='product_category_name',
    how='left'
)

# Fill missing English names
products['product_category_name_english'].fillna(
    products['product_category_name'], inplace=True
)

# Fill other nulls
products['product_category_name'].fillna('unknown', inplace=True)
products['product_category_name_english'].fillna('unknown', inplace=True)
products['product_weight_g'].fillna(0, inplace=True)

# Drop unnecessary columns
products = products.drop(columns=[
    'product_name_lenght',
    'product_description_lenght',
    'product_photos_qty'
])

print(f"\nProducts after cleaning: {len(products)} rows")

# ══════════════════════════════════
# CLEAN CUSTOMERS
# ══════════════════════════════════

# Capitalize city names
customers['customer_city'] = customers[
    'customer_city'].str.title()

# Keep only needed columns
customers = customers[[
    'customer_id',
    'customer_unique_id',
    'customer_city',
    'customer_state'
]]

# ══════════════════════════════════
# CLEAN SELLERS
# ══════════════════════════════════

# Capitalize city names
sellers['seller_city'] = sellers['seller_city'].str.title()

# Keep only needed columns
sellers = sellers[[
    'seller_id',
    'seller_city',
    'seller_state'
]]

# ══════════════════════════════════
# CLEAN PAYMENTS
# ══════════════════════════════════

# Remove zero value payments
payments = payments[payments['payment_value'] > 0]

print(f"\nPayments after removing zeros: {len(payments)} rows")

# ══════════════════════════════════
# SAVE ALL CLEANED FILES
# ══════════════════════════════════

orders.to_csv('orders_cleaned.csv', index=False)
orders_delivered.to_csv('orders_delivered_cleaned.csv', index=False)
order_items.to_csv('order_items_cleaned.csv', index=False)
payments.to_csv('payments_cleaned.csv', index=False)
products.to_csv('products_cleaned.csv', index=False)
customers.to_csv('customers_cleaned.csv', index=False)
sellers.to_csv('sellers_cleaned.csv', index=False)

print("\n✅ All files cleaned and saved!")
print(f"orders_cleaned: {len(orders)} rows")
print(f"orders_delivered_cleaned: {len(orders_delivered)} rows")
print(f"order_items_cleaned: {len(order_items)} rows")
print(f"payments_cleaned: {len(payments)} rows")
print(f"products_cleaned: {len(products)} rows")
print(f"customers_cleaned: {len(customers)} rows")
print(f"sellers_cleaned: {len(sellers)} rows")
