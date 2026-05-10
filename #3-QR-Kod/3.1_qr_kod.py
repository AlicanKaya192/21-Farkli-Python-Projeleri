import tkinter as tk # Arayüz için
from tkinter import filedialog # Kayıt penceresi için
import pyqrcode # QR kod oluşturmak için

def qr_kodu_olustur():
    # Kullanıcının girdiği URL'yi al
    url = url_girdi.get()
    
    if url: # URL boş değilse
        # QR Kodu bellekte oluştur
        qr_url = pyqrcode.create(url)
        
        # Nereye kaydedileceğini sor
        dosya_yolu = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG dosyaları", "*.svg")])

        if dosya_yolu: # İptal edilmediyse
            # SVG formatında kaydet (scale=8 boyut katsayısı)
            qr_url.svg(dosya_yolu, scale=8)
            # Arayüzdeki durumu güncelle
            durum_etiketi.config(text="QR Kodu Oluşturuldu ve Kaydedildi.")

# Ana pencereyi oluştur
uygulama_pencere = tk.Tk()
uygulama_pencere.title("QR Kodu Oluşturucusu")

# Arayüz elemanlarını (widget) tanımla
etiket = tk.Label(uygulama_pencere, text="URL'yi Girin: ")
url_girdi = tk.Entry(uygulama_pencere, width=40)
qr_kodu_butonu = tk.Button(uygulama_pencere, text="QR Kodu Oluştur", command=qr_kodu_olustur)
durum_etiketi = tk.Label(uygulama_pencere, text="")

# Elemanları ızgara (grid) sistemiyle yerleştir
etiket.grid(row=0, column=0, padx=10, pady=10)
url_girdi.grid(row=0, column=1, padx=10, pady=10)
qr_kodu_butonu.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
durum_etiketi.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Uygulamayı dinleme modunda açık tut
uygulama_pencere.mainloop()