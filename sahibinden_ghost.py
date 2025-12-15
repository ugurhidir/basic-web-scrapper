from DrissionPage import ChromiumPage, ChromiumOptions
from bs4 import BeautifulSoup
import os
import time

def main():
    # Sayfa değişkenini başta boş tanımlayalım ki hata olursa çökmesin
    page = None

    try:
        current_dir = os.getcwd()
        profile_path = os.path.join(current_dir, "BenimProfilim")
        
        co = ChromiumOptions()
        co.set_user_data_path(path=profile_path)
        
        # ❌ HEADLESS İPTAL (Çünkü Handshake hatası veriyor)
        # co.headless(True) 
        
        # ✅ NINJA MODU AKTİF (Ekranın dışına atıyoruz)
        # Bu yöntem Headless'tan daha kararlıdır.
        co.set_argument('--window-position=-10000,-10000')
        co.set_argument('--blink-settings=imagesEnabled=false') # Resim yok (Hız için)
        co.set_argument('--mute-audio')

        # Tarayıcıyı başlat
        print("🥷 Ninja Tarayıcı (Ekran Dışı) hazırlanıyor...")
        page = ChromiumPage(co)

        start_global = time.time()
        
        url = "https://www.sahibinden.com/satilik-daire/istanbul"
        print(f"🚀 {url} adresine sessizce gidiliyor...")
        page.get(url)

        # Tabloyu bekle
        if page.wait.ele_displayed("#searchResultsTable", timeout=30):
            print("✅ BAĞLANTI BAŞARILI! Veri çekiliyor...")
            
            # HTML'i Çek
            html_content = page.html
            
            # BeautifulSoup ile Parçala
            soup = BeautifulSoup(html_content, "html.parser")
            satirlar = soup.find_all("tr", attrs={"data-id": True})
            
            print(f"📊 Toplam {len(satirlar)} ilan bulundu.\n")

            for i, satir in enumerate(satirlar, 1):
                try:
                    baslik_tag = satir.find("a", class_="classifiedTitle")
                    if baslik_tag:
                        baslik = baslik_tag.text.strip()
                    else:
                        yedek_tag = satir.find("td", class_="searchResultsTitleValue")
                        baslik = " ".join(yedek_tag.text.split()) if yedek_tag else "Başlık Yok"

                    fiyat_tag = satir.find("td", class_="searchResultsPriceValue")
                    fiyat = fiyat_tag.text.strip() if fiyat_tag else "Fiyat Yok"

                    ilan_no = satir["data-id"]

                    print(f"✅ {i}. 🆔 {ilan_no} | 🏠 {baslik[:40]:<40} | 💰 {fiyat}")

                except:
                    continue
            
            end_global = time.time()
            print(f"\n⚡ OPERASYON TAMAMLANDI! Süre: {end_global - start_global:.2f} saniye")

        else:
            print("❌ Hata: Tablo yüklenmedi.")
            page.get_screenshot(path='ninja_fail.png')

    except Exception as e:
        print(f"💥 Kritik Hata: {e}")
        
    finally:
        if page:
            print("\nTarayıcı kapatılıyor.")
            try:
                page.quit()
            except:
                pass

if __name__ == "__main__":
    main()