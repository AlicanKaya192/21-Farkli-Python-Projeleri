<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"/>
  <img src="https://img.shields.io/github/license/AlicanKaya192/21-Farkli-Python-Projeleri?style=for-the-badge&color=green" alt="License"/>
  <img src="https://img.shields.io/github/last-commit/AlicanKaya192/21-Farkli-Python-Projeleri?style=for-the-badge&color=blue" alt="Last Commit"/>
  <img src="https://img.shields.io/github/repo-size/AlicanKaya192/21-Farkli-Python-Projeleri?style=for-the-badge&color=orange" alt="Repo Size"/>
  <img src="https://img.shields.io/github/stars/AlicanKaya192/21-Farkli-Python-Projeleri?style=for-the-badge&color=yellow" alt="Stars"/>
</p>

<h1 align="center">🐍 21 Farklı Python Projesi</h1>

<p align="center">
  <i>Python öğrenme yolculuğunda adım adım ilerlemek için hazırlanmış, başlangıçtan ileri seviyeye kadar 21 farklı proje koleksiyonu.</i>
</p>

<p align="center">
  <a href="#-projeler">Projeler</a> •
  <a href="#-kurulum">Kurulum</a> •
  <a href="#-kullanım">Kullanım</a> •
  <a href="#-teknolojiler">Teknolojiler</a> •
  <a href="#-katkıda-bulunma">Katkıda Bulunma</a> •
  <a href="#-lisans">Lisans</a>
</p>

---

## 📖 Hakkında

Bu repo, Python programlama dilini **pratik yaparak öğrenmek** amacıyla oluşturulmuş **21 farklı projeyi** barındırmaktadır. Her proje, farklı bir konuyu ve kütüphaneyi ele alarak Python ekosistemini keşfetmenizi sağlar.

> **Not:** Projeler sıralı olarak numaralandırılmıştır. Temel konulardan başlayıp ileri seviye uygulamalara doğru ilerler.

---

## 🚀 Projeler

| # | Proje Adı | Açıklama | Kullanılan Kütüphaneler | Durum |
|:-:|-----------|----------|------------------------|:-----:|
| 1 | [**Web Sitelerinden Veri Çekme**](./%231-Web-Sitelerinden-Veri-Cekme) | Web scraping teknikleriyle sitelerden veri toplama | `requests`, `beautifulsoup4` | ✅ |
| 2 | [**Dijital Masaüstü Saati**](./%232-Dijital-Masaüstü-Saati) | Tkinter ile canlı güncellenen masaüstü saat uygulaması | `tkinter`, `time` | ✅ |
| 3 | [**QR Kod**](./%233-QR-Kod) | QR kod oluşturma ve okuma uygulaması | `tkinter` | 🔄 |
| 4 | **Sesli Kitap Oluşturucu** | — | — | 📋 |
| 5 | **Yüz Algılama Uygulaması** | — | — | 📋 |
| 6 | **İnstagram Bot Yapımı** | — | — | 📋 |
| 7 | **İnstagram Analiz Uygulaması** | — | — | 📋 |
| 8 | **Link Kısaltma Uygulaması** | — | — | 📋 |
| 9 | **Bahis Analiz Uygulaması** | — | — | 📋 |
| 10 | **İnstagram Geri Takip Etmeyenler Uygulaması** | — | — | 📋 |
| 11 | **Stok Takip Uygulaması** | — | — | 📋 |
| 12 | **İnstagram Etkileşim Saatini Analiz Eden Uygulama** | — | — | 📋 |
| 13 | **Video Boyutu Hesaplama Uygulaması** | — | — | 📋 |
| 14 | **Basit Keylogger Yapımı (Eğitim Amaçlı)** | — | — | 📋 |
| 15 | **İnternetten Veri Çeken Bot Yazımı** | — | — | 📋 |
| 16 | **İşletme Verilerini Çeken Bot** | — | — | 📋 |
| 17 | **Görüntülerden Arka Planı Silen Uygulama** | — | — | 📋 |
| 18 | **Driver Bulucu ve Kontrol Edici** | — | — | 📋 |
| 19 | **Kripto Botu (BETA)** | — | — | 📋 |
| 20 | **Yapay Zeka Asistan Botu Yazımı ve Mantığı** | — | — | 📋 |
| 21 | **YouTube Video İndirme Botu (Sınırsız Kullanım)** | — | — | 📋 |

> **Durum Açıklamaları:** ✅ Tamamlandı · 🔄 Devam Ediyor · 📋 Planlandı

---

## 🏗️ Proje Detayları

### 📂 Proje #1 — Web Sitelerinden Veri Çekme

Web scraping (web kazıma) tekniklerini öğrenmek için hazırlanmış üç aşamalı proje:

| Dosya | Açıklama |
|-------|----------|
| `1.1_web.py` | Temel web scraping: HTTP istekleri, HTML parse etme, element bulma |
| `1.2_korona_veri.py` | Sağlık Bakanlığı Covid-19 verilerini tablolardan çekme |
| `1.3_itopya_islemci_fiyat_listesi_cekme.py` | İtopya'dan işlemci ürün adı, fiyat ve linkleri çekme |

**Öğrenilen Konular:**
- HTTP GET istekleri ve durum kodları (200, 403, 404, 500)
- BeautifulSoup ile HTML ayrıştırma (parsing)
- `find()` ve `find_all()` metotları ile element seçimi
- CSS sınıflarına göre element filtreleme
- Hata yönetimi (try-except) ile güvenli veri çekme

---

### 📂 Proje #2 — Dijital Masaüstü Saati

Tkinter kütüphanesi ile oluşturulmuş, canlı güncellenen dijital saat uygulaması:

| Dosya | Açıklama |
|-------|----------|
| `2.1_dijital_saat.py` | Saat ve tarih bilgisini gösteren masaüstü uygulaması |

**Öğrenilen Konular:**
- Tkinter ile GUI (Grafiksel Arayüz) oluşturma
- `Label`, `Tk`, `grid()` layout sistemi
- `time.strftime()` ile zaman formatlama
- `.after()` metodu ile periyodik güncelleme (donmadan)
- Widget stillendirme (font, renk, kenarlık)

---

### 📂 Proje #3 — QR Kod *(Devam Ediyor)*

QR kod oluşturma ve okuma uygulaması geliştirme aşamasında.

---

## ⚙️ Kurulum

### Gereksinimler

- **Python 3.8+** yüklü olmalıdır
- `pip` paket yöneticisi

### Adımlar

```bash
# 1. Repoyu klonlayın
git clone https://github.com/AlicanKaya192/21-Farkli-Python-Projeleri.git

# 2. Proje dizinine girin
cd 21-Farkli-Python-Projeleri

# 3. Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt
```

---

## 🎯 Kullanım

Her proje kendi klasörü içinde bağımsız olarak çalışabilir:

```bash
# Örnek: Web Scraping projesini çalıştırmak
python "#1-Web-Sitelerinden-Veri-Cekme/1.1_web.py"

# Örnek: Dijital Saati çalıştırmak
python "#2-Dijital-Masaüstü-Saati/2.1_dijital_saat.py"
```

---

## 🛠️ Teknolojiler

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Requests-2CA5E0?style=for-the-badge&logo=python&logoColor=white" alt="Requests"/>
  <img src="https://img.shields.io/badge/BeautifulSoup-59666C?style=for-the-badge&logo=python&logoColor=white" alt="BeautifulSoup"/>
  <img src="https://img.shields.io/badge/Tkinter-FF6F00?style=for-the-badge&logo=python&logoColor=white" alt="Tkinter"/>
</p>

| Kütüphane | Açıklama | Projeler |
|-----------|----------|----------|
| `requests` | HTTP istekleri göndermek için | #1 |
| `beautifulsoup4` | HTML/XML ayrıştırma | #1 |
| `tkinter` | Masaüstü GUI oluşturma (built-in) | #2, #3 |
| `time` | Tarih/saat işlemleri (built-in) | #2 |

---

## 📁 Proje Yapısı

```
21-Farkli-Python-Projeleri/
│
├── 📂 #1-Web-Sitelerinden-Veri-Cekme/
│   ├── 1.1_web.py                              # Temel web scraping
│   ├── 1.2_korona_veri.py                      # Covid-19 veri çekme
│   └── 1.3_itopya_islemci_fiyat_listesi_cekme.py  # E-ticaret veri çekme
│
├── 📂 #2-Dijital-Masaüstü-Saati/
│   └── 2.1_dijital_saat.py                     # Dijital saat uygulaması
│
├── 📂 #3-QR-Kod/
│   └── 3.1_qr_kod.py                          # QR kod uygulaması (devam ediyor)
│
├── .github/
│   └── workflows/
│       └── python-lint.yml                     # Otomatik kod kalite kontrolü
│
├── .gitignore                                  # Git tarafından takip edilmeyecek dosyalar
├── LICENSE                                     # MIT Lisansı
├── README.md                                   # Bu dosya
└── requirements.txt                            # Python bağımlılıkları
```

---

## 🤝 Katkıda Bulunma

Katkılarınız memnuniyetle karşılanır! Aşağıdaki adımları izleyerek katkıda bulunabilirsiniz:

1. Bu repoyu **fork** edin
2. Yeni bir **branch** oluşturun (`git checkout -b feature/yeni-proje`)
3. Değişikliklerinizi **commit** edin (`git commit -m 'Yeni proje eklendi'`)
4. Branch'inizi **push** edin (`git push origin feature/yeni-proje`)
5. Bir **Pull Request** açın

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.

---

## 👤 İletişim

<p align="center">
  <a href="https://github.com/AlicanKaya192">
    <img src="https://img.shields.io/badge/GitHub-AlicanKaya192-181717?style=for-the-badge&logo=github" alt="GitHub"/>
  </a>
  <a href="https://alican-kaya.com/">
    <img src="https://img.shields.io/badge/Website-alican--kaya.com-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website"/>
  </a>
</p>

---

<p align="center">
  <b>⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!</b>
</p>
