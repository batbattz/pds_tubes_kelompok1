import csv
import os

def save_records(csv_path, records):
    exists = os.path.exists(csv_path)
   
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow(
                ["no","provinsi","kota", "kecamatan", "kelurahan","nama_sppg"]
            )

        for record in records:
            print(f"simpan{record} cek panjang {len(records)}")
            if len(record)==6:
                writer.writerow(record)
                print("data disimpan")
            else:
                print("data tidak valid",record)
        f.flush()
        
        os.fsync(f.fileno())

