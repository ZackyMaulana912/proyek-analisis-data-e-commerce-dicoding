import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tema seaborn
sns.set(style='dark')

# Menyiapkan fungsi untuk memuat data
def load_data():
    # Membaca file data yang sudah dibersihkan
    df = pd.read_csv("main_data.csv")
    return df

all_df = load_data()

# SIDEBAR
with st.sidebar:
    st.header("Zacky Maulana")
    st.text("Proyek Analisis Data")
    st.text("DICODING")

# MAIN PAGE
st.title("E-Commerce Dashboard")
st.text("Dashboard sederhana ini menampilkan hasil analisis penjualan dan demografi.")

# --- Bagian 1: Performa Penjualan ---
st.header("Performa Penjualan")

# Menyiapkan 2 kolom untuk metrik ringkasan
col1, col2 = st.columns(2)
with col1:
    total_orders = all_df['order_id'].nunique()
    st.metric("Total Pesanan", value=total_orders)
with col2:
    total_revenue = all_df['price'].sum()
    st.metric("Total Pendapatan (BRL)", value=f"{total_revenue:,.2f}")

st.subheader("Kategori Produk Terlaris & Pendapatan Tertinggi")

# Data visualisasi produk
top_sales = all_df.groupby('product_category_name_english').order_id.nunique().sort_values(ascending=False).head(5).reset_index()
top_revenue = all_df.groupby('product_category_name_english').price.sum().sort_values(ascending=False).head(5).reset_index()

# Membuat plot matplotlib yang sama persis seperti di notebook
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors = ["#72BCD4"] + ["#D3D3D3"] * 4

# Plot Jumlah Pesanan
sns.barplot(x="order_id", y="product_category_name_english", data=top_sales, palette=colors, ax=ax[0], hue="product_category_name_english", legend=False)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jumlah Pesanan", fontsize=15)
ax[0].set_title("Berdasarkan Jumlah Pesanan", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=12)

# Plot Total Pendapatan
sns.barplot(x="price", y="product_category_name_english", data=top_revenue, palette=colors, ax=ax[1], hue="product_category_name_english", legend=False)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Total Pendapatan (BRL)", fontsize=15)
ax[1].set_title("Berdasarkan Total Pendapatan", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=12)

# Menampilkan grafik di streamlit
st.pyplot(fig)

# --- Bagian 2: Demografi ---
st.header("Demografi Pelanggan")

st.subheader("Top 10 Kota dengan Pelanggan Terbanyak")
top_cities = all_df.groupby('customer_city').customer_id.nunique().sort_values(ascending=False).head(10).reset_index()

fig2, ax2 = plt.subplots(figsize=(12, 6))
colors_cities = ["#72BCD4"] + ["#D3D3D3"] * 9
sns.barplot(x="customer_id", y="customer_city", data=top_cities, palette=colors_cities, hue="customer_city", legend=False, ax=ax2)

ax2.set_xlabel("Jumlah Pelanggan", fontsize=12)
ax2.set_ylabel(None)
ax2.tick_params(axis='y', labelsize=12)

st.pyplot(fig2)

st.caption("Copyright (c) Zacky Maulana 2026")