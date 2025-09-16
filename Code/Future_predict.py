import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

orders = pd.read_csv('../DataSet/olist_orders_dataset.csv')
items = pd.read_csv('../DataSet/olist_order_items_dataset.csv')
names = pd.read_csv('../DataSet/product_category_name_translation.csv')
conn = sqlite3.connect('../DataSet/predict.db')
items.to_sql('items',conn, if_exists='replace',index = False)
orders.to_sql('orders', conn, index=False, if_exists='replace')
names.to_sql('names',conn, if_exists='replace',index = False)

query_p = """
SELECT o.order_id, o.order_purchase_timestamp,i.price, i.freight_value
FROM orders AS o
Join items AS i ON o.order_id = i.order_id;"""

df_predict = pd.read_sql_query(query_p, conn)
df_predict['order_purchase_timestamp'] = pd.to_datetime(df_predict['order_purchase_timestamp'])
df_predict['revenue'] = df_predict['price'] + df_predict['freight_value']
df_predict['month'] = df_predict['order_purchase_timestamp'].dt.to_period('M')

monthly_revenue = df_predict.groupby('month')['revenue'].sum().reset_index()
monthly_revenue['month'] = monthly_revenue['month'].dt.to_timestamp()
monthly_revenue['month_num'] = np.arange(len(monthly_revenue))

X = monthly_revenue[['month_num']]
y = monthly_revenue['revenue']
# Linear Regression predict
model = LinearRegression()
model.fit(X, y)
y_predict = model.predict(X)

# Metrix quality

r2 = r2_score(y, y_predict)
mae = mean_absolute_error(y, y_predict)
rmse = np.sqrt(mean_squared_error(y, y_predict))

print(f'R2 : {r2}')
print(f'MAE : {mae}')
print(f'RMSE : {rmse}')

# R^2 how good model shows variability of data ( 0.504 ) normal
# the linear model shows the basic trend but does not take into account
# all variations (seasonality, promotions, large orders)
# MAE ( Mean Absolute Error ) gives an idea of the average error of
# the forecast (how much, on average, the model lags or leads the actual income)
# 175 thousand is a rather large error, but it can be acceptable for an approximate forecast
# RMSE - mean squared Error ( sensible to big deviation )
# highlights the impact of abnormally high or low sales (model accuracy)
# The model shows the general trend well, but individual peak months are predicted less accurately

# Predict for next 6 month
future_month = np.arange(len(monthly_revenue), len(monthly_revenue) + 6).reshape(-1,1)
future_preds = model.predict(future_month)
future_dates = pd.date_range(start=monthly_revenue['month'].iloc[-1] + pd.offsets.MonthBegin(1), periods = 6, freq = 'MS')
forecast_df = pd.DataFrame({'month': future_dates, 'revenue' : future_preds})

plt.figure(figsize = (12,8))
plt.plot(monthly_revenue['month'], monthly_revenue['revenue'], label = 'Fact Data', marker = 'o')
plt.plot(monthly_revenue['month'], y_predict, label = 'Linear Regression', color = 'red')
plt.plot(forecast_df['month'], forecast_df['revenue'], color = 'green', linestyle = '--',marker = 'o', label = 'predict')
plt.title('Predict of revenue (Linear Regression)')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.legend()
plt.grid(True)
plt.show()
# according to the visualization, it is clear that in the future period (6 months) the income will grow
# (based on forecasting and the linear regression model)

orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['month'] = orders['order_purchase_timestamp'].dt.to_period('M')

monthly_order = orders.groupby('month')['order_id'].count().reset_index()
monthly_order['month']= monthly_order['month'].dt.to_timestamp()
monthly_order['month_num'] = np.arange(len(monthly_order))

X1 = monthly_order[['month_num']]
y1 = monthly_order['order_id']

model = LinearRegression()
model.fit(X1, y1)
y_pred = model.predict(X1)

r2o = r2_score(y1, y_pred)
mae_o = mean_absolute_error(y1, y_pred)
rmse_o = np.sqrt(mean_squared_error(y1, y_pred))

print(f'R2 orders : {r2o}')
print(f'MAE orders : {mae_o}')
print(f'RMSE orders : {rmse_o}')

future_months = np.arange(len(monthly_order), len(monthly_order)+6).reshape(-1,1)
future_pred = model.predict(future_months)
future_dates = pd.date_range(start = monthly_order['month'].iloc[-1] + pd.offsets.MonthBegin(1), periods = 6, freq='MS')
future_df  = pd.DataFrame({'month' : future_dates, 'orders' : future_pred})

plt.figure(figsize=(8,6))
plt.plot(monthly_order['month'], monthly_order['order_id'], label = 'Fact (count of orders)', marker = 'x')
plt.plot(monthly_order['month'],y_pred, label = 'Regression line', linestyle = '--')
plt.plot(future_df['month'], future_df['orders'],label = 'Predict 6 month', marker = 'o', color = 'red')
plt.xlabel('Month')
plt.title('Prognose (count of orders) Linear Regression')
plt.ylabel('Count orders')
plt.show()


df = orders.merge(items, on="order_id", how="inner")
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
# Income sorted by orders
df['revenue'] = df['price'] + df['freight_value']
# include month
df['month'] = df['order_purchase_timestamp'].dt.to_period('M')
# Average chek group by month
monthly_aov = df.groupby('month').agg({'revenue':'sum','order_id':'nunique'}).reset_index()
monthly_aov['AOV'] = monthly_aov['revenue'] / monthly_aov['order_id']
monthly_aov['month'] = monthly_aov['month'].dt.to_timestamp()
monthly_aov['month_num'] = np.arange(len(monthly_aov))
X = monthly_aov[['month_num']]
y = monthly_aov['AOV']
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)
r2 = r2_score(y, y_pred)
mae = mean_absolute_error(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))
print(f'R2 : {r2}')
print(f'MAE : {mae}')
print(f'RMSE : {rmse}')
# Predict for average chek
future_months = np.arange(len(monthly_aov), len(monthly_aov)+6).reshape(-1,1)
future_preds = model.predict(future_months)
future_dates = pd.date_range(start=monthly_aov['month'].iloc[-1] + pd.offsets.MonthBegin(1), periods=6, freq='MS')
forecast_df = pd.DataFrame({'month': future_dates, 'AOV': future_preds})

plt.figure(figsize=(10,6))
plt.plot(monthly_aov['month'], monthly_aov['AOV'], label='Fact (AOV)', marker='o')
plt.plot(monthly_aov['month'], y_pred, label='Linear Regression', linestyle='--')
plt.plot(forecast_df['month'], forecast_df['AOV'], label='Predict (6 month)', marker='x', color='red')
plt.title('Predict for average check  (AOV) (Linear Regression)')
plt.xlabel('Month')
plt.ylabel('AOV (average check)')
plt.grid(True)
plt.show()
print(forecast_df)
#the value of p2 is close to zero (0.08), this means that the model covers only 8% of the data, so using linear
# regression prediction is not effective, it is easier to use basic mean prediction here

monthly_avg_ticket = df_predict.groupby('month')['revenue'].mean().reset_index()
monthly_avg_ticket['month']= monthly_avg_ticket['month'].dt.to_timestamp()
# Basic predict - mean value
avg_value = monthly_avg_ticket['revenue'].mean()
# predict for 6 month
future_dates = pd.date_range(start=monthly_avg_ticket['month'].iloc[-1] + pd.offsets.MonthBegin(1), periods=6, freq='MS')
forecast_df = pd.DataFrame({'month': future_dates,'avg_ticket_forecast': [avg_value] * 6})

print("Mean value:", avg_value)
print(forecast_df)

plt.figure(figsize=(8,5))
plt.plot(monthly_avg_ticket['month'], monthly_avg_ticket['revenue'], label='Fact')
plt.hlines(avg_value, monthly_avg_ticket['month'].min(), future_dates[-1], colors='red', linestyles='dashed', label='Mean (predict)')
plt.scatter(forecast_df['month'], forecast_df['avg_ticket_forecast'], color='orange', label='Predict')
plt.title('Predict average check')
plt.xlabel('Month')
plt.ylabel('Average check')
plt.legend()
plt.show()


# he average check remains almost at the same level of 135-140, this indicates stability, a simple noticeable gradual
# decrease in the average value of a check (this can be influenced by many factors, such as the economic situation and
# the ability of customers to pay, as well as the economic situation directly in the country and in the world)

# Analysis and forecasting of basic indicators (revenue, number of orders and average check) allows companies to
# formulate the right approach in terms of marketing, logistics, and choice of strategies. In the future, it is
# possible to analyze products that will be in the greatest demand in the future and for which demand is growing.