import pandas as pd
import json

def clean_geojson_with_pandas(input_path, output_path):
    #  Load GeoJSON asli
    with open(input_path, 'r') as f:
        data = json.load(f)

    # Ambil bagian 'features' dan ubah 'properties' menjadi DataFrame Pandas
    # Ini mengubah metadata peta menjadi tabel (rows & columns)
    features = data['features']
    df_prop = pd.json_normalize([f['properties'] for f in features])

    #  Gunakan kekuatan Pandas untuk membersihkan nama
    # Kita bersihkan kolom 'KECAMATAN' (atau sesuaikan jika namanya 'kcamatan')
    target_col = 'KECAMATAN' if 'KECAMATAN' in df_prop.columns else 'kcamatan'
    
    # Hapus semua spasi, tab, newline, dan jadikan KAPITAL
    df_prop[target_col] = df_prop[target_col].astype(str).str.replace(r'\s+', '', regex=True).str.upper()

    #  Masukkan kembali data yang sudah bersih ke objek original
    cleaned_list = df_prop.to_dict(orient='records')
    for i in range(len(features)):
        features[i]['properties'] = cleaned_list[i]

    #  Simpan sebagai file GeoJSON baru
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Sukses! File '{output_path}' siap digunakan tanpa spasi tengah.")

# Jalankan fungsi
clean_geojson_with_pandas("Jabar_By_Kecsimple.json", "Jabar_Kec_clean.json")