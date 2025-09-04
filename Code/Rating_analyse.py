import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

reviews = pd.read_csv('../DataSet/olist_order_reviews_dataset.csv')
conn = sqlite3.connect('../DataSet/review_r.db')
reviews.to_sql('reviews',conn, index=False, if_exists='replace')
query_rev = """
Select
    review_score, COUNT(*) as count_reviews
FROM reviews
GROUP BY review_score
ORDER BY review_score;
"""
df_reviews = pd.read_sql_query(query_rev, conn)
print(df_reviews.head(10))

plt.figure(figsize=(10,7))
labels = {'Very bad':1,'Bad': 2,'Normal':3,'Good':4,'Very good':5}
plt.pie(x = df_reviews['review_score'],labels=labels , autopct='%1.1f%%')
plt.title('Percentage of reviews')
plt.show()

# Most customer reviews are positive, with 33.3% rating 5 (very good), 26.7% rating 4 (good),
# and only 20% (6.7% very bad and 13.3% bad) having negative reviews. Overall, these are positive
# indicators, it is worth exploring these metrics more deeply and finding out what the patterns are.