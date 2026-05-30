import os
import tkinter as tk
from tkinter import ttk
import sqlite3


class StokTakipUygulamasi:
    def __init__(self, root):
        # Ana pencereyi oluştur
        self.root = root
        self.root.title("Stok Takip Uygulaması")

        # Veri Tabanını Oluştur
        # gerekli tabloları oluştur
        db_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(db_dir, "stok_takip.db")
        self.conn = sqlite3.connect(db_path)
        # 'self.cursor' ile imleci sınıf niteliği yaparak diğer fonksiyonlardan da erişilmesini sağlarız.
        # 'self' kelimesi bu sınıf nesnesinin kendisini temsil eder; self'siz değişkenler yerel kalır.
        self.cursor = self.conn.cursor()
        # REAL ONDALIK SAYI
        self.cursor.execute("""
             CREATE TABLE IF NOT EXISTS stok(
                                             id TEXT PRIMARY KEY,
                                             urun_adi TEXT,
                                             adet INTEGER,
                                             birim_fiyat REAL,
                                             toplam_deger REAL
                                             )        
        """)
        self.conn.commit()

        # Giriş Alanları
        self.id_label = tk.Label(root, text="Ürün ID: ")
        self.id_label.grid(row=0, column=0)
        self.id_entry = tk.Entry(root)
        self.id_entry.grid(row=0, column=1)
        
        # Ürün Adı Etiketi ve Giriş Kutusu
        self.urun_adi_label = tk.Label(root, text="Ürün Adı: ")
        self.urun_adi_label.grid(row=1, column=0)
        self.urun_adi_entry = tk.Entry(root)
        self.urun_adi_entry.grid(row=1, column=1)
        
        # Adet Etiketi ve Giriş Kutusu
        self.adet_label = tk.Label(root, text="Adet: ")
        self.adet_label.grid(row=2, column=0)
        self.adet_entry = tk.Entry(root)
        self.adet_entry.grid(row=2, column=1)

        # Birim Fiyatı Etiketi ve Giriş Kutusu
        self.birim_fiyati_label = tk.Label(root, text="Birim Fiyatı: ")
        self.birim_fiyati_label.grid(row=3, column=0)
        self.birim_fiyati_entry = tk.Entry(root)
        self.birim_fiyati_entry.grid(row=3, column=1)

        # İşlem Butonları
        self.ekle_buton = tk.Button(root, text="Ekle", command=self.ekle)
        self.ekle_buton.grid(row=4, column=0, columnspan=1)
        
        # Düzel
        self.duzelt_buton = tk.Button(root, text="Düzelt", command=self.duzelt)
        self.duzelt_buton.grid(row=4,column=1, columnspan=1)

        # Sil
        self.sil_buton = tk.Button(root, text="Sil", command=self.sil)
        self.sil_buton.grid(row=4, column=2, columnspan=1)
        
        # Temizle Butonu
        self.temizle_buton = tk.Button(root, text="Temizle", command=self.girisleri_temizle)
        self.temizle_buton.grid(row=4, column=3, columnspan=1)

        # Arama Çubuğu
        self.arama_label = tk.Label(root, text="Ara")
        self.arama_label.grid(row=5, column=0)
        self.arama_entry = tk.Entry(root)
        self.arama_entry.grid(row=5,column=1)

        # Arama Butonu
        self.arama_entry.bind("<KeyRelease>", self.arama)

        # Tablo Oluştur
        self.tablo = ttk.Treeview(root, columns=("ID", "Ürün Adı", "Adet", "Birim Fiyatı", "Toplam Değer"), show="headings")
        self.tablo.heading("ID", text="ID")
        self.tablo.heading("Ürün Adı", text="Ürün Adı")
        self.tablo.heading("Adet", text="Adet")
        self.tablo.heading("Birim Fiyatı", text="Birim Fiyatı")
        self.tablo.heading("Toplam Değer", text="Toplam Değer")
        self.tablo.grid(row=6, column=0, columnspan=4)

        # Tabloya tıklandığında veri işlemi başlasın
        self.tablo.bind("<ButtonRelease-1>", self.setir_sec)

        self.verileri_yukle()
        # ana metod bitişi
    

    def ekle(self):
        id = self.id_entry.get()
        urun_adi = self.urun_adi_entry.get()
        adet = int(self.adet_entry.get())
        birim_fiyat = float(self.birim_fiyati_entry.get())
        toplam_deger = adet * birim_fiyat

        self.cursor.execute("INSERT INTO stok VALUES(?,?,?,?,?)", (id, urun_adi, adet, birim_fiyat, toplam_deger))
        self.conn.commit()

        self.tablo.insert("", "end", values=(id, urun_adi, adet, birim_fiyat, toplam_deger))
        self.girisleri_temizle()

    
    def girisleri_temizle(self):
        self.id_entry.delete(0, tk.END)
        self.urun_adi_entry.delete(0, tk.END)
        self.adet_entry.delete(0, tk.END)
        self.birim_fiyati_entry.delete(0, tk.END)



if __name__ == "__main__":
    root = tk.Tk()
    app = StokTakipUygulamasi(root)
    root.mainloop()