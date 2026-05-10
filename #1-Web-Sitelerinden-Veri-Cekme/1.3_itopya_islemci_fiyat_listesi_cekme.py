import requests # HTTP istekleri için
from bs4 import BeautifulSoup # HTML parser

url = requests.get("https://www.itopya.com/islemci_k8")

# Bağlantı durumu kontrolü (200: Başarılı)
if url.status_code == 200:
    print("Siteden Veri Çekilebilir")
else:
    print("Siteden Veri Çekilemez")

# HTML içeriğini ayrıştır
soup = BeautifulSoup(url.content, "html.parser")

# Tüm ürün kartlarını kapsayan ana div'i bul
urun_listesi_div = soup.find("div", {"class": "product_product_List"})
if urun_listesi_div:
    # Her bir ürün kartı üzerinde döngü
    for i in urun_listesi_div.find_all("div", {"class": "product-block"}):

        # Ürün başlığını çek
        # pyrefly: ignore [optional-member-access]
        baslik_al = i.find("div", {"class": "product-block-top"}).h2.a.text.strip()

        # Ürün fiyatını çek
        # pyrefly: ignore [optional-member-access]
        fiyat_al = i.find("span", {"class": "product-price"}).text.strip()

        # Ürün detay linkini çek
        # pyrefly: ignore [optional-member-access]
        link = "https://www.itopya.com" + i.find("div", {"class": "product-image"}).a.get("href")

        # Sonuçları ekrana yazdır
        print(f"\nÜrün Adı: {baslik_al}\nÜrün Fiyatı: {fiyat_al}\nÜrün Linki: {link}\n")
        print("-" * 50)

input("") # Terminalin hemen kapanmaması için