# 🗺️ Google Haritalar İşletme Verilerini Çeken Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.x-green?style=for-the-badge&logo=selenium&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Excel-red?style=for-the-badge&logo=pandas&logoColor=white)
![Edge](https://img.shields.io/badge/Edge-WebDriver-blue?style=for-the-badge&logo=microsoftedge&logoColor=white)

**Google Haritalar üzerinden işletme bilgilerini otomatik olarak çeken, Excel'e aktaran ve WhatsApp mesajı gönderebilen kapsamlı bir web otomasyon botu.**

</div>

---

## 📸 Ekran Görüntüsü

<div align="center">

![Uygulama Ekran Görüntüsü](public/Ekran%20görüntüsü%202026-06-06%20210542.png)

*Uygulama "Pizza İstanbul" araması ile 20 işletmenin verilerini başarıyla çekmiştir.*

</div>

---

## 🌟 Proje Hakkında

Bu proje, **Google Haritalar** üzerinde belirli bir arama terimi ile işletme bilgilerini (ad, adres, telefon numarası) otomatik olarak çeken bir **web scraping (veri kazıma)** uygulamasıdır.

### 🎯 Ne İşe Yarar?

Diyelim ki İstanbul'daki tüm pizzacıları, eczaneleri veya kuaförleri bulmak istiyorsunuz. Bu uygulama ile:

1. Arama terimini girersiniz (örn: "Pizza İstanbul")
2. Kaç işletme istediğinizi belirlersiniz (örn: 20)
3. **"Verileri Çek"** butonuna basarsınız
4. Bot otomatik olarak tarayıcıyı açar, Google Haritalar'da arar ve bilgileri çeker
5. Sonuçları Excel'e aktarabilir veya doğrudan WhatsApp mesajı gönderebilirsiniz

### 💡 Kullanım Alanları

| Alan | Örnek Kullanım |
|------|---------------|
| 🏪 **Pazarlama** | Belirli bir bölgedeki tüm işletmelerin iletişim bilgilerini toplama |
| 📊 **Pazar Araştırması** | Rakip analizi için sektördeki işletmeleri listeleme |
| 📱 **Toplu İletişim** | WhatsApp üzerinden işletmelere toplu mesaj gönderme |
| 📋 **Veri Tabanı** | İşletme rehberi oluşturma |

---

## 🔧 Özellikler

### Temel Özellikler
- ✅ **Otomatik Veri Çekme**: Google Haritalar'dan işletme adı, adres ve telefon numarası
- ✅ **Excel'e Aktarma**: Çekilen verileri `.xlsx` formatında kaydetme
- ✅ **WhatsApp Entegrasyonu**: Tek tıkla WhatsApp Web üzerinden mesaj gönderme
- ✅ **Kullanıcı Dostu Arayüz**: Tkinter tabanlı modern GUI

### Teknik Özellikler
- ✅ **Çoklu Tarayıcı Desteği**: Microsoft Edge (varsayılan) + Chrome (yedek)
- ✅ **Anti-Bot Koruması**: Otomasyon tespitini bypass eden özel ayarlar
- ✅ **Çerez Onay Yönetimi**: Google çerez ekranını otomatik geçme
- ✅ **Dinamik Selector Sistemi**: Google'ın değişen HTML yapısına uyum sağlayan çoklu selector
- ✅ **Akıllı Kaydırma**: Sonuç panelini hedefleyen sidebar scroll
- ✅ **Thread-Safe UI**: Tkinter ile arka plan thread'leri arasında güvenli iletişim

---

## 📋 Gereksinimler

### Yazılım Gereksinimleri

| Yazılım | Sürüm | Açıklama |
|---------|-------|----------|
| Python | 3.10+ | Programlama dili |
| Microsoft Edge | Son sürüm | Varsayılan tarayıcı (Windows'ta yüklü gelir) |
| pip | Son sürüm | Python paket yöneticisi |

### Python Kütüphaneleri

```bash
pip install selenium pandas openpyxl
```

| Kütüphane | Sürüm | Kullanım Amacı |
|-----------|-------|---------------|
| `selenium` | 4.x | Web otomasyon ve tarayıcı kontrolü |
| `pandas` | 2.x | Veri işleme ve Excel aktarımı |
| `openpyxl` | 3.x | Excel dosyası yazma motoru |
| `tkinter` | Yerleşik | Grafiksel kullanıcı arayüzü |
| `threading` | Yerleşik | Çoklu iş parçacığı yönetimi |
| `webbrowser` | Yerleşik | WhatsApp Web bağlantısı açma |

---

## 🚀 Kurulum ve Çalıştırma

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/AlicanKaya192/21-Farkli-Python-Projeleri.git
cd 21-Farkli-Python-Projeleri/16-İsletme-Verilerini-Ceken-Bot
```

### 2. Gerekli Kütüphaneleri Yükleyin
```bash
pip install selenium pandas openpyxl
```

### 3. Uygulamayı Çalıştırın
```bash
python isletme_verileri.py
```

### 4. Kullanım Adımları

1. **Arama Kelimesi**: "Aramak İstediğiniz Kelime" alanına arama terimini girin
   - Örnek: `"Eczane Kadıköy"`, `"Restoran Beşiktaş"`, `"Kuaför İstanbul"`
2. **İşletme Sayısı**: Kaç işletmenin verilerinin çekileceğini belirleyin
3. **Verileri Çek**: Kırmızı butona tıklayarak veri çekme işlemini başlatın
4. **Excel'e Aktar**: Yeşil butona tıklayarak sonuçları Excel dosyasına kaydedin
5. **WhatsApp Mesaj**: Tablodaki "Mesaj Gönder" sütununa tıklayarak WhatsApp'tan mesaj gönderin

---

## 🏗️ Proje Mimarisi

```
16-İsletme-Verilerini-Ceken-Bot/
├── isletme_verileri.py          # Ana uygulama dosyası
├── README.md                    # Bu dosya
├── isletme_verileri_rehber.ipynb # Kapsamlı proje rehberi (Jupyter Notebook)
├── selenium_webdriver_rehber.ipynb # Selenium & WebDriver eğitim notebooku
├── public/                      # Ekran görüntüleri
│   ├── Ekran görüntüsü 2026-06-06 210542.png
│   ├── google_maps_anasayfa.png
│   └── google_maps_sonuclar.png
```

---

## ⚙️ Teknik Detaylar

### Mimari Diyagram

```
┌─────────────────────────────────────────────────────┐
│                    Tkinter GUI                       │
│  ┌──────────┐  ┌────────────┐  ┌────────────────┐  │
│  │ Arama    │  │ Verileri   │  │ Excel'e        │  │
│  │ Kutusu   │  │ Çek Butonu │  │ Aktar Butonu   │  │
│  └──────────┘  └─────┬──────┘  └────────────────┘  │
│                      │                               │
│  ┌───────────────────┴───────────────────────────┐  │
│  │              Treeview Tablosu                   │  │
│  │  İşletme Adı │ Adres │ Tel │ Durum │ WhatsApp  │  │
│  └───────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────┘
                       │ threading.Thread (daemon)
                       ▼
┌──────────────────────────────────────────────────────┐
│              Selenium WebDriver                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Edge     │  │ Chrome   │  │ Anti-Bot          │   │
│  │ Driver   │  │ Fallback │  │ Ayarları          │   │
│  └──────────┘  └──────────┘  └──────────────────┘   │
│                                                       │
│  ┌────────────────────────────────────────────────┐  │
│  │ Google Haritalar İşlemleri:                     │  │
│  │ 1. Çerez onayı → 2. Arama → 3. Sonuç çekme    │  │
│  │ 4. Detay sayfası → 5. Veri parse → 6. Scroll   │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│                    Çıktılar                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Tablo    │  │ Excel    │  │ WhatsApp          │   │
│  │ (GUI)    │  │ (.xlsx)  │  │ (wa.me link)      │   │
│  └──────────┘  └──────────┘  └──────────────────┘   │
└──────────────────────────────────────────────────────┘
```

### Kullanılan CSS Selector'ları

| Eleman | Selector | Açıklama |
|--------|----------|----------|
| Arama Kutusu | `//form[contains(@jsaction, 'searchbox')]//input` | Google'ın dinamik ID'lerine karşı dayanıklı |
| İşletme Kartı | `.Nv2PK` | Sonuç listesindeki her işletme kartı |
| İşletme Adı | `//h1[contains(@class, 'DUwDvf')]` | Detay sayfasındaki işletme başlığı |
| Adres | `button[data-item-id='address'] .Io6YTe` | Adres bilgisi |
| Telefon | `button[data-item-id^='phone'] .Io6YTe` | Telefon numarası |
| Sonuç Paneli | `//div[@role='feed']` | Kaydırılabilir sonuç listesi |

---

## ⚠️ Bilinen Sorunlar ve Çözümler

| Sorun | Çözüm |
|-------|-------|
| Chrome yüklü değil hatası | Edge otomatik olarak kullanılır (Windows'ta varsayılan) |
| Çerez onay ekranı | Otomatik olarak geçilir (Türkçe/İngilizce) |
| `searchboxinput` bulunamadı | Çoklu selector ile fallback sistemi aktif |
| Sonsuz scroll döngüsü | Feed paneli hedefli scroll + yükseklik kontrolü |
| Thread hatası | `_update_ui()` ile thread-safe UI güncellemesi |

---

## 📚 Eğitim Materyalleri

Bu proje ile birlikte iki kapsamlı Jupyter Notebook sunulmaktadır:

1. **`isletme_verileri_rehber.ipynb`**: Projenin tüm kodlarının detaylı açıklaması
2. **`selenium_webdriver_rehber.ipynb`**: Selenium ve WebDriver kütüphanelerinin kapsamlı eğitimi

---

## 📄 Lisans

Bu proje eğitim amaçlı oluşturulmuştur. Google Haritalar'ın kullanım koşullarına dikkat ediniz.

---

## 👤 Geliştirici

**Alican Kaya** - [GitHub](https://github.com/AlicanKaya192)

---

<div align="center">

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! ⭐

</div>
