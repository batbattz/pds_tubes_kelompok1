from scrapping.driver import create_driver
from scrapping.extract import extract_rows,cari_daerah
from scrapping.saveCSV import save_records
from scrapping.pagination import scroll_table,get_max_page,click_next
import time
import os
import random


#CP
def get_checkpoint(file_path="cp.txt"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            content = f.read().strip()
            if content:
                return int(content)
    return 1
def save_checkpoint(page, file_path="cp.txt"):
    with open(file_path, "w") as f:
        f.write(str(page))

# SCRAPING
driver = create_driver()
cari_daerah(driver, "jawa barat")
scroll_table(driver,timeout=10)
max=get_max_page(driver)
print(f"halaman = {max}")

current_page = get_checkpoint() 
print(f"Melanjutkan dari halaman: {current_page}")
if current_page > 1:
    target_url = f"https://bgn.go.id/operasional-sppg/?page={current_page}&search=jawa%20barat"
    driver.get(target_url)
time.sleep(3)
    
while current_page <=max:
    print(f"Scraping halaman {current_page}/{max}")
    time.sleep(random.uniform(2,3))
    scroll_table(driver, timeout=5)  
    
    data = extract_rows(driver)
    data_list = list(data)
    print(f"debug : data ditemukan{len(data_list)}") 
    if len(data_list) > 0:
        save_records("data.csv", data_list) 
        save_checkpoint(current_page)
    else:
        print("Tidak ada data untuk disimpan.")
    
    if current_page < max:
        next_page = click_next(driver)  
        if next_page is None:
            break  
        current_page = next_page  # Update current_page
        time.sleep(random.uniform(2,3))
    else:
        break  

time.sleep(10)
driver.quit()  


