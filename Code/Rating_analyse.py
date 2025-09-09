import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from Code.Time_analyse import df_c_time

reviews = pd.read_csv('../DataSet/olist_order_reviews_dataset.csv')
cat_name = pd.read_csv('../DataSet/product_category_name_translation.csv')
products = pd.read_csv('../DataSet/olist_products_dataset.csv')
items = pd.read_csv('../DataSet/olist_order_items_dataset.csv')
conn = sqlite3.connect('../DataSet/review_r.db')
reviews.to_sql('reviews',conn, index=False, if_exists='replace')
cat_name.to_sql('names', conn, if_exists='replace',index = False)
products.to_sql('products', conn, if_exists='replace',index = False)
items.to_sql('items',conn, index= False, if_exists='replace')
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
query_rev_b_p = """
Select 
    COUNT(*) as number_of_reviews,
    AVG(r.review_score) AS avg_review_score, 
    n.product_category_name_english 
FROM items as i
JOIN products p ON i.product_id = p.product_id
Join reviews as r ON i.order_id = r.order_id
JOIN names n ON p.product_category_name = n.product_category_name
GROUP BY n.product_category_name_english
Order by avg_review_score DESC;
"""

df_rev_avg = pd.read_sql_query(query_rev_b_p,conn)
print(df_rev_avg.head(10))

# Visualization for Top 10 height product categories by rating (reviews) and Top 10 low rating

df_rev_avg.head(10).plot(kind='bar', x = 'product_category_name_english' , y ='avg_review_score', legend = False)
plt.title ('Top 10 categories of products by height rating (reviews)')
plt.ylabel('Average review score')
plt.xticks(rotation = 45, ha = 'right')
plt.show()

df_rev_avg.tail(10).plot(kind = 'bar', x = 'product_category_name_english' , y ='avg_review_score',color = 'red', legend = False)
plt.xticks(rotation = 45)
plt.ylabel('Average review score')
plt.title('Top 10 categories of products by low rating (reviews)')
plt.show()

# Based on the visualization of the results, it is possible to distinguish categories of goods with an
# average low or, on the contrary, a high rating (searches and ratings of customers), this makes it
# possible to identify problems and find the reasons for low ratings)

# in more detail, you can look at product ratings directly by the number of reviews on ratings for
# each category.

query_disc = """
SELECT
    COUNT(*) as counts,
    r.review_score, 
    n.product_category_name_english 
FROM items as i
JOIN products p ON i.product_id = p.product_id
Join reviews as r ON i.order_id = r.order_id
JOIN names n ON p.product_category_name = n.product_category_name
GROUP BY n.product_category_name_english, review_score
Order by n.product_category_name_english, review_score;
"""
df_rev_disc = pd.read_sql_query(query_disc,conn)
print(df_rev_disc.head(10))

# change table (pivot)
pivot_rev = df_rev_disc.pivot(index='product_category_name_english', columns = 'review_score', values='counts').fillna(0)
top_category = pivot_rev.sum(axis=1).sort_values(ascending=False).head(10).index
pivot_top = pivot_rev.loc[top_category]
pivot_top.plot(kind='bar',stacked = True, figsize = (10,7))
plt.title('Reviews of top 10 categories')
plt.xticks(rotation = 45)
plt.ylabel('Number of reviews')
plt.xlabel('Category')
plt.show()
# taking into account reviews and sorting by ratings of the top categories, you can observe a positive
# trend and many good customer ratings. In addition, it is possible to observe that the ratings are mostly
# positive (4-5) or negative (1), because there are very few ratings (2-3) compared to the general

# It is also interesting to look at reviews and messages from customers. Since the reviews
# are in Portuguese, we will use a translator and find approximately words that can describe
# the product or be contained in the reviews in order to sort positive and negative comments
# (words like "good", "terrible", "delay", "satisfied", "long", "defect", "recommend")

query_kom = """
SELECT
    SUM(CASE WHEN review_comment_message LIKE '%otimo%' 
        OR review_comment_message LIKE '%excelente' 
        OR review_comment_message LIKE '%bom%' THEN 1 ELSE 0 END) AS positive_commentaries,
    SUM(CASE WHEN review_comment_message LIKE '%ruim%' 
        OR review_comment_message LIKE '%pessimo%' 
        OR review_comment_message LIKE '%atraso%' THEN 1 ELSE 0 END) AS negative_commentaries
FROM reviews
"""
df_rev_kom = pd.read_sql_query(query_kom,conn)
print(df_rev_kom)

df_review_delivery = pd.merge(df_c_time, reviews, on = 'order_id', how = 'inner')
df_review_delivery = df_review_delivery.dropna(subset=['order_delivered_customer_date', 'review_score'])
avg_score_by_delay = df_review_delivery.groupby('delay_days')['review_score'].mean()
print(avg_score_by_delay)

avg_score_by_delay.plot(marker = 'o')
plt.title('Dependence of rating on delivery delay')
plt.xlabel('Count of Days of delay')
plt.ylabel('Average review_score')
plt.show()
# Looking at the graph, it is immediately clear how the rating
# and ratings from customers fall depending on the delay

correlation = df_review_delivery['review_score'].corr(df_review_delivery['delay_days'])
print(f'Correlation between delay and reviews rating: {correlation}')
# -0.26 correlation index means that there is still a dependence of the assessment on the speed
# of delivery and delay, although it is not high enough (this may be due to good evaluations from
# customers not depending on the speed of delivery)

# 1. Most buyers leave positive reviews — the average rating is above 4 points, which indicates overall satisfaction with the service.
# 2. At the same time, there are categories with significantly lower average ratings,
# which may signal problems with the quality of goods or service in these segments.
# 3. Text analysis of reviews showed that buyers most often use positive formulations such as
# “ótimo”, “excelente”, but negative mentions (“ruim”, “atraso”) are often related to delivery issues.
# 4. Preliminary analysis indicates a possible relationship between delivery delay and low ratings —
# this factor is worth checking in more detail.