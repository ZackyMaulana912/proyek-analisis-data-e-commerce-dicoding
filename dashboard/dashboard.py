import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Set tema
sns.set(style='dark')

def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    df = pd.read_csv(file_path)
    return df

all_df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.header("Zacky Maulana")
    st.image("https://github.com/apple-touch-icon.png", width=50) 
    
    st.header("Filter Eksplorasi")
    # Filter 1: Kategori Produk
    category_list = ["Semua Kategori"] + sorted(all_df['product_category_name_english'].unique().tolist())
    selected_category = st.selectbox("Pilih Kategori Produk:", category_list)
    
    # Filter 2: Pilih Kota (Tambahan untuk Bintang 5!)
    city_list = ["Semua Kota"] + sorted(all_df['customer_city'].unique().tolist())
    selected_city = st.selectbox("Pilih Kota Pelanggan:", city_list)

# --- LOGIKA FILTER BERLAPIS ---
main_df = all_df.copy()
if selected_category != "Semua Kategori":
    main_df = main_df[main_df['product_category_name_english'] == selected_category]
if selected_city != "Semua Kota":
    main_df = main_df[main_df['customer_city'] == selected_city]

# --- MAIN PAGE ---
st.title("E-Commerce Insight Dashboard ")

# --- Bagian 1: Performa Penjualan ---
st.header("Performa Penjualan")
col1, col2 = st.columns(2)

with col1:
    total_orders = main_df['order_id'].nunique()
    st.metric("Total Pesanan", value=f"{total_orders:,}")
with col2:
    total_revenue = main_df['price'].sum()
    st.metric("Total Pendapatan", value=f"BRL {total_revenue:,.2f}")

st.markdown("---")

# --- Bagian 2: Visualisasi Produk ---
st.subheader("Top 5 Kategori Produk")

# Logika cerdas: Jika user pilih 'Semua', tampilkan Top 5. 
# Jika user pilih satu kategori, tampilkan kategori tersebut dibandingkan rata-rata/total.
if selected_category == "Semua Kategori":
    viz_df = all_df.groupby('product_category_name_english').order_id.nunique().sort_values(ascending=False).head(5).reset_index()
else:
    # Menampilkan performa kategori terpilih di antara 4 kategori teratas lainnya
    top_4_others = all_df[all_df['product_category_name_english'] != selected_category].groupby('product_category_name_english').order_id.nunique().sort_values(ascending=False).head(4).reset_index()
    this_cat = all_df[all_df['product_category_name_english'] == selected_category].groupby('product_category_name_english').order_id.nunique().reset_index()
    viz_df = pd.concat([this_cat, top_4_others]).sort_values(by='order_id', ascending=False)

fig, ax = plt.subplots(figsize=(12, 5))
# Memberi warna berbeda pada kategori yang dipilih user
colors = ["#72BCD4" if c == selected_category else "#D3D3D3" for c in viz_df['product_category_name_english']]

sns.barplot(x="order_id", y="product_category_name_english", data=viz_df, palette=colors, hue="product_category_name_english", legend=False, ax=ax)
ax.set_title(f"Posisi Performa: {selected_category}", fontsize=15)
ax.set_xlabel("Jumlah Pesanan")
ax.set_ylabel(None)

# JAWABAN REQUEST SKALA: Jika kamu ingin skala tetap (misal max 15.000)
# ax.set_xlim(0, 15000) 

st.pyplot(fig)

# --- Bagian 3: Demografi ---
st.header("Demografi Pelanggan")
st.subheader("Top 10 Kota")
top_cities = main_df.groupby('customer_city').customer_id.nunique().sort_values(ascending=False).head(10).reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x="customer_id", y="customer_city", data=top_cities, palette="Blues_r", hue="customer_city", legend=False, ax=ax2)
ax2.set_title(f"Kota dengan Pembelian Terbanyak ({selected_category})")
st.pyplot(fig2)

st.caption("Copyright (c) Zacky Maulana 2026")
