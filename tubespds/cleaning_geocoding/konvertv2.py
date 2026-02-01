import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import os
from tqdm import tqdm


geolocator = Nominatim(user_agent="geoapi_example")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Baca data
data = pd.read_csv("data_alamat.csv", sep=",")

# Tambahkan kolom latitude & longitude kosong jika oweh
if "latitude" not in data.columns:
    data["latitude"] = None
if "longitude" not in data.columns:
    data["longitude"] = None

# Variabel checkpoint
cp_koordinat = "data_koordinat4.csv"


if os.path.exists(cp_koordinat):
    data = pd.read_csv(cp_koordinat)
    start_index = data[data["latitude"].isna() | data["longitude"].isna()].index.min()
    if pd.isna(start_index):
        start_index = len(data)  # semua sudah selesai
    print(f"Melanjutkan dari baris ke-{start_index}")
else:
    start_index = 0
    print("Memulai dari awal")


def get_coor(address):
    try:
        location = geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error pada {address}: {e}")
        return None, None


batch_size = 500
for i in tqdm(range(start_index, len(data)), desc="Proses geocoding"):
    if pd.isna(data.at[i, "latitude"]) or pd.isna(data.at[i, "longitude"]):
        lat, lon = get_coor(data.at[i, "alamat_lengkap"])
        data.at[i, "latitude"] = lat
        data.at[i, "longitude"] = lon

    # Simpan checkpoint setiap batch
    if i % batch_size == 0 or i == len(data) - 1:
        data.to_csv(cp_koordinat, index=False, encoding="utf-8")
        print(f"Checkpoint disimpan di baris ke-{i}")

print(f"Proses geocoding selesai. Hasil akhir ada di {cp_koordinat}")
