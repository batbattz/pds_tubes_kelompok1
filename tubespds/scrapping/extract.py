from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def cari_daerah(driver, keyword):
    driver.get("https://www.bgn.go.id/operasional-sppg/?page=1&search=")

    search_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "search-input"))
    )

    search_input.clear()
    search_input.send_keys(keyword + Keys.ENTER)



def extract_rows(driver):
    tbody = driver.find_element(By.ID, "sppg-body")
    rows = tbody.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 5:
            print("Baris tidak valid:", [c.text for c in cols])
            continue
        
        no         = cols[0].text.strip()
        provinsi   = cols[1].text.strip()
        kota       = cols[2].text.strip()
        kecamatan  = cols[3].text.strip()
        kelurahan  = cols[4].text.strip()
        nama_sppg  = cols[5].text.strip()

        yield (no,provinsi, kota, kecamatan, kelurahan, nama_sppg)

        print("data sudah di scrap")

