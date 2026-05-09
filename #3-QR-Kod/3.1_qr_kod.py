# =============================================================================
# PROJE: QR KOD OLUŞTURUCU (Masaüstü Uygulaması)
# =============================================================================
# Bu proje, kullanıcıdan bir URL veya metin alarak bu veriyi içeren bir
# QR kod (Karekod) oluşturur ve bunu bilgisayara SVG formatında kaydeder.
# Arayüz için "tkinter", QR kod oluşturma işlemleri için ise "pyqrcode" kullanılır.
# =============================================================================

import tkinter as tk # Arayüz (GUI - Graphical User Interface) oluşturmak için standart Python kütüphanesi.
from tkinter import filedialog # Kullanıcının dosyayı nereye kaydedeceğini seçmesini sağlayan pencereyi açmak için.
import pyqrcode # type: ignore # Girilen metin/URL'den QR kod üretmek için kullanılan kütüphane.
from pyqrcode import QRCode # type: ignore # pyqrcode kütüphanesinden QRCode sınıfını doğrudan erişilebilir yapmak için (opsiyonel ama kod okunaklılığını artırır).

# =============================================================================
# TEMEL FONKSİYONLAR
# =============================================================================

# Kullanıcı butona tıkladığında çalışacak olan QR kod oluşturma ve kaydetme fonksiyonu.
def qr_kodu_olustur():
    # url_girdi adlı Entry (Girdi alanı) widget'ının içindeki metni alır.
    url = url_girdi.get()

    # Eğer kullanıcı girdi alanına bir şey yazmışsa (boş değilse) işlemlere başla:
    if url:
        # pyqrcode.create() fonksiyonu, girilen metni/URL'yi alır ve bellekte bir QR kod nesnesi oluşturur.
        qr_url = pyqrcode.create(url)
        
        # filedialog.asksaveasfilename(): Kullanıcıya standart bir "Farklı Kaydet" penceresi açar.
        # defaultextension=".svg": Kullanıcı uzantı yazmazsa varsayılan olarak .svg ekler.
        # filetypes: Penceredeki "Kayıt türü" açılır menüsünde görünecek filtreler.
        # NOT: asksaveasfile() yerine asksaveasfilename() kullandık çünkü pyqrcode dosyayı
        # kendisi "bytes" formatında yazmak istiyor. Sadece dosya yolunu (string) vermemiz yeterli.
        dosya_yolu = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG dosyaları", "*.svg")])

        # Eğer kullanıcı pencereyi "İptal" diyerek kapatmamışsa ve bir dosya yolu seçmişse:
        if dosya_yolu:
            # Oluşturduğumuz qr_url nesnesini, kullanıcının seçtiği dosya yoluna SVG formatında kaydeder.
            # scale=8: QR kodun boyutunu (çözünürlüğünü/büyüklüğünü) belirler. Değer büyüdükçe kod fiziksel olarak büyür.
            qr_url.svg(dosya_yolu, scale=8)
            
            # İşlem başarılı olduktan sonra arayüzdeki durum etiketinin metnini günceller ve kullanıcıya bilgi verir.
            durum_etiketi.config(text="QR Kodu Oluşturuldu ve Kaydedildi.")


# =============================================================================
# ARAYÜZ (TASARIM) KISMI
# =============================================================================

# tk.Tk(): Ana uygulama penceresini oluşturur. Bu uygulamanın temel taşıdır.
uygulama_pencere = tk.Tk()

# Pencerenin başlık çubuğunda görünecek ismi belirler.
uygulama_pencere.title("QR Kodu Oluşturucusu")

# tk.Label(): Pencere üzerinde sadece metin göstermek için kullanılan bir etikettir.
etiket = tk.Label(uygulama_pencere, text="URL'yi Girin: ")

# tk.Entry(): Kullanıcının klavyeden veri girebileceği tek satırlık bir metin kutusudur. width=40 ile genişliğini ayarladık.
url_girdi = tk.Entry(uygulama_pencere, width=40)

# tk.Button(): Tıklanabilir bir buton oluşturur. 
# command=qr_kodu_olustur: Butona tıklandığında yukarıda tanımladığımız fonksiyonun çalışmasını sağlar. (Yanında () parantez yok!)
qr_kodu_butonu = tk.Button(uygulama_pencere, text="QR Kodu Oluştur", command=qr_kodu_olustur)

# İşlem sonucunu (başarılı olup olmadığını) göstereceğimiz etiket. Başlangıçta boş ("", text="").
durum_etiketi = tk.Label(uygulama_pencere, text="")

# .grid() Metodu: Bileşenleri (widget'ları) pencereye bir tablo gibi (satır/sütun) yerleştirmemizi sağlar.
# padx ve pady: Bileşenin dış kenarlarından bırakılacak boşluk (padding) miktarıdır (Nefes almasını sağlar).
etiket.grid(row=0, column=0, padx=10, pady=10)                 # 1. Satır, 1. Sütun
url_girdi.grid(row=0, column=1, padx=10, pady=10)              # 1. Satır, 2. Sütun (Girdi alanı etiketin yanında)
qr_kodu_butonu.grid(row=1, column=0, columnspan=2, padx=10, pady=10) # 2. Satır. columnspan=2 ile butonun iki sütunluk yeri kaplamasını ve ortalanmasını sağladık.
durum_etiketi.grid(row=2, column=0, columnspan=2, padx=10, pady=10)  # 3. Satır. Bu da bilgilendirme yazısı, 2 sütunu kaplar.

# Uygulamanın çalışmasını sağlayan ana döngüdür.
# Bu kod pencerenin sürekli açık kalmasını ve kullanıcı etkileşimlerini (tıklama, yazma vb.) dinlemesini sağlar.
# Program kapatılana kadar bu satırda bekler.
uygulama_pencere.mainloop()