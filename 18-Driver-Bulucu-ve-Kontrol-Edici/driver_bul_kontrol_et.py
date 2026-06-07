# =============================================================================
# Proje #18: Driver Bulucu ve Kontrol Edici
# =============================================================================
# Bu uygulama, Windows işletim sistemindeki tüm donanım sürücülerini (driver)
# WMI (Windows Management Instrumentation) arayüzü üzerinden sorgulayarak
# bir Tkinter tablosunda (Treeview) listeleyen, arama yapılabilir ve çift tıkla
# Google'da sürücü aratılabilir bir masaüstü aracıdır.
# =============================================================================

# ---- Kütüphanelerin İçe Aktarılması ----
import wmi          # Windows Management Instrumentation — donanım ve sistem bilgilerine erişim sağlar
import json         # Sürücü bilgilerini JSON formatında dışa aktarmak için
import os           # Dosya yolu oluşturma ve dizin işlemleri için
import tkinter as tk     # Masaüstü grafik arayüz (GUI) kütüphanesi
from tkinter import ttk  # Treeview (tablo) ve gelişmiş widget'lar için Themed Tkinter modülü
import webbrowser   # Kullanıcının varsayılan tarayıcısında URL açmak için


# =============================================================================
# 1. SÜRÜCÜ LİSTELEME FONKSİYONU
# =============================================================================
def list_drivers(save_to_file=False):
    """
    WMI üzerinden bilgisayardaki tüm Plug and Play (PnP) cihazları sorgular.
    Her cihaz için ad, Device ID, üretici ve durum bilgilerini bir sözlük (dict)
    listesi olarak döndürür.

    Parametreler:
        save_to_file (bool): True ise sürücü bilgilerini JSON dosyasına da kaydeder.

    Dönüş:
        list[dict]: Sürücü bilgilerini içeren sözlük listesi.

    WMI Sorgusu (Arka Plan):
        Bu fonksiyon arka planda şu WQL (WMI Query Language) sorgusunu çalıştırır:
        SELECT * FROM Win32_PnPEntity
        Bu sorgu, işletim sisteminin Aygıt Yöneticisi'nde (Device Manager)
        listelenen tüm donanım ve sanal aygıtları döndürür.
    """
    try:
        # WMI bağlantısını kuruyoruz. Bu, COM (Component Object Model) arayüzü
        # üzerinden Windows'un yönetim altyapısına bağlanır.
        computer = wmi.WMI()

        drivers = []

        # Win32_PnPEntity sınıfı, Plug and Play uyumlu tüm aygıtları temsil eder.
        # Bu sınıf; ses kartı, ekran kartı, USB denetleyicileri, klavye, fare,
        # ağ adaptörleri, disk denetleyicileri gibi tüm donanımları içerir.
        for device in computer.Win32_PnPEntity():
            # Yalnızca adı ve Device ID'si olan geçerli cihazları işliyoruz
            if device.Name and device.DeviceID:
                # Cihazın durumunu kontrol ediyoruz.
                # Status == "OK" ise sürücü doğru şekilde yüklenmiş demektir.
                # Diğer durumlar (Error, Degraded vb.) sorunlu sürücüyü işaret eder.
                status = "Yüklü" if device.Status == "OK" else "Yüklü Değil"

                driver_info = {
                    "Cihaz": device.Name,
                    "Device ID": device.DeviceID,
                    # hasattr kontrolü ile üretici bilgisinin mevcut olup olmadığını doğruluyoruz.
                    # Bazı sanal aygıtlar (virtual devices) üretici bilgisi taşımaz.
                    "Üretici": device.Manufacturer if hasattr(device, 'Manufacturer') else "Bilinmiyor",
                    "Durum": status,
                    "Sürücü Linki": "Sürücüyü araştır"
                }
                drivers.append(driver_info)

        # İsteğe bağlı olarak tüm sürücü verilerini JSON formatında diske kaydediyoruz.
        # Bu, raporlama veya sonradan karşılaştırma amacıyla kullanışlıdır.
        if save_to_file:
            file_path = os.path.join(os.getcwd(), "drivers_info.json")
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(drivers, file, ensure_ascii=False, indent=4)
            print(f"Sürücü bilgileri {file_path} dosyasına kaydedildi.")

        return drivers

    except Exception as e:
        print(f"Hata: {str(e)}")
        return []


# =============================================================================
# 2. TKINTER ARAYÜZÜ VE TREEVIEW TABLOSU
# =============================================================================
def display_drivers_in_table():
    """
    Sürücü listesini çekip Tkinter GUI üzerinde Treeview tablosunda görüntüler.
    Ayrıca arama çubuğu ve çift tıkla Google'da arama gibi etkileşim özellikleri sunar.
    """
    # Önce tüm sürücüleri WMI üzerinden çekiyoruz
    drivers = list_drivers()

    # ---- Ana Pencere Oluşturma ----
    root = tk.Tk()
    root.title("Bilgisayar Sürücüleri")
    root.geometry("1000x500")  # Başlangıç boyutu (genişlik x yükseklik)

    # ---- Arama Çubuğu Bölümü ----
    # Üst kısımda yatay bir arama alanı oluşturuyoruz.
    search_frame = tk.Frame(root)
    search_frame.pack(fill="x", padx=10, pady=5)

    search_label = tk.Label(search_frame, text="Ara:")
    search_label.pack(side="left", padx=5)

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side="left", fill="x", expand=True, padx=5)

    # ---- Treeview Tablosu Oluşturma ----
    # ttk.Treeview, Excel benzeri çok sütunlu tablo görünümü sağlayan bir widget'tır.
    # show="headings" parametresi, varsayılan ağaç (tree) sütununu gizleyerek
    # yalnızca bizim tanımladığımız sütun başlıklarını gösterir.
    columns = ("Cihaz", "Device ID", "Üretici", "Durum", "Sürücü Linki")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    # Her sütun için başlık metnini ve genişliğini ayarlıyoruz
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200)

    # ---- Tabloyu Veriyle Doldurma Fonksiyonu ----
    def populate_treeview(data):
        """
        Treeview'daki mevcut satırları temizleyip verilen sürücü listesiyle yeniden doldurur.
        Her satıra durumuna göre renk etiketi (tag) atar.
        """
        # Önce mevcut tüm satırları siliyoruz (arama filtrelemesinde gereklidir)
        for item in tree.get_children():
            tree.delete(item)

        # Yeni verileri satır satır ekliyoruz
        for driver in data:
            item_id = tree.insert("", tk.END, values=(
                driver.get("Cihaz", "Bilinmiyor"),
                driver.get("Device ID", "Bilinmiyor"),
                driver.get("Üretici", "Bilinmiyor"),
                driver.get("Durum", "Bilinmiyor"),
                "Sürücüyü araştır" if driver.get("Sürücü Linki") != "Bilinmiyor" else "Bilinmiyor"
            ))

            # Koşullu renklendirme: Sürücü durumuna göre satır arka planını ayarlıyoruz.
            # "Yüklü" olan cihazlar yeşil, sorunlu olanlar kırmızı arka plana sahip olur.
            if driver.get("Durum") == "Yüklü":
                tree.item(item_id, tags=("yuklu",))
            else:
                tree.item(item_id, tags=("yuklu_degil",))

    # ---- Tag (Etiket) Stilleri ----
    # Treeview'da tag_configure ile etiketlere görsel stil atıyoruz.
    tree.tag_configure("yuklu", background="lightgreen")
    tree.tag_configure("yuklu_degil", background="lightcoral")

    # Tabloyu ilk verilerle dolduruyoruz
    populate_treeview(drivers)
    tree.pack(expand=True, fill="both")

    # ---- Arama (Filtreleme) İşlevi ----
    def search_drivers(event=None):
        """
        Arama kutusundaki metne göre sürücü listesini filtreler.
        Cihaz adı, Device ID, üretici veya durum alanlarından herhangi birinde
        eşleşme varsa o satır gösterilir.
        """
        query = search_entry.get().lower()
        filtered_drivers = [
            driver for driver in drivers
            if (driver.get("Cihaz") and query in driver["Cihaz"].lower()) or
               (driver.get("Device ID") and query in driver["Device ID"].lower()) or
               (driver.get("Üretici") and query in driver["Üretici"].lower()) or
               (driver.get("Durum") and query in driver["Durum"].lower())
        ]
        populate_treeview(filtered_drivers)

    # <KeyRelease> olayı: Kullanıcı bir tuşa her bastığında arama otomatik tetiklenir
    search_entry.bind("<KeyRelease>", search_drivers)

    search_button = tk.Button(search_frame, text="Ara", command=search_drivers)
    search_button.pack(side="left", padx=5)

    # ---- Çift Tıklama ile Google'da Sürücü Arama ----
    def on_treeview_double_click(event):
        """
        Treeview'daki bir satıra çift tıklandığında, o cihazın adıyla
        Google'da sürücü araması yapan bir URL açar.
        webbrowser.open() sisteme kurulu varsayılan tarayıcıyı kullanır.
        """
        item = tree.selection()[0]
        # pyrefly: ignore [bad-index]
        device_name = tree.item(item, "values")[0]
        driver_link = f"https://www.google.com/search?q={device_name} driver"
        if driver_link:
            webbrowser.open(driver_link)

    # <Double-1> olayı: Sol fare tuşuyla çift tıklama
    tree.bind("<Double-1>", on_treeview_double_click)

    # Tkinter olay döngüsünü başlatıyoruz — pencere kapanana kadar aktif kalır
    root.mainloop()


# =============================================================================
# 3. ANA GİRİŞ NOKTASI
# =============================================================================
# Bu blok, script doğrudan çalıştırıldığında (python driver_bul_kontrol_et.py)
# arayüzü başlatır. Modül olarak import edildiğinde ise çalışmaz.
if __name__ == "__main__":
    display_drivers_in_table()
