import requests # HTTP istekleri için
from bs4 import BeautifulSoup # HTML ayrıştırıcı

url = "https://covid19.saglik.gov.tr/" 
response = requests.get(url) 

if response.status_code == 200:
    print("Siteden Veri Çekilebilir")
else:
    print(f"Siteden Veri Çekilemez. Hata Kodu: {response.status_code}")

soup = BeautifulSoup(response.content, "html.parser")

try:
    # Sayfadaki tablo gövdesindeki satırları (tr) bul
    for i in soup.find("tbody").find_all("tr"):
        print("----------")
        print(i.text) # Satırın metnini yazdır
except AttributeError:
    # tbody bulunamazsa çökmemesi için
    print("Sitede 'tbody' etiketi bulunamadı! Sayfa yapısı değişmiş veya veriler JavaScript ile yükleniyor olabilir.")