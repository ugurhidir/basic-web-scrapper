from playwright.sync_api import sync_playwright
import time
import csv

def save_to_csv(all_quotes):
    """Verileri CSV'ye kaydeder"""
    with open("quotes_js.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Alıntı", "Yazar"])
        writer.writerows(all_quotes)
    print(f"\n✅ Toplam {len(all_quotes)} alıntı 'quotes_js.csv' dosyasına kaydedildi.")

def main():
    tum_veriler = [] # Tüm sayfaların verisi burada birikecek

    with sync_playwright() as p:
        print("🌍 Tarayıcı başlatılıyor (Headless)...")
        # Tarayıcıyı DÖNGÜNÜN DIŞINDA bir kez açıyoruz
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1'den 10'a kadar sayfaları gez
        for page_number in range(1, 11):
            # Doğru URL yapısı: /js/page/X/
            url = f"http://quotes.toscrape.com/js/page/{page_number}/"
            print(f"🚀 Gidiliyor: {url}")
            
            try:
                page.goto(url)
                
                # Verinin (JavaScript'in) yüklenmesini bekle
                page.wait_for_selector(".quote", timeout=3000)

                # Elemanları bul
                quotes = page.query_selector_all(".quote")
                print(f"   ✅ Sayfa {page_number}: {len(quotes)} veri bulundu.")

                # Verileri Ayıkla (Extract)
                for q in quotes:
                    text = q.query_selector(".text").inner_text()
                    author = q.query_selector(".author").inner_text()
                    tum_veriler.append([text, author]) # Ana listeye ekle

            except Exception as e:
                print(f"   ❌ Sayfa {page_number} yüklenirken hata veya veri yok: {e}")
                break # Hata varsa döngüden çık

        print("\n🏁 Tarama bitti, tarayıcı kapatılıyor.")
        browser.close()
    
    # Döngü bitince ve tarayıcı kapanınca kaydet
    return tum_veriler

if __name__ == "__main__":
    # Verileri çek
    veriler = main()
    
    # Kaydet
    if veriler:
        save_to_csv(veriler)
    else:
        print("Hiç veri çekilemedi.")