import requests 
from bs4 import BeautifulSoup
import csv
import time

def get_books(page_number):
    url = f"http://books.toscrape.com/catalogue/page-{page_number}.html"
    response = requests.get(url)
    books_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        kitaplar = soup.find_all("article", class_="product_pod")

        for kitap in kitaplar:
            baslik = kitap.h3.a["title"]
            fiyat = kitap.find("p", class_="price_color").text
            temiz_fiyat = fiyat.replace("Â£", "").replace("£", "")

            books_data.append([baslik,temiz_fiyat])

    else:
        print(f"Sayfa {page_number} bulunamadı!")

    return books_data

def save_to_cs(all_books):
    with open("books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Kitap Adı", "Fiyat(£)"])
        writer.writerows(all_books)
    print(f"Toplam {len(all_books)} kitap 'books.csv' dosyasına yazıldı.")

if __name__ == "__main__":
    tum_kitaplar = []
    for page_number in range (1,6):
        print(f"Sayfa {page_number} taranıyor... ")
        tum_kitaplar.extend(get_books(page_number))
        time.sleep(1)
    save_to_cs(tum_kitaplar)
