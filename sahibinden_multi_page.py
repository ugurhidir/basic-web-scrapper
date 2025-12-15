from DrissionPage import ChromiumPage, ChromiumOptions
from bs4 import BeautifulSoup
import os
import time
import csv
import random

def main():
    # --- AYARLAR ---
    csv_dosya_adi = "sahibinden_tum_ilanlar.csv"
    current_dir = os.getcwd()
    profile_path = os.path.join(current_dir, "BenimProfilim")
    
    co = ChromiumOptions()
    co.set_user_data_path(path=profile_path)
    
    # Ninja Modu (Görünmez ama Headless değil)
    co.set_argument('--window-position=-10000,-10000') 
    co.set_argument('--blink-settings=imagesEnabled=false')

    # --- CSV HAZIRLIĞI ---
    # Dosyayı baştan oluştur ve başlıkları yaz
    with open(csv_dosya_adi, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["İlan No", "Başlık", "Fiyat", "Sayfa"]) # Sayfa bilgisini de ekleyelim

    print("🥷 Ninja Tarayıcı Başlatılıyor...")
    page = ChromiumPage(co)

    try:
        # 0'dan 980'e kadar, 20'şer artarak (Toplam 50 Sayfa)
        for offset in range(0, 1000, 20):
            sayfa_no = (offset // 20) + 1
            print(f"\n🔄 Sayfa {sayfa_no} Taranıyor (Offset: {offset})...")
            
            # URL Oluşturma
            if offset == 0:
                url = "https://www.sahibinden.com/satilik-daire/istanbul"
            else:
                url = f"https://www.sahibinden.com/satilik-daire/istanbul?pagingOffset={offset}"
            
            # Sayfaya Git
            page.get(url)

            # Tablo Kontrolü
            if page.wait.ele_displayed("#searchResultsTable", timeout=20):
                # HTML'i al ve işle
                soup = BeautifulSoup(page.html, "html.parser")
                satirlar = soup.find_all("tr", attrs={"data-id": True})
                
                print(f"   ✅ {len(satirlar)} ilan bulundu. Kaydediliyor...")

                # Bu sayfanın verilerini geçici listeye al
                sayfa_verileri = []
                for satir in satirlar:
                    try:
                        baslik_tag = satir.find("a", class_="classifiedTitle")
                        baslik = baslik_tag.text.strip() if baslik_tag else "Başlık Yok"

                        fiyat_tag = satir.find("td", class_="searchResultsPriceValue")
                        fiyat = fiyat_tag.text.strip() if fiyat_tag else "Fiyat Yok"

                        ilan_no = satir["data-id"]
                        
                        sayfa_verileri.append([ilan_no, baslik, fiyat, sayfa_no])
                    except:
                        continue
                
                # --- ANLIK KAYIT (APPEND MODE) ---
                # Her sayfadan sonra dosyayı açıp ekleyip kapatıyoruz.
                # Böylece kod patlasa bile çekilenler elimizde kalır.
                with open(csv_dosya_adi, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerows(sayfa_verileri)

                # İnsan Taklidi (Bekleme Süresi)
                # 50 sayfa gezeceğimiz için dikkat çekmemek lazım.
                # 3 ile 6 saniye arası rastgele bekle.
                bekleme = random.uniform(3, 6)
                print(f"   💾 Kaydedildi. {bekleme:.2f} saniye dinleniyor...")
                time.sleep(bekleme)

            else:
                print("   ❌ Sayfa yüklenemedi veya bot korumasına takıldık!")
                # Eğer korumaya takılırsak döngüyü kırmalıyız ki boşuna dönmesin
                break

    except Exception as e:
        print(f"💥 Genel Hata: {e}")
        
    finally:
        print(f"\n🏁 İşlem bitti. Veriler '{csv_dosya_adi}' dosyasına işlendi.")
        page.quit()

if __name__ == "__main__":
    main()