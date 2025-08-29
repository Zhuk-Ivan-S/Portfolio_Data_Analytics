import pandas as pd


# A large volume of data allows you to use a number of tools for analysis, at first glance
# I understand that I will use SQL to sort and combine datasets for more comfortable calculation
# and visualization of important indicators
# Matplotlib and seaborne will be used for preliminary visualization and highlighting
# of the main analytical processes
# Data processing takes place from the point of view of analysis and business goals, not technical use
# (therefore, for each stage of the analysis, I will create separate pieces of code and separate files)
# First of all lets look on data
# Create function
def csv_reading(path):
    df = pd.read_csv(path)
    print(df.head(10))
    print('Size of dataFrame: ', df.size)
    print('Type of DataFrame: ', df.dtypes)
    print('Column names: ', df.columns)
    print('Missing values: ',df.isnull().sum())
    print('Duplicates: ',f'{df.duplicated().sum()}/{df.value_counts().sum()} rows')
# Use function for customers dataset and make notice
csv_reading('../DataSet/olist_customers_dataset.csv')

# That's show column names, type od data, duplicates and missing values (later I can see some
# incorrect values, mistakes Outliers and so on.)
# Firs look on all datasets (geolocation)
csv_reading('../DataSet/olist_geolocation_dataset.csv')
# In proces I can understand, why so many duplicates and clean that by some column (id, zip code for example)

csv_reading('../DataSet/olist_orders_dataset.csv')
# Some missing values in dates (delivery) - that's not so critic

csv_reading('../DataSet/olist_sellers_dataset.csv')
# All is clean and prepare for analyse

csv_reading('../DataSet/olist_products_dataset.csv')
# Some missing values about category/photo/name but no duplicates (id is unique) that's why i cant
# make some replace or changing with frequency or mean

csv_reading('../DataSet/olist_order_items_dataset.csv')
# Perfect

csv_reading('../DataSet/olist_order_payments_dataset.csv')
# Good

#csv_reading('../DataSet/olist_order_reviews_dataset.csv')
# reviews comments and messages are not so important for analyse ( Score much more important )
csv_reading('../DataSet/product_category_name_translation.csv')
# That's for changing names of products
