import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Download CSV files
orders = pd.read_csv('../DataSet/olist_orders_dataset.csv')
items = pd.read_csv('../DataSet/olist_order_items_dataset.csv')
payments = pd.read_csv('../DataSet/olist_order_payments_dataset.csv')
products = pd.read_csv('../DataSet/olist_products_dataset.csv')
cat_name = pd.read_csv('../DataSet/product_category_name_translation.csv')

# Create SQL Base
conn = sqlite3.connect('../DataSet/Ex_An.db')

# And from csv files into tables
orders.to_sql('orders', conn, if_exists='replace', index = False)
items.to_sql('items', conn, if_exists='replace', index = False)
payments.to_sql('payments', conn, if_exists='replace', index = False)
products.to_sql('products', conn, if_exists='replace',index = False)
cat_name.to_sql('names', conn, if_exists='replace',index = False)

# SQL work and preparing and firs analyse in Sales (count of orders by category or product)
query = ("""
SELECT 
    o.order_id,
    i.freight_value,
    s.product_id, 
    p.payment_type, 
    i.product_id, 
    n.product_category_name_english, 
    i.price,
    p.payment_value
FROM orders o 
JOIN items i ON o.order_id = i.order_id
JOIN payments p ON o.order_id = p.order_id
Join products s ON i.product_id = s.product_id
JOIN names n ON s.product_category_name = n.product_category_name;
""")

df = pd.read_sql_query(query, conn)
#print(df.head())
#print(df.columns)
#Make EDA analysis
#print(df.describe())
# 1. Gross Revenue ( Sum of prices ) without Freight Revenue - that is logistic
#print('Gross Revenue = ', sum(df['price']))
# 2. Gross Freight Revenue:
#print('Gross Freight Revenue = ', sum(df['freight_value']))
# 3. Orders count (how much orders)
#print('Orders count: ', len(df['order_id'].unique()))
# 4. Items sold
#print('Items sold: ', len(df['product_id']))
# 5. Average Check price
#print('Average Check price: ', sum(df['price'])/len(df['order_id'].unique()))
# 6. Price Distribution (min, max, median and average price + visualization binning)
#medianprice = df['price'].median()
#print(medianprice)
#plt.figure(figsize = (10,7))
#plt.boxplot(df['price'])
#plt.title('Price analysis')
#plt.show()
# So median price is 74.9 but in data are many emissions,
# that should be grouped and look at the number of orders by group and the cost of prices

#Segments ( low , Medium , Height , Lux ) prices
#bins = [df['price'].min(), 100, 500, 2500, df['price'].max()]
#labels = ['low', 'medium', 'height', 'lux']
#df['price_seg'] = pd.cut(df['price'], bins= bins, labels = labels, include_lowest=True)
#s_counts = df['price_seg'].value_counts().sort_index()
#plt.figure(figsize=(10,7))
#s_counts.plot(kind='bar')
#plt.title('Count of products by price segmentation')
#plt.xlabel('Price segmentation')
#plt.ylabel('Count of products')
#plt.show()

# Most of products are in segment low-costed and second place takes medium-costed products
# Lets see top of this category (Top 10 low costed and Expensive products in market)