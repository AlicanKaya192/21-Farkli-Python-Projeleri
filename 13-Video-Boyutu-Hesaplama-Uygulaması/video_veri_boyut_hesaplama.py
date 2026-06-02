"""
Video Veri Boyutu Hesaplama Uygulaması
======================================
Bu uygulama, kullanıcının seçtiği video çözünürlüğüne (360p, 480p, 720p, 1080p)
ve girdiğü video süresine (dakika) göre tahmini video dosya boyutunu (MB) hesaplar.

Hesaplama Formülü:
    Dosya Boyutu (MB) = (Bit Hızı (kbps) * Süre (saniye)) / 8 / 1024

Kullanılan Kütüphaneler:
    - tkinter : Temel GUI (Grafiksel Kullanıcı Arayüzü) bileşenleri için.
    - ttk     : Modern görünümlü stilize bileşenler (Combobox, Button vb.) için.
"""

import tkinter as tk
from tkinter import ttk, messagebox


def hesapla():
    """
    Seçilen çözünürlüğe ve girilen süreye göre video dosya boyutunu hesaplar.
    Sonucu result_label etiketi üzerinde gösterir.
    """
    try:
        # Arayüzden çözünürlük ve süre bilgilerini al
        resolution = resolution_var.get()
        duration = int(duration_var.get())

        if duration <= 0:
            raise ValueError("Süre sıfır veya negatif olamaz.")

        # Bit hızlarını çözünürlüklerine göre ayarla (kbps cinsinden)
        # Standart YouTube/Video platformu bit hızları baz alınmıştır.
        bit_rates = {
            "360p": 750,    # 750 kbps
            "480p": 1500,   # 1.5 Mbps
            "720p": 3000,   # 3.0 Mbps
            "1080p": 4500   # 4.5 Mbps
        }
        bit_rate = bit_rates[resolution]

        # Dosya boyutu hesaplama (MB cinsinden)
        # Formül: (Bit Hızı (kbps) * Süre (dakika) * 60 saniye) / 8 (byte'a çeviri) / 1024 (MB'a çeviri)
        file_size_mb = bit_rate * duration * 60 / 8 / 1024
        
        # Sonucu etikete yazdır (.2f ile virgülden sonra iki basamak gösterilir)
        result_label.config(text=f"Video Boyutu : {file_size_mb:.2f} MB")

    except ValueError:
        # Geçersiz karakter girilmesi veya boş bırakılması durumunda hata mesajı göster
        messagebox.showerror("Hata", "Lütfen geçerli bir süre (pozitif tamsayı) giriniz.")
    except Exception as e:
        # Beklenmeyen diğer hataları yakala
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")


# =============================================================================
# ARAYÜZ TASARIMI VE YAPILANDIRMASI
# =============================================================================

# Ana pencereyi oluştur
root = tk.Tk()
root.title("Video Veri Boyutu Hesaplama")
root.geometry("450x450")
root.resizable(False, False)  # Pencere boyutunun değiştirilmesini engelle

# Stil Ayarları
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 16))
style.configure("TButton", font=("Helvetica", 16))
style.configure("TCombobox", font=("Helvetica", 16))

# Buton Aktif/Pasif Renk Stili Ayarları
style.map("TButton", 
          foreground=[("active", "black"), ("!disabled", "black")],
          background=[("active", "#45a049"), ("!disabled", "#45a049")])

# 1. Çözünürlük Seçim Alanı
resolution_label = ttk.Label(root, text="Çözünürlük: ")
resolution_label.pack(pady=10)

resolution_var = tk.StringVar()
resolution_combobox = ttk.Combobox(root, textvariable=resolution_var, state="readonly")
resolution_combobox['values'] = ("360p", "480p", "720p", "1080p")
resolution_combobox.current(0)  # Varsayılan olarak 360p seçilsin
resolution_combobox.pack(pady=10)

# 2. Süre Giriş Alanı (Dakika cinsinden)
duration_label = ttk.Label(root, text="Video Süresi (Dakika): ")
duration_label.pack(pady=10)

duration_var = tk.StringVar()
duration_entry = ttk.Entry(root, textvariable=duration_var)
duration_entry.pack(pady=10)

# 3. Hesaplama Butonu
calculate_button = ttk.Button(root, text="Hesapla", command=hesapla)
calculate_button.pack(pady=20)

# 4. Sonuç Gösterim Etiketi
result_label = ttk.Label(root, text="Video Boyutu")
result_label.pack(pady=20)

# Uygulama döngüsünü başlat
root.mainloop()