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