import pandas as pd


df_sekolah = pd.read_excel("Data_Sekolah_jawabarat.xlsx")
df_sppg = pd.read_csv("data_koordinat_ready.csv")

#memfilter data sekolah
def clean_area_names(df, kec_col, kab_col):
    # Standardisasi Dasar
    df[kec_col] = df[kec_col].astype(str).str.upper().str.strip()
    df[kab_col] = df[kab_col].astype(str).str.upper().str.strip()
    
    # Hapus Simbol & Singkatan yang sering bikin beda
    # Menghapus titik (misal: BL. -> BL) dan koma
    df[kec_col] = df[kec_col].str.replace(r'[.,]', '', regex=True)
    
    # Bersihkan Prefix Wilayah
    df[kec_col] = df[kec_col].str.replace(r'^KEC\s+', '', regex=True)
    df[kab_col] = df[kab_col].str.replace(r'KAB\.|KOTA|KABUPATEN', '', regex=True).str.strip()
    
    
    # hapus semua spasi HANYA untuk perbandingan, tapi simpan format aslinya
    df[kec_col] = df[kec_col].str.replace(r'\s+', '', regex=True)
    
    return df
df_sekolah_unique = clean_area_names(df_sekolah, 'kecamatan', 'Kab/Kota')
df_sppg = clean_area_names(df_sppg, 'kecamatan', 'kota') # 'kota' adalah nama asli di file koordinat
df_sppg = df_sppg.rename(columns={'kota': 'Kab/Kota'})

#merging
if 'Kab/Kota' in df_sppg.columns:
    sppg_count = df_sppg.groupby(['Kab/Kota', 'kecamatan']).size().reset_index(name='jumlah_sppg')
    df_merge = pd.merge(df_sekolah_unique, sppg_count, on=['Kab/Kota', 'kecamatan'], how='left')
else:
    # Jika SPPG tidak punya kolom Kab/Kota, lakukan drop_duplicates pada data sekolah dulu
    # agar satu kecamatan hanya ada satu baris sebelum di-merge
    sppg_count = df_sppg.groupby('kecamatan').size().reset_index(name='jumlah_sppg')
    df_merge = pd.merge(df_sekolah_unique, sppg_count, on='kecamatan', how='left')
#isi data kosong dng nilai 0
df_merge['jumlah_sppg'] = df_merge['jumlah_sppg'].fillna(0).astype(int)
#menghitung weighted priority score
df_merge['priority_score'] = (df_merge['TOTAL'] - df_merge['jumlah_sppg']) * (1+ (1/(df_merge['jumlah_sppg'] + 1 )))
df_merge['priority_score'] = df_merge['priority_score'].round(2)
#make sure hilangin spasi atau text terpotong
df_merge['kecamatan'] = df_merge['kecamatan'].str.replace(' ', '', regex=False)
df_merge.to_csv("data_final_priority.csv", index=False)

print(df_merge.head())
print("Total Data SPPG asli (setelah geocoding):", len(df_sppg))
print("Total Data SPPG di hasil akhir (sum):", df_merge['jumlah_sppg'].sum())

sppg_only = pd.merge(sppg_count,df_sekolah_unique, on=['Kab/Kota','kecamatan'], how='left', indicator=True)
data_hilang = sppg_only[sppg_only['_merge'] == 'left_only']

print("Daftar Kecamatan yang datanya hilang:")
print(data_hilang[['Kab/Kota', 'kecamatan', 'jumlah_sppg']])
print(f"Total data yang tidak ter-merge: {data_hilang['jumlah_sppg'].sum()}")

