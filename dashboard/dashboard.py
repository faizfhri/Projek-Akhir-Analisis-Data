import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set theme and layout
st.set_page_config(page_title="Dashboard Visualisasi Data E-Commerce", layout="wide")

st.title("Dashboard Visualisasi Data E-Commerce")
st.subheader("m011b4ky2812 - Muhammad Faiz Fahri")

st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
        padding: 20px;
    }
    h1 {
        color: #2c3e50;
        font-family: 'Arial', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

customers_df = pd.read_csv('data/customers_dataset.csv')
sellers_df = pd.read_csv('data/sellers_dataset.csv')
geolocation_df = pd.read_csv('data/geolocation_dataset.csv')
products_df = pd.read_csv('data/products_dataset.csv')
order_items_df = pd.read_csv('data/order_items_dataset.csv')

geolocation_df.drop_duplicates(inplace=True)
products_df['product_name_lenght'] = products_df['product_name_lenght'].fillna(products_df['product_name_lenght'].median())
products_df['product_description_lenght'] = products_df['product_description_lenght'].fillna(products_df['product_description_lenght'].median())
products_df['product_photos_qty'] = products_df['product_photos_qty'].fillna(products_df['product_photos_qty'].median())
products_df['product_category_name'] = products_df['product_category_name'].fillna('Unknown')
products_df.dropna(subset=['product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm'], inplace=True)
order_items_df["shipping_limit_date"] = pd.to_datetime(order_items_df["shipping_limit_date"])

st.header("Distribusi jumlah pelanggan dan penjual berdasarkan provinsi di Brasil")

customer_geolocation = pd.merge(customers_df, geolocation_df, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')
seller_geolocation = pd.merge(sellers_df, geolocation_df, left_on='seller_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')

customer_geolocation = customer_geolocation.dropna(subset=['geolocation_state'])
seller_geolocation = seller_geolocation.dropna(subset=['geolocation_state'])

customer_counts = customer_geolocation['geolocation_state'].value_counts().reset_index()
customer_counts.columns = ['state', 'customer_count']
seller_counts = seller_geolocation['geolocation_state'].value_counts().reset_index()
seller_counts.columns = ['state', 'seller_count']

location_summary = pd.merge(customer_counts, seller_counts, on='state', how='outer').fillna(0)

fig, ax = plt.subplots(figsize=(10, 6))
location_summary.set_index('state').plot(kind='bar', ax=ax)
plt.title('Distribution of Customers and Sellers by State')
plt.xlabel('State')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(['Customer Count', 'Seller Count'])
plt.tight_layout()

st.pyplot(fig)

st.header("Rata-rata harga produk berdasarkan kategori")

order_products = pd.merge(order_items_df, products_df, on='product_id', how='left')

category_availability = order_products['product_category_name'].value_counts().reset_index()
category_availability.columns = ['product_category_name', 'product_count']
most_available_category = category_availability.loc[category_availability['product_count'].idxmax()]

avg_price_per_category = order_products.groupby('product_category_name')['price'].mean().reset_index()

# Sort the average price per category from highest to lowest
avg_price_per_category = avg_price_per_category.sort_values(by='price', ascending=True)

fig2, ax2 = plt.subplots(figsize=(10, 12))
ax2.barh(avg_price_per_category['product_category_name'], avg_price_per_category['price'], color='#3498db')
ax2.set_title('Average Product Price by Category')
ax2.set_xlabel('Average Price')
ax2.set_ylabel('Product Category')
plt.tight_layout()

st.pyplot(fig2)

st.write("Most available product category:", most_available_category)
st.write("Average product price by category:")
st.dataframe(avg_price_per_category)
