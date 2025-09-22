# Portfolio_Data_Analytics
The repository is designed to demonstrate practical skills in the field of data analytics
📊  E-commerce Data Analysis

📖 Project Description

This project is dedicated to a comprehensive analysis of the Olist Brazilian E-commerce dataset.
The main goal was to explore customer behavior, seller performance, logistics efficiency, reviews, demographics, and finally to build basic forecasts for future business performance.

The analysis was performed using Python (Pycharm)(Jupyter Notebook) with SQL integration, and complemented with Power BI dashboards (Tableau) and a presentation (PowerPoint).

⸻

🛠 Tech Stack
 • Python: pandas, numpy, matplotlib, seaborn, folium, scikit-learn
 • SQL: SQLite3 for querying large datasets
 • Visualization: Matplotlib, Folium, Power BI
 • Presentation: PowerPoint

 ## Project Structure 🗃️
 ''' Code
 ┣ Demografic_analyse.py                                -   Python file with Demografic analyse
 ┣ Exploatory_Analyse.py                                -   Python file with Exploatory (Basic) Analyse
 ┣ Intro_preparing_and_cleaning                         -   Python file with first view and understandig of information
 ┣ Rating_analyse.py                                    -   Python file with analyse of Ratings (Orders ant grades from Customers)
 ┣ Sellers.py                                           -   Python file with Sallers analyse and information
 ┣ Time_analyse.py                                      -   Python file with time analyse 
 ┣ Future_predict.py                                    -   Python file with predictions (Linear regression/ mean)
  DataSet
 ┣ db files                                             -   Data Base
 ┣ csv files                                            -   sources of information
  results
 ┣ E-commerce Analyse (Brazil).ipynb                    -  Jupiter Notebook file with results of code
 ┣ E-commerce Analyse (Brazil)(without results).ipynb   -  Jupiter Notebook file without results of code '''

 Key Stages of Analysis

1. Time Analysis
 • Orders distribution: majority of purchases are made between 5 p.m. – 11 p.m. (free time after work).
 • Delivery performance:
 • Average delivery time: 7–8 days
 • Delays: ~15% of orders
 • Early deliveries: ~25% of orders (delivered before estimated date).

📈 Insight: Logistics efficiency directly affects customer satisfaction. Improving delivery times could reduce negative reviews significantly.

⸻

2. Reviews & Ratings
 • Overall average review score: 4.08 / 5.
 • Products with highest reviews: electronics, books, and home appliances.
 • Sentiment analysis via SQL LIKE patterns (Portuguese keywords):
 • Positive reviews: >70% contain words like ótimo, excelente.
 • Negative reviews often mention ruim, pessimo, atraso.

📉 Insight: Late deliveries are the #1 reason for negative reviews, not product quality.

⸻

3. Demographics (Customers)
 • Customer distribution:
 • Top states: São Paulo (SP), Rio de Janeiro (RJ), Minas Gerais (MG).
 • Top cities: São Paulo, Rio de Janeiro, Belo Horizonte, Brasília, Curitiba.
 • Heatmap (Folium) clearly shows concentration around southeastern Brazil.
 • Repeat customers: only ~5–10% of customers make more than one purchase.

📈 Insight: Customer loyalty is very low. Marketing campaigns should target repeat purchases.

⸻

4. Sellers
 • Majority of sellers are concentrated in the same top states as customers.
 • Top-10 sellers generate over 30% of total sales revenue.
 • Top categories sold by top sellers:
 • Computers & Accessories
 • Home Appliances
 • Furniture & Décor
 • Health & Beauty

📊 Visualization:
 • Pie chart of top-10 sellers’ market share
 • Bar chart of product categories by sales among top sellers

📉 Insight: The seller base is highly fragmented. A few large sellers dominate the market, while the majority contribute little.

⸻

5. Forecasting
 • Built a linear regression model to predict monthly revenue.
 • Performance metrics:
 • R² = 0.50 → model explains ~50% of revenue variability
 • MAE = 174,609 → average monthly error
 • RMSE = 287,731 → sensitive to revenue peaks
 • Forecast for next 6 months (basic linear trend):
 • Shows a steady growth trend in revenue
 • But does not capture seasonality or special events

📉 Insight: Linear regression gives only a rough trend. For business use, advanced models like ARIMA, Prophet or ML-based forecasting should be used.

⸻

🔑 Key Insights & Business Recommendations
 1. Logistics is the main driver of customer satisfaction.
 • 15% of deliveries are delayed → reduces ratings.
 • Faster deliveries correlate with higher review scores.
✅ Recommendation: Invest in local warehouses near São Paulo and Rio to reduce delivery times.
 2. Customer loyalty is very low (5–10%).
 • Most customers buy only once.
✅ Recommendation: Introduce loyalty programs, discounts for returning customers.
 3. Sales are dominated by a few sellers.
 • Top 10 sellers control ~30% of the market.
✅ Recommendation: Support small/mid sellers to diversify the market and reduce dependency on large players.
 4. Revenue shows growth but predictions are unstable.
 • R² = 0.50 shows model limitations.
✅ Recommendation: Apply advanced forecasting (Prophet, ARIMA) for seasonality and event-based predictions.
 5. Geographical concentration:
 • Most customers are in the Southeast region.
✅ Recommendation: Optimize logistics hubs in SP, RJ, MG for faster service.

⸻

📎 References
 • Brazilian E-commerce Dataset (Kaggle (https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce))
 • Python libraries: pandas, numpy, matplotlib, scikit-learn, folium

⸻

⚡️ This project demonstrates end-to-end analytics: from data cleaning & SQL queries to business insights, visualization, and forecasting.
