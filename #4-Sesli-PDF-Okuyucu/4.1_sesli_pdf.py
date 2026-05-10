from tkinter import Label # Arayüz etiketi
from PyPDF2 import filters
import PyPDF2 # PDF işlemleri için
from gtts import gTTS # Google Text-to-Speech (Sese çevirme)
import os # İşletim sistemi işlemleri (dosya açma)
import subprocess # Sistem komutları çalıştırmak için
import tkinter as tk # Arayüz için
from tkinter import filedialog # Dosya seçme penceresi için

# PDF dosyasından metin çıkaran fonksiyon
def pdf_metni_cikart(pdf_yolu):
    metin = ""
    # PDF'i okuma modunda (rb) aç
    pdf_reader = PyPDF2.PdfReader(open(pdf_yolu, 'rb'))
    
    # Tüm sayfaları dolaş ve metni birleştir
    for sayfa_num in range(len(pdf_reader.pages)):
        metin += pdf_reader.pages[sayfa_num].extract_text()
    return metin

# Metni MP3 olarak kaydeden fonksiyon
def metni_sese_cevir(metin, cikti_dosyasi):
    # Metni Türkçe dilinde sese çevir
    sesli_cevirici = gTTS(text=metin, lang='tr')
    # Belirtilen dosya adıyla kaydet
    sesli_cevirici.save(cikti_dosyasi)

# Butona tıklandığında çalışan ana akış fonksiyonu
def dosya_sec():
    # PDF dosyası seçme penceresi aç
    dosya_yolu = filedialog.askopenfilename(filetypes=[("PDF Dosyaları", "*pdf")])
    
    if dosya_yolu: # Dosya seçildiyse
        # PDF'in içindeki yazıları metin olarak al
        pdf_metin = pdf_metni_cikart(dosya_yolu)
        
        # O metni 'kaydet.mp3' olarak sese çevir
        metni_sese_cevir(pdf_metin, "kaydet.mp3")
        
        # Oluşan mp3 dosyasını otomatik oynat
        os.startfile("kaydet.mp3")
        
        # Durum etiketini güncelle
        durum_etiketi.config(text="Dosya Başarılı Şekilde Oluşturuldu.")

# Tkinter Arayüzü
app = tk.Tk()
app.title("Sesli Kitap Uygulaması")
app.geometry("250x150")

# Buton oluştur ve tıklandığında 'dosya_sec' fonksiyonunu bağla
secim_butonu = tk.Button(app, text="PDF Seçiniz", command=dosya_sec, padx=20, pady=20)
secim_butonu.pack(pady=20)

# Durum mesajı için boş etiket
durum_etiketi = Label(app, text="")
durum_etiketi.pack(pady=10)

# Pencereyi açık tut
app.mainloop()