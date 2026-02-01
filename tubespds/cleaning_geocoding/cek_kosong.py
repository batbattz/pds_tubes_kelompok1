import pandas as pd

# Load data dari file CSV
df_sppg= pd.read_csv('data_koordinat4.csv')

df_sppg_clean = df_sppg.dropna(subset=['latitude', 'longitude'])
# Hapus juga jika koordinatnya berupa angka 0 
df_sppg_clean = df_sppg_clean[(df_sppg_clean['latitude'] != 0) & (df_sppg_clean['longitude'] != 0)]
df_sppg = df_sppg.drop(columns=['alamat_lengkap'])
#  Lihat perbandingannya
print(f"Jumlah data awal: {len(df_sppg)}")
print(f"Jumlah data setelah dihapus yang kosong: {len(df_sppg_clean)}")
print(f"Data yang dibuang: {len(df_sppg) - len(df_sppg_clean)}")

df_sppg_clean.to_csv("data_koordinat_ready.csv", index=False)