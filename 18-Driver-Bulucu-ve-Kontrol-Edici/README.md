# 📂 Proje #18 — Driver Bulucu ve Kontrol Edici

Windows işletim sistemindeki tüm donanım sürücülerini (driver) **WMI (Windows Management Instrumentation)** arayüzü üzerinden otomatik olarak tarayan, durumlarını renkli tabloda gösteren, arama yapılabilen ve çift tıkla sürücüyü Google'da aratabilmeyi sağlayan masaüstü uygulamasıdır.

<p align="center">
  <img src="./public/Ekran görüntüsü 2026-06-07 191630.png" alt="Driver Bulucu Ekran Görüntüsü" width="700"/>
</p>

---

## 🚀 Özellikler

- **Otomatik Donanım Tarama:** WMI'ın `Win32_PnPEntity` sınıfı üzerinden bilgisayardaki tüm Plug and Play aygıtları otomatik olarak tespit eder.
- **Koşullu Renklendirme:** Sürücüsü düzgün yüklenmiş cihazlar **yeşil**, sorunlu olanlar **kırmızı** arka planla gösterilir.
- **Anlık Arama / Filtreleme:** Arama çubuğuna yazdığınız metin, cihaz adı, Device ID, üretici ve durum alanlarında anlık olarak filtrelenir.
- **Google'da Sürücü Arama:** Tablodaki herhangi bir satıra çift tıklandığında, cihaz adıyla Google'da otomatik sürücü araması başlatılır.
- **JSON Dışa Aktarma:** İsteğe bağlı olarak tüm sürücü bilgileri `drivers_info.json` dosyasına kaydedilebilir.

---

## ⚠️ Platform Uyumluluğu

Bu uygulama yalnızca **Windows** işletim sisteminde çalışır. WMI, Windows'a özgü bir yönetim altyapısıdır ve Linux veya macOS üzerinde mevcut değildir.

---

## ⚙️ Kurulum ve Gereksinimler

```bash
# WMI kütüphanesini yükleyin (pywin32 bağımlılığı otomatik gelir)
pip install wmi
```

**Gerekli Python Sürümü:** Python 3.8+

---

## 💻 Kullanım

```bash
python driver_bul_kontrol_et.py
```

1. Uygulama başlatıldığında tüm donanım sürücüleri WMI üzerinden otomatik olarak taranır.
2. Tablo, **Cihaz Adı**, **Device ID**, **Üretici**, **Durum** ve **Sürücü Linki** sütunlarıyla listelenir.
3. Üst kısımdaki arama çubuğuna yazarak sonuçları anlık olarak filtreleyebilirsiniz.
4. Herhangi bir satıra **çift tıklayarak** Google'da o cihazın sürücüsünü aratabilirsiniz.

---

## 🛠️ Kullanılan Teknolojiler

| Kütüphane | Açıklama |
|-----------|----------|
| [**wmi**](https://pypi.org/project/WMI/) | Windows Management Instrumentation Python sarmalayıcısı — donanım, işletim sistemi ve servis bilgilerine erişim |
| [**pywin32**](https://pypi.org/project/pywin32/) | `wmi` kütüphanesinin bağımlılığı — Windows COM arayüzü ile iletişim kurar |
| **tkinter** | Python'ın yerleşik masaüstü GUI kütüphanesi |
| **json** | Sürücü bilgilerini yapılandırılmış JSON formatında kaydetmek için (built-in) |
| **webbrowser** | Varsayılan tarayıcıda URL açmak için (built-in) |

---

## 📘 Eğitim İçerikleri

Bu projenin arkasındaki teknik detayları öğrenmek için proje klasöründeki notebook dosyalarını inceleyebilirsiniz:

| Dosya | Açıklama |
|-------|----------|
| [**driver_bul_kontrol_et_Aciklamalari.ipynb**](./driver_bul_kontrol_et_Aciklamalari.ipynb) | Uygulamanın çalışma mantığını, WMI sorgularını, Treeview yapısını ve olay yönetimini adım adım açıklayan eğitim notebook'u |
| [**wmi_rehber.ipynb**](./wmi_rehber.ipynb) | WMI kütüphanesini kapsamlı şekilde inceleyen, donanım/yazılım/ağ/servis sorgulama örnekleri sunan detaylı rehber |
