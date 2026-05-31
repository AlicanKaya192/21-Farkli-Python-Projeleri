import os
import tkinter as tk
from tkinter import ttk
import sqlite3


class StokTakipUygulamasi:
    """
    SQLite veritabanı destekli, kullanıcı dostu bir grafik arayüze (GUI) sahip
    Stok Takip Uygulaması sınıfı. Ürün ekleme, silme, güncelleme, arama ve temizleme
    işlemlerini içerir.
    """
    def __init__(self, root):
        # Ana pencere nesnesini sınıf değişkeni olarak kaydet
        self.root = root
        self.root.title("Stok Takip Uygulaması")
        self.root.resizable(False, False) # Pencerenin boyutlandırılmasını engelle

        # Veri tabanı dosyası için bu kod dosyasının bulunduğu dizini baz al
        db_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(db_dir, "stok_takip.db")
        
        # SQLite veritabanı bağlantısını kur ve imleci oluştur
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
        # Stok tablosunu oluştur (Eğer daha önce oluşturulmadıysa)
        # id (Birincil Anahtar), urun_adi, adet, birim_fiyat ve toplam_deger alanları tanımlanmıştır.
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

        # --- Arayüz Giriş (Entry) Alanları ve Etiketleri (Label) ---
        
        # Ürün ID Girişi
        self.id_label = tk.Label(root, text="Ürün ID: ")
        self.id_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.id_entry = tk.Entry(root)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Ürün Adı Girişi
        self.urun_adi_label = tk.Label(root, text="Ürün Adı: ")
        self.urun_adi_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.urun_adi_entry = tk.Entry(root)
        self.urun_adi_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Ürün Adeti Girişi
        self.adet_label = tk.Label(root, text="Adet: ")
        self.adet_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.adet_entry = tk.Entry(root)
        self.adet_entry.grid(row=2, column=1, padx=5, pady=5)

        # Ürün Birim Fiyatı Girişi
        self.birim_fiyati_label = tk.Label(root, text="Birim Fiyatı: ")
        self.birim_fiyati_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.birim_fiyati_entry = tk.Entry(root)
        self.birim_fiyati_entry.grid(row=3, column=1, padx=5, pady=5)

        # --- İşlem Butonları (Ekle, Düzelt, Sil, Temizle) ---
        
        # Yeni Ürün Ekleme Butonu
        self.ekle_buton = tk.Button(root, text="Ekle", command=self.ekle, width=10)
        self.ekle_buton.grid(row=4, column=0, padx=5, pady=10)
        
        # Seçili Ürünü Düzeltme / Güncelleme Butonu
        self.duzelt_buton = tk.Button(root, text="Düzelt", command=self.duzelt, width=10)
        self.duzelt_buton.grid(row=4, column=1, padx=5, pady=10)

        # Seçili Ürünü Silme Butonu
        self.sil_buton = tk.Button(root, text="Sil", command=self.sil, width=10)
        self.sil_buton.grid(row=4, column=2, padx=5, pady=10)
        
        # Giriş Kutularını Temizleme Butonu
        self.temizle_buton = tk.Button(root, text="Temizle", command=self.girisleri_temizle, width=10)
        self.temizle_buton.grid(row=4, column=3, padx=5, pady=10)

        # --- Arama Çubuğu ---
        self.arama_label = tk.Label(root, text="Ara: ")
        self.arama_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.arama_entry = tk.Entry(root)
        self.arama_entry.grid(row=5, column=1, padx=5, pady=5, columnspan=2, sticky="ew")

        # Klavyeden tuş bırakıldığında arama fonksiyonunu tetikle
        self.arama_entry.bind("<KeyRelease>", self.arama)

        # --- Verileri Göstereceğimiz Tablo (Treeview) ---
        self.tablo = ttk.Treeview(root, columns=("ID", "Ürün Adı", "Adet", "Birim Fiyatı", "Toplam Değer"), show="headings")
        self.tablo.heading("ID", text="ID")
        self.tablo.heading("Ürün Adı", text="Ürün Adı")
        self.tablo.heading("Adet", text="Adet")
        self.tablo.heading("Birim Fiyatı", text="Birim Fiyatı")
        self.tablo.heading("Toplam Değer", text="Toplam Değer")
        
        # Sütun genişliklerini ayarla
        self.tablo.column("ID", width=80, anchor="center")
        self.tablo.column("Ürün Adı", width=150, anchor="w")
        self.tablo.column("Adet", width=80, anchor="center")
        self.tablo.column("Birim Fiyatı", width=100, anchor="e")
        self.tablo.column("Toplam Değer", width=120, anchor="e")
        self.tablo.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

        # Tablodan bir satıra tıklandığında bilgileri giriş alanlarına çekmek için olay bağlama
        # pyrefly: ignore [missing-attribute]
        self.tablo.bind("<ButtonRelease-1>", self.satir_sec)

        # Uygulama açılışında veritabanındaki kayıtları tabloya yükle
        # pyrefly: ignore [missing-attribute]
        self.verileri_yukle()
    
    def ekle(self):
        """Giriş alanlarındaki verileri okuyup veritabanına ve tabloya yeni kayıt olarak ekler."""
        try:
            id = self.id_entry.get()
            urun_adi = self.urun_adi_entry.get()
            adet = int(self.adet_entry.get())
            birim_fiyat = float(self.birim_fiyati_entry.get())
            toplam_deger = adet * birim_fiyat

            # Veritabanına kaydet
            self.cursor.execute("INSERT INTO stok VALUES(?,?,?,?,?)", (id, urun_adi, adet, birim_fiyat, toplam_deger))
            self.conn.commit()

            # Tabloya (Treeview) ekle
            self.tablo.insert("", "end", values=(id, urun_adi, adet, birim_fiyat, toplam_deger))
            # Ekleme sonrası giriş alanlarını temizle
            self.girisleri_temizle()
        except ValueError:
            # Hatalı veri girişi yapıldığında (örneğin adet veya fiyat alanına harf girilirse)
            pass

    def girisleri_temizle(self):
        """Arayüzdeki tüm veri giriş kutularının içeriğini temizler."""
        self.id_entry.delete(0, tk.END)
        self.urun_adi_entry.delete(0, tk.END)
        self.adet_entry.delete(0, tk.END)
        self.birim_fiyati_entry.delete(0, tk.END)

    def arama(self, event):
        """Kullanıcının arama kutusuna yazdığı metne göre eşleşen kayıtları tabloda seçer."""
        arama_metni = self.arama_entry.get().lower()

        # Tablodaki tüm satırları tara
        for item in self.tablo.get_children():
            values = self.tablo.item(item, "values")

            # Arama metni ID, Ürün Adı, Adet veya Fiyat alanlarından herhangi birinde geçiyorsa satırı seç
            # pyrefly: ignore [bad-index]
            if arama_metni in values[0].lower() or arama_metni in values[1].lower() or arama_metni in values[2].lower() or arama_metni in values[3].lower():
                self.tablo.selection_set(item)
                self.tablo.see(item) # Satırın görünür olmasını sağla
            else:
                self.tablo.selection_remove(item)

    def satir_sec(self, event):
        """Tablodan seçilen satırdaki verileri düzenleme amacıyla giriş kutularına yazar."""
        secili = self.tablo.selection()

        if secili:
            # pyrefly: ignore [no-matching-overload]
            item = self.tablo.item(secili)
            values = item["values"]

            # Alanları temizle ve seçili satırın değerlerini doldur
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, values[0])

            self.urun_adi_entry.delete(0, tk.END)
            self.urun_adi_entry.insert(0, values[1])

            self.adet_entry.delete(0, tk.END)
            self.adet_entry.insert(0, values[2])

            self.birim_fiyati_entry.delete(0, tk.END)
            self.birim_fiyati_entry.insert(0, values[3])

    def duzelt(self):
        """Seçili ürünün güncellenmiş değerlerini veritabanı ve tabloda günceller."""
        secili = self.tablo.selection()

        if secili:
            try:
                id = self.id_entry.get()
                urun_adi = self.urun_adi_entry.get()
                adet = int(self.adet_entry.get())
                birim_fiyat = float(self.birim_fiyati_entry.get())
                toplam_deger = adet * birim_fiyat

                # Veritabanında güncelle
                self.cursor.execute("UPDATE stok SET urun_adi = ?, adet = ?, birim_fiyat = ?, toplam_deger = ? WHERE id = ?", (urun_adi, adet, birim_fiyat, toplam_deger, id))
                self.conn.commit()

                # Tablodaki (Treeview) görünümü güncelle
                # pyrefly: ignore [no-matching-overload]
                self.tablo.item(secili, values=(id, urun_adi, adet, birim_fiyat, toplam_deger))
                # Alanları temizle
                self.girisleri_temizle()
            except ValueError:
                pass

    def sil(self):
        """Seçili ürünü veritabanından ve tablodan siler."""
        secili = self.tablo.selection()

        if secili:
            # pyrefly: ignore [no-matching-overload]
            id = self.tablo.item(secili)['values'][0]
            
            # Veritabanından sil
            self.cursor.execute("DELETE FROM stok WHERE id = ?", (id,))
            self.conn.commit()

            # Tablodan sil
            # pyrefly: ignore [bad-argument-type, no-matching-overload]
            self.tablo.delete(secili)
            
            # Giriş alanlarını temizle
            self.girisleri_temizle()

    def verileri_yukle(self):
        """Veritabanındaki tüm stok kayıtlarını okuyarak tabloya yükler."""
        for row in self.cursor.execute("SELECT * FROM stok"):
            self.tablo.insert("", "end", values=row)


if __name__ == "__main__":
    # Tkinter ana döngüsünü başlat
    root = tk.Tk()
    app = StokTakipUygulamasi(root)
    root.mainloop()