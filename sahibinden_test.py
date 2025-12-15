from DrissionPage import ChromiumPage, ChromiumOptions
import os
import time

def main():
    current_dir = os.getcwd()
    profile_path = os.path.join(current_dir, "BenimProfilim")
    
    co = ChromiumOptions()
    co.set_user_data_path(path=profile_path)

    page = ChromiumPage(co)
    print("🌍 Tarayıcı (Profil Modunda) açılıyor...")

    url = "https://www.sahibinden.com/satilik-daire/istanbul"
    page.get(url)

    print("⏳ İlan tablosu bekleniyor...")

    if page.wait.ele_displayed("#searchResultsTable", timeout=30):
        print("✅ KORUMA AŞILDI! Veriler işleniyor...\n")
        
        # Sadece data-id'si olan satırları al (Gerçek ilanlar)
        ilan_satirlari = page.eles("css:tr[data-id]")
        
        print(f"📊 Toplam {len(ilan_satirlari)} adet ilan satırı bulundu.\n")

        for i, satir in enumerate(ilan_satirlari, 1):
            try:
                # --- BAŞLIK ALMA (3 Aşamalı Güvenlik) ---
                baslik = "Başlık Bulunamadı"
                
                # Yöntem 1: Standart Class (.classifiedTitle)
                t1 = satir.ele(".classifiedTitle")
                
                # Yöntem 2: Kapsayıcı Hücre (.searchResultsTitleValue) - DAHA GARANTİ
                t2 = satir.ele(".searchResultsTitleValue")
                
                # Yöntem 3: Satırın içindeki ilk Link (a etiketi)
                t3 = satir.ele("tag:a")

                if t1:
                    baslik = t1.text.strip()
                elif t2:
                    # Hücrenin içindeki metni al (fazla boşlukları temizle)
                    baslik = " ".join(t2.text.split()) 
                elif t3:
                    baslik = t3.text.strip()

                # --- FİYAT ALMA ---
                fiyat_ele = satir.ele(".searchResultsPriceValue")
                fiyat = fiyat_ele.text.strip() if fiyat_ele else "Fiyat Yok"

                # --- İLAN NO ---
                ilan_no = satir.attr("data-id")

                # Başlık çok uzunsa keselim, terminal kirlenmesin
                kisa_baslik = (baslik[:40] + '..') if len(baslik) > 40 else baslik

                print(f"✅ {i}. İlan: 🆔 {ilan_no} | 🏠 {kisa_baslik} | 💰 {fiyat}")

            except Exception as e:
                print(f"⚠️ Satır {i} işlenirken hata: {e}")
                continue

    else:
        print("❌ Tablo yüklenmedi.")

    print("\n🏁 İşlem tamamlandı. Tarayıcı kapatılıyor.")
    page.quit()

if __name__ == "__main__":
    main()