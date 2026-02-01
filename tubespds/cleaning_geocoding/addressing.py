from geopy.geocoders import Nominatim
import pandas as pd
import os

data = pd.read_csv("alamat.csv",sep=",")
data["alamat_lengkap"] = (data["kecamatan"]+","+data["kota"]+","+data["provinsi"]+","+"indonesia").str.lower()
data_clean = data.drop_duplicates()

cp_addressing = "data_alamat.csv"

if os.path.exists(cp_addressing):
     processed = pd.read_csv(cp_addressing) 
     start_index = len(processed) 
     print(f"Melanjutkan dari baris ke-{start_index}") 
else:
    processed = pd.DataFrame(columns=data_clean.columns) 
    start_index = 0 
    print("Memulai dari awal")

batch_size = 500 
for i in range(start_index, len(data_clean), batch_size): 
    batch = data_clean.iloc[i:i+batch_size] 
    processed = pd.concat([processed, batch], ignore_index=True) 
    processed.to_csv(cp_addressing, index=False, encoding="utf-8") 
    print(f"Checkpoint disimpan sampai baris ke-{i+len(batch)}")


    
