import requests # HTTP istekleri için
from bs4 import BeautifulSoup # HTML ayrıştırıcı

url = "https://alican-kaya.com/" 
response = requests.get(url)

if response.status_code == 200:
    print("Siteden Veri Çekilebilir")
else:
    print(f"Siteden Veri Çekilemez. Hata Kodu: {response.status_code}")

soup = BeautifulSoup(response.content, "html.parser")

print(soup.title) # Sayfanın <title> etiketi
print(soup.prettify()) # HTML'i okunaklı, girintili formatta yazdırır

yazdir = soup.html
print("-" * 80)

# Tüm alt elemanların metnini yazdırır
for i in yazdir:
    print(i.text)

# Sınıfı "h-28" olan div'i ve href'ini bulur
try:
    div_cek = soup.find("div", {"class": "h-28"})
    print(div_cek.text)
    print(div_cek.get("href"))
except AttributeError:
    print("Sınıfı 'h-28' olan bir <div> elementi bulunamadı.")

# Belirli bir class'a sahip li etiketini bulur
try:
    li_cek = soup.find("li", {"class": "flex items-start gap-2 text-sm text-white/90"}).text
    print(li_cek)
except AttributeError:
    print("Belirtilen sınıfa ait bir <li> elementi bulunamadı.")
