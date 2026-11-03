import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Dashboard Analisis Penyewaan Sepeda",
    page_icon="🚲",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('day.csv')
    # Preprocessing / Cleaning data
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['season'] = df['season'].map({1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    df['weathersit'] = df['weathersit'].map({
        1: 'Clear/Few Clouds', 
        2: 'Mist/Cloudy', 
        3: 'Light Snow/Rain', 
        4: 'Heavy Rain/Ice'
    })
    
    # Binning suhu untuk analisis lanjutan
    bins = [0.0, 0.3, 0.6, 1.0]
    labels = ['Cold', 'Warm', 'Hot']
    df['temp_category'] = pd.cut(df['temp'], bins=bins, labels=labels)
    return df

day_df = load_data()

# Judul Dashboard
st.title("🚲 Dashboard Interaktif Analisis Penyewaan Sepeda")
st.markdown("Proyek Analisis Data - Bike Sharing Dataset")
st.markdown("---")

# Sidebar untuk Filter Interaktif
st.sidebar.header("🔍 Filter Data")

# Filter berdasarkan Musim
selected_season = st.sidebar.multiselect(
    "Pilih Musim:",
    options=day_df['season'].unique(),
    default=day_df['season'].unique()
)

# Filter berdasarkan Kondisi Cuaca
selected_weather = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca:",
    options=day_df['weathersit'].unique(),
    default=day_df['weathersit'].unique()
)

# Filter dataframe berdasarkan sidebar
filtered_df = day_df[
    (day_df['season'].isin(selected_season)) & 
    (day_df['weathersit'].isin(selected_weather))
]

# Menampilkan Metrik Utama di Bagian Atas
col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = filtered_df['cnt'].sum()
    st.metric("Total Penyewaan Sepeda", value=f"{total_rentals:,}")
with col2:
    avg_rentals = int(filtered_df['cnt'].mean())
    st.metric("Rata-rata Penyewaan Harian", value=f"{avg_rentals:,}")
with col3:
    total_days = filtered_df.shape[0]
    st.metric("Total Hari Teranalisis", value=f"{total_days} Hari")

st.markdown("---")

# Layout Visualisasi 1 & 2 (Berdampingan)
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Pengaruh Kondisi Cuaca terhadap Penyewaan")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=filtered_df, 
        x='weathersit', 
        y='cnt', 
        estimator='mean', 
        palette='Blues_d', 
        ax=ax,
        order=['Clear/Few Clouds', 'Mist/Cloudy', 'Light Snow/Rain']
    )
    ax.set_title("Rata-rata Penyewaan Berdasarkan Cuaca", fontsize=11, fontweight='bold')
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan")
    plt.xticks(rotation=15)
    st.pyplot(fig)

with col_chart2:
    st.subheader("Perbandingan Penyewaan Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 5))
    season_order = ['Springer', 'Summer', 'Fall', 'Winter']
    sns.barplot(
        data=filtered_df, 
        x='season', 
        y='cnt', 
        order=season_order, 
        estimator='mean', 
        palette='Greens_d', 
        ax=ax
    )
    ax.set_title("Rata-rata Penyewaan Berdasarkan Musim", fontsize=11, fontweight='bold')
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

st.markdown("---")

# Layout Visualisasi 3: Analisis Lanjutan (Binning Suhu)
st.subheader("🌡️ Analisis Lanjutan: Pengaruh Kategori Suhu terhadap Penyewaan")
fig, ax = plt.subplots(figsize=(10, 4))
sns.barplot(
    data=filtered_df, 
    x='temp_category', 
    y='cnt', 
    order=['Cold', 'Warm', 'Hot'],
    estimator='mean', 
    palette='Oranges_d', 
    ax=ax
)
ax.set_title("Rata-rata Penyewaan Berdasarkan Kategori Suhu", fontsize=11, fontweight='bold')
ax.set_xlabel("Kategori Suhu")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)

# Catatan kaki / Informasi
st.markdown("---")
st.caption("Dibuat untuk memenuhi kriteria submission kelas Belajar Analisis Data dengan Python - Dicoding.")