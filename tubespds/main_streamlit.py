import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from map_engine.maping import create_mark, create_choropleth_map,load_geojson
from cleaning_geocoding.diagrambatangprio import create_priority_chart
from cleaning_geocoding.diagrambatangterbanyak import create_top_10_chart

st.set_page_config(layout="wide")
@st.cache_data
def load_data():
    df = pd.read_csv("tubespds/cleaning_geocoding/data_koordinat_ready.csv")
    df2 = pd.read_csv("tubespds/cleaning_geocoding/data_final_priority.csv")
    geojson_data = load_geojson("tubespds/Jabar_Kec_clean.json") 
    return df, df2, geojson_data
df, df2, geojson_data = load_data()

st.title("Pemetaan GIS Tingkat Kecamatan untuk Penentuan Urgensi Pembangunan SPPG Berdasarkan Sebaran Sekolah SD/SMP/SMA/SMK di Jawa Barat")
st.divider()
placeholder = st.empty()
col_peta, col_stats = st.columns([4, 1])

with col_stats:
    mode_peta = st.radio(
        "Pilih Mode Visualisasi:",
        ["Peta Prioritas Kebutuhan","Peta Persebaran Lokasi"],
        index=0
    )
with col_stats:
    st.subheader("Statistik")
    total_sekolah = df2['TOTAL'].sum()
    total_sppg = df2["jumlah_sppg"].sum()
    total_kecamatan = len(df2['kecamatan'])
    st.metric("Total Sekolah", value=f"{total_sekolah:,}")
    st.metric("Total Sppg", value=f"{total_sppg:,}")
    st.metric("Total Kecamatan", value=f"{total_kecamatan:,}")
    st.text("data per tanggal 16 Januari 2026")
with col_peta:
    container = st.container()
    if mode_peta == "Peta Persebaran Lokasi":
        placeholder.subheader("Peta Persebaran SPPG")
        df_unique = df.drop_duplicates(subset=['latitude', 'longitude'])
        peta = create_mark(df_unique)
        print("loading map mark")
        
    else:
        placeholder.subheader("Peta Prioritas Kecamatan")
        
        peta = create_choropleth_map(df2, geojson_data)
    with container:
        st_folium(
            peta, 
            use_container_width=True, 
            height=550, 
            key=f"display_{mode_peta}", #mencegah duplikasi
            returned_objects=[]
        )
        print("loading map choroplath")
st.divider()
col_tabel,col_text  = st.columns([1.8,1])
col_diagraml, col_diagramr  = st.columns([1,2])
col_diagraml2, col_diagramr2 = st.columns([2,1])


with col_tabel:
    st.subheader("Analisis Prioritas Pembangunan Titik SPPG")
    st.text("Tabel di bawah ini menyajikan daftar wilayah di Jawa Barat yang memiliki urgensi pembangunan atau penambahan titik layanan SPPG paling mendesak.")
    df_prio = df2[['Kab/Kota','kecamatan','TOTAL','jumlah_sppg','priority_score']].copy()
    df_prio = df_prio.sort_values(by='priority_score', ascending=False)
    df_prio.insert(0, 'No', range(1, len(df_prio) + 1))
    df_prio.columns = ['No', 'Kabupaten/Kota', 'Kecamatan', 'Jumlah Sekolah', 'JumlahSPPG', 'Nilai Prioritas']
    st.dataframe(df_prio,use_container_width=True,hide_index=True)
with col_text:
    st.subheader("")
    st.subheader("")
    st.write("")
    st.text("Di tabel tersebut kita bisa lihat ada nama-nama kecamatan yang memiliki ketimpangan antara jumlah sekolah dan jumlah sppg. Kecamatan yang memerlukan pembangunan sppg dilihat dari priority score yang dicari menggunakan rumus berikut :")
    st.image("rumus.jpeg")
    st.write("Logika rumus ini secara sengaja memberikan bobot atau penalti lebih berat pada kecamatan yang memiliki jumlah layanan SPPG sangat minim atau bahkan nol, sehingga urgensi pembangunannya akan terlihat lebih menonjol.")
    st.write("")
with col_diagraml:
    st.subheader("")
    st.subheader("")
    st.write("Ini adalah visualisasi dari 10 kecamatan dengan priority score/nilai prioritas tertinggi di jawabarat. Grafik ini menjadi titik rekomendasi pembangunan sppg tambahan di tingkat kecamtan")
    st.text("")
with col_diagramr:
    st.subheader("")
    fig_sppg = create_priority_chart(df2)
    
    # Tampilkan di Streamlit
    st.pyplot(fig_sppg)

with col_diagraml2:
    st.subheader("")
    
    fig_sppg2 = create_top_10_chart(df2)
    
    
    st.pyplot(fig_sppg2)
with col_diagramr2:
    st.subheader("")
    st.subheader("")
    st.write("Ini adalah visualisasi 10 kecamatan dengan jumah sppg terbanyak di jawa barat")
st.divider()
st.write("data yang digunakan ada dibawah ini")
with st.expander("Lihat Data SPPG"):
    st.write("Berikut adalah data alamat sppg di tiap kecamatan yang dipakai :")
    
    # Menampilkan dataframe asli (df2) di dalam expander
    st.dataframe(df, use_container_width=True)
    
    # Tombol opsional untuk mengunduh data sebagai CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name='data_sppg_jabar.csv',
        mime='text/csv',
    )
with st.expander("Lihat Data Sekolah"):
    st.write("Berikut adalah data sekolah di tiap kecamatan yang dipakai :")
    
    # Menampilkan dataframe asli (df2) di dalam expander
    st.dataframe(df2, use_container_width=True)
    
    # Tombol opsional untuk mengunduh data sebagai CSV
    csv = df2.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name='data_sekolah_jabar.csv',
        mime='text/csv',

    )
