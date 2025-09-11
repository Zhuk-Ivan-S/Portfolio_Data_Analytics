import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap



geo = pd.read_csv('../DataSet/olist_geolocation_dataset.csv')
cust = pd.read_csv('../DataSet/olist_customers_dataset.csv')
items = pd.read_csv('../DataSet/olist_order_items_dataset.csv')
product = pd.read_csv('../DataSet/olist_products_dataset.csv')
names = pd.read_csv('../DataSet/product_category_name_translation.csv')
orders = pd.read_csv('../DataSet/olist_orders_dataset.csv')

conn = sqlite3.connect('../DataSet/dem_an.db')
orders.to_sql('orders', conn, index=False, if_exists='replace')
product.to_sql('product',conn,if_exists='replace',index = False)
geo.to_sql('geo',conn, index=False, if_exists='replace')
cust.to_sql('cust',conn,index = False, if_exists='replace')
items.to_sql('items',conn, index=False, if_exists='replace')
names.to_sql('names',conn, index= False, if_exists='replace')

query_dem1 = """Select customer_state, customer_city, customer_id, customer_unique_id from cust"""
df_cust = pd.read_sql_query(query_dem1, conn)
print(df_cust.head(10))

# calculate number of customers by states and city
count_cust_city = df_cust.groupby('customer_city')['customer_id'].count().sort_values()
print(count_cust_city)

# Visualization for top 20 Cities sorted by count of customers
count_cust_city.tail(20).plot(kind='bar')
plt.title('top 20 Cities sorted by count of customers')
plt.xlabel('City')
plt.ylabel('Count of customers')
plt.show()

# curitiba, brasilia, belo horizonte, rio de janeiro, sao paulo - when analyzing the number of orders
# according to the list, these cities are the concentration of the largest number of orders,
# such information allows sellers to understand the need to place warehouses (logistics nodes) in order
# to improve and speed up the possibilities of realization

# same thing for states
count_cust_state = df_cust.groupby('customer_state')['customer_id'].count().sort_values()
print(count_cust_state)
count_cust_state.plot(kind='bar', color = 'red')
plt.title('States sorted by count of customers')
plt.xlabel('State')
plt.ylabel('Count of customers')
plt.show()

# use folium library for geolocation and concentration of orders visualization
query_map = """
SELECT c.customer_id, g.lat, g.lng From cust c
Join (SELECT geolocation_city, AVG(geolocation_lat) as lat, AVG(geolocation_lng) as lng FROM geo
Group BY geolocation_city) g ON c.customer_city = g.geolocation_city; """
df_map = pd.read_sql_query(query_map, conn)
print(df_map.head(10))
br_center = folium.Map(location=[-15.78, -48.93], zoom_start = 4)
HeatMap(df_map[['lat','lng']].values, radius=10).add_to(br_center)
# save that map in html file than we can see that in browser
br_center.save('../DataSet/customer_heatmap.html')

braz_map = folium.Map(location = [-15.78, 47.93], zoom_start=4)
for _, row in df_map.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lng']],
        radius = 2,
        color = 'red',
        fill = True,
        fill_opacity = 0.5).add_to(braz_map)
braz_map.save('../DataSet/braz_map.html')

# analysis of customer behavior (repeatability)
query_cust = """
SELECT c.customer_unique_id, COUNT(o.order_id) as orders_count
FROM orders AS o
JOIN cust c ON o.customer_id = c.customer_id
Group by c.customer_unique_id;"""
df_o_c = pd.read_sql_query(query_cust,conn)

df_o_c['repeat_customer'] = df_o_c['orders_count'] > 1
repeat_rate = df_o_c['repeat_customer'].mean() * 100
print(f'Percentage repeat customers: {repeat_rate}')
df_o_c['orders_count'].value_counts().sort_index().plot(kind = 'hist')
plt.title('Count of orders per customer')
plt.xlabel('Count of orders')
plt.ylabel('Count of customers')
plt.show()

df_items_per_order = items.groupby('order_id')['product_id'].count().reset_index()
print(f'Average count of products in orders: {df_items_per_order["product_id"].mean()}')

query_orders_cust = """
SELECT o.order_id, c.customer_unique_id
FROM orders o
JOIN cust c ON o.customer_id = c.customer_id;
"""
orders_cust = pd.read_sql_query(query_orders_cust, conn)
# repeat customers
repeat_customers = df_o_c[df_o_c['orders_count'] > 1]['customer_unique_id']
# orders
repeat_orders = orders_cust[orders_cust['customer_unique_id'].isin(repeat_customers)][['order_id','customer_unique_id']].reset_index(drop=True)
# products of orders
repeat_items = items[items['order_id'].isin(repeat_orders['order_id'])]
# top products
top_repeat_products = repeat_items['product_id'].value_counts().head(10)
print(f'Repeat orders with id of product : {top_repeat_products}')


