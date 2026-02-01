import pandas as pd
import folium
from folium.plugins import MarkerCluster
import streamlit as st
import os
import json

@st.cache_resource
def create_mark(datak):
    data = datak
    #titik awal
    center_lat = data["latitude"].dropna().mean()
    center_lon = data["longitude"].dropna().mean()

    m = folium.Map(location=[center_lat, center_lon],zoom_start=11,max_zoom=15,min_zoom=9,tiles="OpenStreetMap")
    marker_cluster = MarkerCluster().add_to(m)
    #nambahin marker
    for idx, row in data.iterrows():
        if pd.notnull(row["latitude"]) and pd.notnull(row["longitude"]):
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=f"{row['nama_sppg']}<br>{row['kecamatan']}",
                tooltip=row['kecamatan'],
                prefer_canvas=True
                        ).add_to(marker_cluster)
    return m
def create_choropleth_map(df_final, geojson):
    m = folium.Map(location=[-6.9175, 107.6191], zoom_start=10,max_zoom=11,min_zoom=9, tiles='CartoDB voyager')
    
    #
    folium.Choropleth(
        geo_data=geojson,
        name="Prioritas Kebutuhan",
        data=df_final,
        columns=['kecamatan', 'priority_score'],
        key_on="feature.properties.KECAMATAN",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Skor Prioritas (Semakin Merah = Semakin Butuh)",
        nan_fill_color="grey",
        prefer_canvas=True
    ).add_to(m)

    
    score_dict = df_final.set_index('kecamatan')['priority_score'].to_dict()

    folium.GeoJson(
        geojson,
        style_function=lambda x: {'fillColor': '#ffffff00', 'color': '#00000000', 'weight': 0}, # Transparan
        tooltip=folium.GeoJsonTooltip(
            fields=['KECAMATAN'], # Nama field di JSON Anda
            aliases=['Kecamatan: '],
            localize=True,
            sticky=True,
            labels=True
        )
    ).add_to(m)

    return m
@st.cache_data
def load_geojson(relative_path):
    base_path = os.getcwd()
    full_path = os.path.join(base_path, relative_path)
    
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)

# m.save("peta_sppg4.html")






