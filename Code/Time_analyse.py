import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

from numpy.ma.core import count

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
time_df['order_estimated_delivery_date'] = pd.to_datetime(time_df['order_estimated_delivery_date'])

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
# Combo : make heatmap and see orders sorted by day of week and hours
# Create pivot table
pivot = time_df.pivot_table(index = 'day_o_w',columns = 'time_of_day', values= 'order_id',aggfunc='count',fill_value=0)
order_days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
pivot = pivot.reindex(order_days)

plt.figure(figsize = (8,11))
plt.imshow(pivot)
plt.xticks(range(len(pivot.columns)),pivot.columns,rotation = 25)
plt.yticks(range(len(pivot.index)),pivot.index)
plt.colorbar(label='Number of Orders')
plt.title('Orders by day of week and hours')
plt.show()
# Now I make time analyse for delivery time and make some insights

# proportion of delays. I need clean data without info about canceled orders order not completed
df_c_time = time_df.dropna(subset=['order_delivered_customer_date','order_purchase_timestamp','order_estimated_delivery_date']).copy()
print(df_c_time.head(10))

# Change metrics in datetime (days):
# How much day need from purchase date to delivery date - that give some info about logistic
df_c_time.loc[:, 'delivery_days'] = (df_c_time['order_delivered_customer_date']-df_c_time['order_purchase_timestamp']).dt.days
average_delivery = df_c_time['delivery_days'].mean()
print(f'Average delivery time - {average_delivery} days')
# what is the difference between the expectation and the actual delivery,
# which will allow you to evaluate the speed and quality of logistics services
# ('+' value will be positive, '-' will be negative for logistics evaluation)

df_c_time.loc[:,'estimate_time'] = (df_c_time['order_estimated_delivery_date'] - df_c_time['order_purchase_timestamp']).dt.days
df_c_time.loc[:,'faster_days'] = (df_c_time['order_estimated_delivery_date']-df_c_time['order_delivered_customer_date']).dt.days
df_c_time.loc[:,'delay_days'] = (df_c_time['order_delivered_customer_date'] - df_c_time['order_estimated_delivery_date']).dt.days
plt.figure(figsize=(10,7))
plt.boxplot(df_c_time['delivery_days'].dropna(),vert=False)
plt.title('Distribution of Delivery Time')
plt.xlabel('Days')
plt.show()
# time is different
# first try of
avg_faster_del = (df_c_time['estimate_time']-df_c_time['faster_days']).mean()
print(f'Faster delivery average - {avg_faster_del} days')
# Percentage of delivery efficient
p_f_d = ((df_c_time['estimate_time']-df_c_time['delivery_days'])/df_c_time['estimate_time']) * 100
print(f'Percentage of delivery efficient - {p_f_d.mean()} %')
counts = []
for late in df_c_time['delay_days']:
    if late > 0 :
        counts.append(late)
late_count = len(counts)
print(f'Late delivery count - {late_count} orders/{df_c_time['delay_days'].value_counts().sum()} orders')
# proportion of delays
late_deliveries = (df_c_time['delay_days'] > 0).mean() * 100
print(f'proportion of delays - {late_deliveries} %')
# visualization histogram for showing how often orders arrive ahead of schedule
plt.figure(figsize=(10,8))
df_c_time['faster_days'].hist(bins = 10, edgecolor = 'black')
plt.title('Distribution of faster delivery')
plt.xlabel('Days faster as plan')
plt.ylabel('Count of orders')
plt.show()

# Insights :
# 1.Order activity is recorded according to the season (this may be related to holidays,
# promotions, and advantageous offers)
# 2. Most orders are placed in the evening (5:00 PM–11:00 PM), which indicates customer activity after work.
# This can be a key time for targeted promotions and marketing campaigns.
# 3. The average faster delivery time was about 12 days, which is in most
# cases less than the expected time. This indicates good logistics efficiency.
# 4.On average, orders arrive 12 days faster than predicted, which can increase
# customer satisfaction and increase their loyalty. Percentage of delivery efficient - 47.23 %
# 5. The proportion of delays is 6.73 %, meaning the company consistently adheres to
# the stated delivery times. This is a competitive advantage.
# 6. Despite the overall positive picture, it is worth analyzing exceptional cases with long deliveries
# to understand their reasons (geography, product category, seasonal peaks).