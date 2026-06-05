# İnternet üzerinden HTTP istekleri göndermek için kullanılan kütüphane
import requests
# HTML kodlarını ayrıştırmak (parse) ve içinden bilgi çekmek için kullanılan kütüphane
from bs4 import BeautifulSoup
# Arayüz (GUI) oluşturmak için kullanılan Python dahili kütüphanesi
import tkinter as tk
# Kullanıcıya bilgi veya hata mesajı (pop-up) göstermek için
from tkinter import messagebox
# Arayüz elemanlarına daha modern bir stil katmak ve ek bileşenleri (Treeview, Combobox) kullanmak için
from tkinter import ttk

# Hedef çekilecek adres: Hürriyet Bigpara döviz sayfası
# https://bigpara.hurriyet.com.tr/doviz/

# 1. Aşama: Web Scraping ile Siteden Güncel Veri Çeken Fonksiyon
def fiyatlari_getir():
    url = "https://bigpara.hurriyet.com.tr/doviz/"
    # Sitenin bizi bir bot olarak algılayıp engellemesini önlemek için tarayıcı kimliği (User-Agent) tanımlıyoruz
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        # Belirtilen adrese HTTP GET isteği gönderiyoruz
        response = requests.get(url, headers=headers)
        
        # Eğer sunucu başarıyla (200 durum koduyla) yanıt verdiyse
        if response.status_code == 200:
            # Gelen HTML içeriğini BeautifulSoup ile ayrıştırıyoruz
            soup = BeautifulSoup(response.content, 'html.parser')
            fiyatlar = []
            
            # Sitede her döviz satırının içinde "symbol-info" adında bir div bulunuyor
            symbol_infos = soup.find_all("div", class_="symbol-info")
            
            # Bulunan tüm döviz div'lerini dönüyoruz
            for info in symbol_infos:
                # İlgili div'in bağlı olduğu ana tablo satırını (tr) buluyoruz
                tr = info.find_parent("tr")
                if not tr:
                    continue
                
                # Döviz Adı (Örn: Dolar, Euro, Altın vb.)
                name_el = info.find(class_="symbol-name")
                doviz_cinsi = name_el.text.strip() if name_el else ""
                
                # Anlık Fiyat (data-column="price" olan td hücresi)
                price_el = tr.find("td", {"data-column": "price"})
                fiyat = price_el.text.strip() if price_el else "0"
                
                # Günlük Değişim/Fark Oranı (data-column="change" olan td hücresi)
                change_el = tr.find("td", {"data-column": "change"})
                fark = change_el.text.strip() if change_el else "0"
                
                # Alış Fiyatı (data-column="volume" olan td hücresi)
                alis_el = tr.find("td", {"data-column": "volume"})
                alis = alis_el.text.strip() if alis_el else "0"
                
                # Satış Fiyatı (data-column="sales" olan td hücresi)
                satis_el = tr.find("td", {"data-column": "sales"})
                satis = satis_el.text.strip() if satis_el else "0"
                
                # Eğer döviz adı boş değilse verileri sözlük (dictionary) olarak listemize ekliyoruz
                if doviz_cinsi:
                    fiyatlar.append({
                        "doviz": doviz_cinsi,
                        "fiyat": fiyat,
                        "fark": fark,
                        "alis": alis,
                        "satis": satis
                    })
            return fiyatlar
        else:
            # Sunucu hata verdiyse kullanıcıya bilgi veriyoruz
            messagebox.showerror("Hata", f"Döviz Fiyatları Çekilemedi (Durum Kodu: {response.status_code})")
            return None
    except Exception as e:
        # İnternet bağlantı hatası oluşursa
        messagebox.showerror("Hata", f"Bağlantı hatası: {str(e)}")
        return None

# 2. Aşama: Döviz Çevirici Hesaplama Fonksiyonu
def hesapla():
    try:
        # Giriş kutusundan girilen miktarı alıp ondalık ayırıcıları düzelterek float sayıya çeviriyoruz
        miktar = float(entry_miktar.get().replace(",", "."))
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayısal miktar girin.")
        return
        
    # Combobox'tan seçilen döviz cinsini alıyoruz
    secilen_doviz = combobox_doviz.get()
    if not secilen_doviz:
        messagebox.showerror("Hata", "Lütfen bir döviz cinsi seçin.")
        return
        
    # Global kurlar listesinden seçilen dövize ait olan veriyi ayıklıyoruz
    hedef_veri = None
    for d in doviz_listesi:
        if d["doviz"] == secilen_doviz:
            hedef_veri = d
            break
            
    if not hedef_veri:
        messagebox.showerror("Hata", "Seçilen döviz verisi bulunamadı.")
        return
        
    try:
        # Değerlerdeki binlik (.) ve ondalık (,) ayırıcıları Python standartlarına (noktaya) çeviriyoruz
        fiyat = float(hedef_veri["fiyat"].replace(".", "").replace(",", "."))
        alis = float(hedef_veri["alis"].replace(".", "").replace(",", "."))
        satis = float(hedef_veri["satis"].replace(".", "").replace(",", "."))
    except Exception as e:
        messagebox.showerror("Hata", f"Döviz kurları sayısal değere dönüştürülemedi: {e}")
        return
        
    # Eğer alış veya satış kurları sıfır döndüyse ana fiyatı kullanıyoruz
    if alis == 0:
        alis = fiyat
    if satis == 0:
        satis = fiyat
        
    # Çeviri yönünü kontrol ediyoruz (Dövizden TL'ye mi, TL'den Dövize mi?)
    yon = var_yon.get()
    
    if yon == 1:
        # Dövizden TL'ye çeviri: Siz elinizdeki dövizi bozduruyorsunuz (Banka sizden ALIYOR)
        # Dolayısıyla "Alış" kurunu kullanıyoruz.
        sonuc = miktar * alis
        label_sonuc.config(text=f"{miktar:.2f} {secilen_doviz} = {sonuc:.2f} TL\n(Banka Alış Kuru: {alis:.4f} üzerinden)")
    else:
        # TL'den Dövize çeviri: Siz TL verip döviz alıyorsunuz (Banka size SATIYOR)
        # Dolayısıyla "Satış" kurunu kullanıyoruz.
        if satis > 0:
            sonuc = miktar / satis
            label_sonuc.config(text=f"{miktar:.2f} TL = {sonuc:.4f} {secilen_doviz}\n(Banka Satış Kuru: {satis:.4f} üzerinden)")
        else:
            label_sonuc.config(text="Hata: Satış kuru 0 olamaz.")

# Arayüzdeki kur listesini ve combobox elemanlarını güncelleyen yardımcı fonksiyon
def kurları_guncelle():
    global doviz_listesi
    # Tablodaki (Treeview) eski satırları tamamen siliyoruz
    for item in tree.get_children():
        tree.delete(item)
        
    # Web kazıma fonksiyonumuzu çağırarak güncel kurları alıyoruz
    doviz_listesi = fiyatlari_getir()
    
    if doviz_listesi:
        # Çekilen dövizlerin her birini satır satır tabloya yerleştiriyoruz
        for veri in doviz_listesi:
            tree.insert("", "end", values=(
                veri["doviz"],
                veri["fiyat"],
                veri["fark"],
                veri["alis"],
                veri["satis"]
            ))
            
        # Döviz hesaplayıcı seçeneği için combobox'ı güncelliyoruz
        doviz_isimleri = [d["doviz"] for d in doviz_listesi]
        combobox_doviz["values"] = doviz_isimleri
        if doviz_isimleri:
            combobox_doviz.current(0)
    else:
        messagebox.showwarning("Bağlantı Hatası", "Döviz kurları yüklenemedi!")

# --- 3. Aşama: Tasarım ve Arayüzün Kurulması ---
# Ana arayüz penceremizi oluşturuyoruz
app = tk.Tk()
app.title("Canlı Döviz Takip ve Hesaplama Botu")
app.geometry("550x700")
app.resizable(False, False) # Kullanıcının pencere boyutunu değiştirmesini engelliyoruz
app.configure(bg="#f1f2f6") # Pencere arka plan rengini gri ton yapıyoruz

# --- 4. Aşama: Canvas (Tuval) Alanı ve Final Görsel Ayarları ---
# Başlık ve görsel grafik arka planı için üstte bir Canvas alanı oluşturuyoruz
canvas = tk.Canvas(app, width=550, height=100, bg="#2f3542", highlightthickness=0)
canvas.pack(fill="x")

# Canvas üzerine yeşil renkte bir yükseliş grafik çizgisi (trend line) çiziyoruz
canvas.create_line(10, 85, 80, 65, 160, 75, 240, 35, 320, 50, 400, 20, 480, 30, 540, 10, fill="#2ed573", width=3, smooth=True)
canvas.create_line(10, 85, 80, 65, 160, 75, 240, 35, 320, 50, 400, 20, 480, 30, 540, 10, fill="#7bed9f", width=1, smooth=True)

# Başlık yazılarını Canvas üzerine ekliyoruz
canvas.create_text(275, 40, text="CANLI DÖVİZ TAKİP", fill="#ffffff", font=("Impact", 24, "bold"))
canvas.create_text(275, 75, text="Anlık veriler Bigpara sitesinden çekilmektedir.", fill="#a4b0be", font=("Arial", 10, "italic"))

# Tablomuzu barındıracak bir Çerçeve (Frame) kuruyoruz
tablo_frame = tk.Frame(app, bg="#f1f2f6")
tablo_frame.pack(pady=10, padx=15, fill="both", expand=True)

# Tablo için dikey kaydırma çubuğu (Scrollbar) ekliyoruz
scrollbar = ttk.Scrollbar(tablo_frame)
scrollbar.pack(side="right", fill="y")

# Çok sütunlu listeleme için Treeview bileşenini oluşturuyoruz
sutunlar = ("doviz", "fiyat", "fark", "alis", "satis")
tree = ttk.Treeview(tablo_frame, columns=sutunlar, show="headings", yscrollcommand=scrollbar.set, height=10)
tree.pack(fill="both", expand=True)

# Kaydırma çubuğunu Treeview ile ilişkilendiriyoruz
scrollbar.config(command=tree.yview)

# Tablo başlık isimlerini belirliyoruz
tree.heading("doviz", text="Döviz Cinsi")
tree.heading("fiyat", text="Fiyat")
tree.heading("fark", text="Değişim (%)")
tree.heading("alis", text="Alış")
tree.heading("satis", text="Satış")

# Sütun hizalamalarını ve genişliklerini piksellerine göre ayarlıyoruz
tree.column("doviz", width=120, anchor="w")
tree.column("fiyat", width=90, anchor="e")
tree.column("fark", width=90, anchor="center")
tree.column("alis", width=90, anchor="e")
tree.column("satis", width=90, anchor="e")

# Tablonun hemen altına yerleşen Manuel Kurları Yenileme Butonu
btn_yenile = tk.Button(app, text="Kurları Şimdi Güncelle", command=kurları_guncelle, bg="#1e90ff", fg="white", font=("Arial", 11, "bold"), bd=0, padx=15, pady=8, cursor="hand2")
btn_yenile.pack(pady=5)

# Döviz Çevirici panelini LabelFrame ile çevreleyerek ekliyoruz
hesap_paneli = tk.LabelFrame(app, text=" Döviz Çevirici / Hesap Makinesi ", bg="#f1f2f6", font=("Arial", 11, "bold"), fg="#2f3542", padx=15, pady=10)
hesap_paneli.pack(fill="x", padx=15, pady=15)

# Çevrilecek Miktar Etiketi ve Giriş Kutusu (Entry)
tk.Label(hesap_paneli, text="Miktar:", bg="#f1f2f6", font=("Arial", 10, "bold"), fg="#2f3542").grid(row=0, column=0, padx=5, pady=10, sticky="e")
entry_miktar = tk.Entry(hesap_paneli, width=12, font=("Arial", 11))
entry_miktar.insert(0, "100") # Varsayılan olarak kutunun içine 100 yazdırıyoruz
entry_miktar.grid(row=0, column=1, padx=5, pady=10, sticky="w")

# Hangi dövize çevrileceğinin seçildiği Combobox bileşeni
tk.Label(hesap_paneli, text="Döviz Cinsi:", bg="#f1f2f6", font=("Arial", 10, "bold"), fg="#2f3542").grid(row=0, column=2, padx=5, pady=10, sticky="e")
combobox_doviz = ttk.Combobox(hesap_paneli, width=10, font=("Arial", 11), state="readonly")
combobox_doviz.grid(row=0, column=3, padx=5, pady=10, sticky="w")

# Çeviri türü için Radiobutton'lar (Döviz -> TL ve TL -> Döviz)
var_yon = tk.IntVar(value=1)
rb1 = tk.Radiobutton(hesap_paneli, text="Döviz'den TL'ye (Alış)", variable=var_yon, value=1, bg="#f1f2f6", font=("Arial", 10), fg="#2f3542", activebackground="#f1f2f6")
rb1.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")

rb2 = tk.Radiobutton(hesap_paneli, text="TL'den Döviz'e (Satış)", variable=var_yon, value=2, bg="#f1f2f6", font=("Arial", 10), fg="#2f3542", activebackground="#f1f2f6")
rb2.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="w")

# Hesaplamayı gerçekleştiren dönüştür butonu
btn_hesapla = tk.Button(hesap_paneli, text="Dönüştür", command=hesapla, bg="#2ed573", fg="white", font=("Arial", 11, "bold"), bd=0, cursor="hand2")
btn_hesapla.grid(row=2, column=0, columnspan=4, padx=5, pady=10, sticky="we")

# Çeviri sonucunun görüntüleneceği alt etiket paneli
label_sonuc = tk.Label(hesap_paneli, text="Hesaplama sonucu burada gösterilecek.", bg="#ffffff", fg="#2f3542", font=("Arial", 11, "bold"), height=3, relief="groove", bd=1)
label_sonuc.grid(row=3, column=0, columnspan=4, padx=5, pady=10, sticky="we")

# Uygulama ilk açıldığında kurları çekip listeliyoruz
kurları_guncelle()

# Uygulamayı sonsuz döngüye sokarak kullanıcı işlemlerini beklemeye başlıyoruz
app.mainloop()