import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scroll_table(driver, timeout=10):
    container = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.relative.overflow-scroll")
        )
    )

    driver.execute_script(
        "arguments[0].scrollTop = arguments[0].scrollHeight",
        container
    )
    time.sleep(2)
    return container


def get_max_page(driver, timeout=10):
    buttons = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            "a.px-2.w-max.max-w-16.text-center.py-1.rounded.text-base.font-semibold.bg-transparent.text-darkBlue.border.border-gray-200"
        ))
    )

    return max(int(b.text.strip()) for b in buttons if b.text.strip().isdigit())

def click_next(driver, timeout=10):
    try:
        # 1. TEMUKAN HALAMAN AKTIF
       
        active_page_element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 
                "a.bg-darkBlue.text-white" 
            ))
        )
        
        
        current_page_text = active_page_element.get_attribute("innerText").strip()
        if not current_page_text.isdigit():
            print("Gagal membaca nomor halaman aktif.")
            return None
            
        current_page = int(current_page_text)
        target_page = current_page + 1
        print(f"Halaman saat ini: {current_page}. Mencari halaman: {target_page}...")

        # 2. CARI TOMBOL HALAMAN BERIKUTNYA SECARA SPESIFIK
        
        next_button_xpath = f"//div[contains(@class, 'flex')]//a[normalize-space()='{target_page}']"
        
        try:
            next_button = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, next_button_xpath))
            )
        except:
            print(f"Tombol untuk halaman {target_page} tidak ditemukan (Mungkin halaman terakhir).")
            return None

        # 3. KLIK TOMBOL
       
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", next_button)
        time.sleep(0.5) # Beri jeda sedikit setelah scroll
        
        # Klik via JS 
        driver.execute_script("arguments[0].click();", next_button)
        
        # Tunggu sebentar untuk memastikan loading dimulai sebelum fungsi return
        time.sleep(2) 
        
        print(f"Berhasil klik halaman {target_page}")
        return target_page

    except Exception as e:
        print(f"Error saat klik next page: {e}")
        return None