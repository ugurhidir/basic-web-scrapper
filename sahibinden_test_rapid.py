from DrissionPage import ChromiumPage, ChromiumOptions
from bs4 import BeautifulSoup # Hızın kaynağı
import os
import time

def main():
    # --- AYARLAR ---
    current_dir = os.getcwd()
    profile_path = os.path.join(current_dir, "BenimProfilim")
    
    co = ChromiumOptions()
    co.set_user_data_path(path=profile_path)
    
    # Resimleri kapat (Ekstra hız)
    co.set_argument('--blink-settings=imagesEnabled=false')

    page = ChromiumPage(co)
    print("🌍 Tarayıcı açılıyor...")

    url = "https://www.sahibinden.com/satilik-daire/istanbul"
    page.get(url)

    print("⏳ Sayfa yükleniyor...")

    # Tabloyu bekle
    if page.wait.ele_displayed("#searchResultsTable", timeout=30):
        print("✅ KORUMA AŞILDI! HTML alınıyor...")
        
        # --- KRİTİK HAMLE: HTML'i AL VE TARAYICIYI UNUT ---
        # Artık sayfayla işimiz bitti, HTML'i kopyalayıp Python'a alıyoruz.
        html_content = page.html 
        
        print("⚡ BeautifulSoup devreye giriyor (Rapid Mode)...")
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Sadece data-id'si olan satırları bul (Reklamları atla)
        satirlar = soup.find_all("tr", attrs={"data-id": True})
        
        print(f"📊 Toplam {len(satirlar)} ilan bulundu. İşleniyor...\n")

        start_time = time.time()

        for i, satir in enumerate(satirlar, 1):
            try:
                # --- BAŞLIK ---
                # BeautifulSoup ile arama yapmak milisaniyeler sürer, bekleme yapmaz.
                baslik_tag = satir.find("a", class_="classifiedTitle")
                
                if baslik_tag:
                    baslik = baslik_tag.text.strip()
                else:
                    # Yedek plan (Title Value)
                    yedek_tag = satir.find("td", class_="searchResultsTitleValue")
                    baslik = " ".join(yedek_tag.text.split()) if yedek_tag else "Başlık Yok"

                # --- FİYAT ---
                fiyat_tag = satir.find("td", class_="searchResultsPriceValue")
                fiyat = fiyat_tag.text.strip() if fiyat_tag else "Fiyat Yok"

                # --- İLAN NO ---
                ilan_no = satir["data-id"]

                # Ekrana Bas (Uzun başlığı kısalt)
                print(f"✅ {i}. 🆔 {ilan_no} | 🏠 {baslik[:40]:<40} | 💰 {fiyat}")

            except Exception as e:
                print(f"⚠️ Hata: {e}")
                continue
        
        end_time = time.time()
        print(f"\n🚀 İŞLEM TAMAM! {len(satirlar)} satır sadece {end_time - start_time:.4f} saniyede işlendi.")

    else:
        print("❌ Tablo yüklenmedi.")

    # İstersen kapat, istersen açık kalsın
    # page.quit()

if __name__ == "__main__":
    main()