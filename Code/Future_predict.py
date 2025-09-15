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