import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

sellers = pd.read_csv('../DataSet/olist_sellers_dataset.csv')
product = pd.read_csv('../DataSet/olist_products_dataset.csv')
items = pd.read_csv('../DataSet/olist_order_items_dataset.csv')
names = pd.read_csv('../DataSet/product_category_name_translation.csv')
conn = sqlite3.connect('../DataSet/salers.db')
sellers.to_sql('sellers',conn, if_exists='replace',index=False)
items.to_sql('items',conn, if_exists='replace',index = False)
product.to_sql('product',conn,if_exists='replace',index = False)
names.to_sql('names',conn, if_exists='replace',index = False)

query_sellers = """SELECT s.seller_id, s.seller_city, s.seller_state, i.price, i.order_id, p.product_id, n.product_category_name_english FROM sellers AS s
Join items AS i ON i.seller_id = s.seller_id
JOIN product AS p ON p.product_id = i.product_id
JOIN names AS n ON n.product_category_name = p.product_category_name;"""

df_sellers = pd.read_sql_query(query_sellers,conn)
print(df_sellers.head(10))

# top 10 sellers
top_10_sellers = df_sellers['seller_id'].value_counts()
print(top_10_sellers.head(10))
# and show info with barchart for top sellers
top_10_sellers.head(10).plot(kind= 'bar')
plt.title('Top sellers id sorted by count of sales (orders)')
plt.xlabel('seller ID')
plt.ylabel('Count of orders')
plt.show()
# and show top sellers sorted by Revenue
total_sales = df_sellers.groupby('seller_id')['price'].sum().sort_values()
top_10_sellers = total_sales.tail(10)
print(top_10_sellers)
top_10_sellers.plot(kind = 'bar', color = 'gold')
plt.title('Top sellers id sorted by Revenue (price sum)')
plt.xlabel('Sellers ID')
plt.ylabel('Revenue')
plt.show()
# Concentration of top sellers in Total revenue in market
other = total_sales.sum() - top_10_sellers.tail(10).sum()
seller_share = top_10_sellers._append(pd.Series({'Others' : other}))

plt.figure(figsize=(8,6))
plt.pie(seller_share, labels = seller_share.index, autopct='%1.1f%%')
plt.title('Sales part of the top 10 sellers on Market')
plt.show()
# Geo position of sellers , where are the most of sellers(city/ state)
geopos = df_sellers.groupby('seller_city')['seller_id'].nunique().sort_values()
print(geopos.tail(10))
# Show by barchart
geopos.tail(10).plot(kind = 'bar',color = 'green')
plt.title('Top 10 cities sorted by count of sellers')
plt.xlabel('City')
plt.ylabel('Count of sellers')
plt.show()
# Same thing for state of sellers
geoposstate = df_sellers.groupby('seller_state')['seller_id'].nunique().sort_values(ascending=False)
print(geoposstate.head(10))
# Show that with bar chart
geoposstate.head(10).plot(kind='bar', color = 'brown')
plt.title('Top 10 states sorted by count of sellers')
plt.xlabel('State')
plt.ylabel('Count of sellers')
plt.show()

# Top products distributed among the top 10 sellers (find out what the top sellers sell)
top_10_sellers = items.groupby('seller_id')['price'].sum().sort_values(ascending=False).head(10)
top_sellers_id = top_10_sellers.index
items_products = items.merge(product, on = 'product_id', how = 'left')
items_products = items_products.merge(names, on = 'product_category_name', how = 'left')
top_seller_items = items_products[items_products['seller_id'].isin(top_sellers_id)]
top_product = (top_seller_items.groupby('product_category_name_english')['price'].sum().sort_values(ascending=False).head(10))
print(top_product)
top_product.plot(kind='bar',color = 'red')
plt.title('Top 10 categories of products  in Top 10 sellers')
plt.xlabel('Product category')
plt.ylabel('Count of sales')
plt.show()

# Some insights
# 1 Given the distribution and frequent top 10 sellers from the total revenue, it can be said that the market and income
# are distributed approximately equally (which indicates the absence of monopolists)
# The pie chart showed that the top 10 sellers cover only 12.3% of the total sales market
# 2 The best-selling categories among the top sellers are (watches_gifts,bed_bath_tableoffice_furniture, furniture_decor,
# computers, cool_stuff, telephony, housewares, health_beauty,home_comfort)
# Which makes it possible to understand what the top sellers are betting on
# 3 Concentration and sales, which are displayed according to demographic indicators (geo-positioning),
# make it possible to understand the concentration and distribution of sales among cities and states -
# this makes it possible to study possible competition and a free niche for creating trade


#Having made certain small conclusions, it is possible to summarize as a result (which territories should
# be explored by newcomers in the online sales sector, which products are in demand, taking into account the
# experience of top sellers, taking into account the fact that the market adheres to effective competition due to
# the absence of monopolists)

# Note: you can analyze the reviews according to the sellers, determine the rating of the tops,
# whether the positive reviews on the tops prevail or vice versa. This will give a good picture of the
# interdependence of gross income and reputation

