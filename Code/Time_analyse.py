import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

# I want to work with time dataset in order to understand the patterns of peak orders and the
# differentiation of customer activity, the data of the study allow more productive use of marketing
# tools to improve one's position in the market and efficient use of resources

# First of all preparing date for analysis (take years/months/days/hours of orders) change that into datetime
# Lets use SQL for collecting important datasets in this part of analysis
# I need order id , order purchase, time deliver, date payment value.
orders = pd.read_csv('../DataSet/olist_orders_dataset.csv')
payments = pd.read_csv('../DataSet/olist_order_payments_dataset.csv')

conn = sqlite3.connect('../DataSet/Time.db')
orders.to_sql('orders',conn, if_exists='replace', index=False)
payments.to_sql('payments',conn, if_exists='replace', index=False)

query= """
        Select
            o.order_id,
            o.order_purchase_timestamp,
            o.order_approved_at,
            o.order_delivered_customer_date,
            o.order_estimated_delivery_date,
            p.payment_value
        From orders AS o
        Join payments p ON o.order_id = p.order_id;
            """
time_df = pd.read_sql_query(query,conn)
# and check dataset
print(time_df.head(10))

#make datetime sets
time_df['order_purchase_timestamp'] = pd.to_datetime(time_df['order_purchase_timestamp'])
time_df['order_approved_at'] = pd.to_datetime(time_df['order_approved_at'])
time_df['order_delivered_customer_date'] = pd.to_datetime(time_df['order_delivered_customer_date'])
time_df['order_estimated_delivery_date'] = pd.to_datetime(time_df['order_delivered_customer_date'])

# Separate time into (years, months, days, hours) order purchase and analyse
time_df['year'] = time_df['order_purchase_timestamp'].dt.year
time_df['month'] = time_df['order_purchase_timestamp'].dt.month
time_df['day_o_w'] = time_df['order_purchase_timestamp'].dt.day_name()
time_df['hour'] = time_df['order_purchase_timestamp'].dt.hour

# Let's see orders sorted by date(years and months) for understanding peaks of orders
order_month_year = time_df.groupby(['year','month'])['order_id'].count()
order_month_year.plot(kind='line', figsize=(15,7),title='Orders by month and year')
plt.show()
order_month = time_df.groupby('month')['order_id'].count()
order_month.plot(kind='line', figsize=(15,7),title='Orders by month')
plt.show()

# analysis separately by year and month gives a general picture of peak orders, which
# increase in the summer period if taken in general by month and directly in the 11th
# month (November), possibly connected with "Black Friday". A strong decline in the autumn
# period may indicate a lack of interest from buyers or a lack of profitable offers from sellers.

# Orders sorted by days of week
order_da = time_df.groupby('day_o_w')['order_id'].count().sort_values()
order_da.plot(kind='bar', figsize=(10,7),title='Orders by days')
plt.show()
# Most orders are placed at the beginning of the week from Monday to Wednesday
# (this may be due to the fact that customers want to receive the product on the weekend,
# which will allow to be present at the delivery or for other reasons) a short note - a marketing
# strategy on the weekend stimulates the incentive to buy and gives results

# Orders sorted by hours
order_hour = time_df.groupby('hour')['order_id'].count().sort_values()
order_hour.plot(kind='bar', figsize=(10,7),title='Orders by hours')
plt.show()
# Buyer activity starts at 11 a.m. and peaks during this time until at least 11 p.m.
# But much better make some bins such like (morning, day, evening, night)
day_bins = [0,6,12,17,24]
labels_d = ['Night (0-6)','Morning (6-12)','Afternoon (12-18)','Evening (18-24)']
time_df['time_of_day']=pd.cut(time_df['hour'], bins=day_bins, labels=labels_d, include_lowest=True,right=False)
time_df['time_of_day'].value_counts().sort_values().plot(kind='bar',figsize = (10,7), title='Orders by time of day')
plt.show()

# Naturally, most orders are made in the evening from 5 to 11 p.m. (free time after work)