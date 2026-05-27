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

> **Not:** Projeler sıralı olarak numaralandırılmıştır. Temel konulardan başlayıp ileri seviye uygulamalara doğru ilerler. Ayrıca tamamlanan her proje klasöründe kodun işleyişini adım adım anlatan etkileşimli **Jupyter Notebook (`.ipynb`)** eğitim dosyaları yer almaktadır.

---

## 🚀 Projeler

| # | Proje Adı | Açıklama | Kullanılan Kütüphaneler | Durum |
|:-:|-----------|----------|------------------------|:-----:|
| 1 | [**Web Sitelerinden Veri Çekme**](./01-Web-Sitelerinden-Veri-Cekme) | Web scraping teknikleriyle sitelerden veri toplama | `requests`, `beautifulsoup4` | ✅ |
| 2 | [**Dijital Masaüstü Saati**](./02-Dijital-Masaüstü-Saati) | Tkinter ile canlı güncellenen masaüstü saat uygulaması | `tkinter`, `time` | ✅ |
| 3 | [**QR Kod**](./03-QR-Kod) | QR kod oluşturma ve SVG olarak kaydetme uygulaması | `tkinter`, `pyqrcode` | ✅ |
| 4 | [**Sesli Kitap Okuyucu**](./04-Sesli-PDF-Okuyucu) | PDF içindeki metni okuyan uygulama | `tkinter`, `PyPDF2`, `gTTS` | ✅ |
| 5 | [**Yüz Algılama Uygulaması**](./05-Yüz-Algılama-Uygulaması) | OpenCV ve Haar Cascade ile resimlerde yüz tespiti | `opencv-python`, `Pillow`, `numpy`, `tkinter` | ✅ |
| 6 | [**Instagram Bot Yapımı**](./06-Instagram-Bot-Yapimi) | Instaloader ile profil gönderilerini indiren GUI botu | `instaloader`, `tkinter` | ✅ |
| 7 | [**Instagram Analiz Uygulaması**](./07-Instagram-Analiz-Uygulaması) | Instagram profil istatistiklerini gösteren GUI uygulaması | `instaloader`, `tkinter` | ✅ |
| 8 | [**Link Kısaltma Uygulaması**](./08-Link-Kısaltma-Uygulaması) | TinyURL API ile uzun linkleri kısaltan ve kopyalayan araç | `requests`, `pyperclip`, `tkinter` | ✅ |
| 9 | [**Bahis Analiz Uygulaması**](./09-Bahis-Analiz-Uygulaması) | Sporx üzerinden form decay ve Poisson modelleriyle Üst/Alt tahmini yapan GUI analiz aracı | `requests`, `beautifulsoup4`, `tkinter` | ✅ |
| 10 | [**İnstagram Geri Takip Etmeyenler Uygulaması**](./10-Instagram-Geri-Takip-Etmeyenler-Uygulaması) | HTML takipçi/takip edilen verilerini karşılaştırarak geri takip etmeyenleri bulan araç | `pandas`, `beautifulsoup4`, `fpdf`, `tkinter` | ✅ |
| 11 | **Stok Takip Uygulaması** | — | — | 📋 |
| 12 | **İnstagram Etkileşim Saatini Analiz Eden Uygulama** | — | — | 📋 |
| 13 | **Video Boyutu Hesaplama Uygulaması** | — | — | 📋 |
| 14 | **Basit Keylogger Yapımı (Eğitim Amaçlı)** | — | — | ✅ |
| 15 | **İnternetten Veri Çeken Bot Yazımı** | — | — | 📋 |
| 16 | **İşletme Verilerini Çeken Bot** | — | — | 📋 |
| 17 | **Görüntülerden Arka Planı Silen Uygulama** | — | — | 📋 |
| 18 | **Driver Bulucu ve Kontrol Edici** | — | — | 📋 |
| 19 | [**Kripto Botu (BETA)**](./19-Kripto-Botu-(Beta)) | BtcTurk API'si ile çalışan, 5 dakikalık periyotlarda fiyat gözlemleyen ve otomatik alım-satım yapan GUI botu | `requests`, `tkinter` | ✅ |
| 20 | **Yapay Zeka Asistan Botu Yazımı ve Mantığı** | — | — | 📋 |
| 21 | [**YouTube Video İndirici**](./21-Youtube-Video-İndirici) | YouTube videolarını ve seslerini indirme | `yt-dlp`, `pillow`, `requests`, `tkinter` | ✅ |

> **Durum Açıklamaları:** ✅ Tamamlandı · 🔄 Devam Ediyor · 📋 Planlandı

---

## 🏗️ Proje Detayları

### 📂 Proje #1 — Web Sitelerinden Veri Çekme

Web scraping (web kazıma) tekniklerini öğrenmek için hazırlanmış üç aşamalı proje:

| Dosya | Açıklama |
|-------|----------|
| `1.1_web.py` | Temel web scraping: HTTP istekleri, HTML parse etme, element bulma |
| `1.1_web_Aciklamalari.ipynb` | Web scraping temellerini adım adım anlatan interaktif rehber |
| `1.2_korona_veri.py` | Sağlık Bakanlığı Covid-19 verilerini tablolardan çekme |
| `1.2_korona_veri_Aciklamalari.ipynb` | Tablo verisi ayıklama mantığını açıklayan eğitim dosyası |
| `1.3_itopya_islemci_fiyat_listesi_cekme.py` | İtopya'dan işlemci ürün adı, fiyat ve linkleri çekme |
| `1.3_itopya_..._Aciklamalari.ipynb` | Gelişmiş e-ticaret veri çekme işleminin detaylı rehberi |

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
| `Dijital_Saat_Aciklamalari.ipynb` | Uygulamanın çalışma mantığını ve Tkinter kullanımını anlatan eğitim dosyası |

**Öğrenilen Konular:**
- Tkinter ile GUI (Grafiksel Arayüz) oluşturma
- `Label`, `Tk`, `grid()` layout sistemi
- `time.strftime()` ile zaman formatlama
- `.after()` metodu ile periyodik güncelleme (donmadan)
- Widget stillendirme (font, renk, kenarlık)

---

### 📂 Proje #3 — QR Kod

Tkinter ve PyQRCode kütüphaneleri kullanılarak geliştirilmiş, metin veya bağlantıları (URL) QR koda dönüştüren masaüstü uygulaması:

| Dosya | Açıklama |
|-------|----------|
| `3.1_qr_kod.py` | Girilen URL'yi QR koda çevirip istenilen konuma SVG formatında kaydeden uygulama |
| `QR_Kod_Aciklamalari.ipynb` | Karekod üretim sürecini kod bloklarıyla aşama aşama gösteren doküman |

**Öğrenilen Konular:**
- `pyqrcode` ile metin verisinden QR kod (Karekod) oluşturma ve SVG formatında ölçekli (scale) dışa aktarma
- `tkinter.filedialog.asksaveasfilename()` ile kullanıcının dosya kaydetme yeri ve ismini seçebileceği işletim sistemi diyalog penceresini kullanma
- Tkinter GUI üzerinde `Entry` (girdi alanı) verisini `.get()` metoduyla çekip işlem yapma
- İşlem sonucuna göre GUI üzerindeki etiket (`Label`) metnini `.config()` metodu ile dinamik olarak güncelleme

---

### 📂 Proje #4 — Sesli Kitap Okuyucu

Seçilen bir PDF dosyasındaki metinleri ayıklayıp bu metinleri gerçeğe yakın bir sese dönüştüren ve oynatan uygulama:

| Dosya | Açıklama |
|-------|----------|
| `4.1_sesli_pdf.py` | Seçilen PDF dosyasını okuyan ve MP3 formatında çalan uygulama |
| `Sesli_PDF_Okuyucu_Aciklamalari.ipynb` | PDF okuma ve sesi oynatma döngüsünü adım adım anlatan rehber |

**Öğrenilen Konular:**
- `PyPDF2` ile PDF dosyalarından metin ayıklama (`extract_text`)
- `gTTS` (Google Text-to-Speech) ile metni sese dönüştürme ve kaydetme
- `os.startfile()` ile sistemin yerleşik medya oynatıcısını başlatma
- `tkinter.filedialog.askopenfilename()` ile dosya seçme işlemleri

---

### 📂 Proje #5 — Yüz Algılama Uygulaması

OpenCV ve makine öğrenimi tabanlı Haar Cascade sınıflandırıcıları kullanılarak geliştirilmiş yüz algılama uygulaması:

| Dosya | Açıklama |
|-------|----------|
| `yuz_algilama.py` | Seçilen resim üzerindeki insan yüzlerini tespit edip işaretleyen Tkinter tabanlı uygulama |
| `yuz_algilama_Aciklamalari.ipynb` | OpenCV ile görüntü işleme ve yüz tespit algoritmalarını anlatan eğitim dosyası |
| `face_detector.xml` | Önceden eğitilmiş Haar Cascade yüz tanıma modeli |

**Öğrenilen Konular:**
- OpenCV (`cv2`) ile görüntü okuma, işleme ve renk formatı dönüştürme (BGR'den RGB ve Gri tonlamaya)
- Haar Cascade (`CascadeClassifier`) modeli ile nesne/yüz tespiti
- Numpy array manipülasyonu ile Türkçe karakterli dosya yollarından görüntü yükleme
- Pillow (`Image`, `ImageTk`) ile OpenCV görüntülerini Tkinter GUI üzerinde gösterme
- Tkinter Canvas üzerinde resim sergileme ve dosya iletişim kutuları (FileDialog) kullanımı

---

### 📂 Proje #6 — Instagram Bot Yapımı

Instaloader ve Tkinter kütüphaneleri kullanılarak geliştirilmiş, belirtilen bir Instagram hesabındaki tüm gönderileri otomatik olarak indiren masaüstü uygulaması:

| Dosya | Açıklama |
|-------|----------|
| `insta.py` | Gönderileri indiren Tkinter tabanlı uygulama |
| `insta_Aciklamalari.ipynb` | Instaloader kullanımı ve arayüz entegrasyonunu anlatan eğitim dosyası |

**Öğrenilen Konular:**
- `instaloader` ile Instagram'a giriş yapma ve profil verilerini çekme
- Hedef profilin gönderilerini (`get_posts`) bir döngü ile klasörlere kaydetme
- `try-except` blokları ile hataları (2FA, gizli profil vb.) yakalama ve yönetme
- Tkinter'da şifre alanlarını gizleme (`show="*"`) ve tablo (`Frame`) oluşturma

---

### 📂 Proje #7 — Instagram Analiz Uygulaması

Instaloader ve Tkinter kütüphaneleri kullanılarak geliştirilmiş, belirtilen bir Instagram hesabının profil detaylarını ve istatistiklerini gösteren masaüstü uygulaması:

| Dosya | Açıklama |
|-------|----------|
| `insta_analiz.py` | Instagram profil analizlerini sunan Tkinter tabanlı uygulama |
| `insta_analiz_Aciklamalari.ipynb` | Profil istatistikleri ve arayüz yapısını anlatan eğitim dosyası |

**Öğrenilen Konular:**
- Profil takipçi sayısı, takip edilenler, biyografi ve profil fotoğrafı bilgilerini çekme
- Profil verilerini arayüzde dinamik olarak sergileme
- Hata yakalama ve kullanıcıyı hata diyaloglarıyla bilgilendirme

---

### 📂 Proje #8 — Link Kısaltma Uygulaması

TinyURL API'si ve Tkinter kullanılarak geliştirilmiş, uzun web adreslerini saniyeler içinde kısaltan ve tek tıkla panoya kopyalayan masaüstü uygulaması:

| Dosya | Açıklama |
|-------|----------|
| `link_kisaltma.py` | TinyURL API'si ile çalışan link kısaltma uygulaması |
| `link_kisaltma_Aciklamalari.ipynb` | API istekleri ve pano kopyalama mantığını anlatan eğitim dosyası |

**Öğrenilen Konular:**
- Web API'leri ile GET istekleri göndererek veri alışverişi yapma
- `pyperclip` kütüphanesi kullanarak metinleri işletim sistemi panosuna (clipboard) kopyalama
- Buton durumlarını (`state=tk.DISABLED` / `state=tk.NORMAL`) dinamik olarak yönetme

---

### 📂 Proje #9 — Bahis Analiz Uygulaması

Sporx sitesinden takımların fikstür verilerini çekerek, form decay (zaman ağırlıklı ortalama) ve ev/deplasman katsayıları eşliğinde Poisson olasılık dağılımı ile maç gol ve derbi tahminleri yapan masaüstü uygulaması:

| Dosya | Açıklama |
|-------|----------|
| `bahis_analiz.py` | Poisson ve zaman ağırlıklı algoritmayla çalışan bahis analiz uygulaması |
| `bahis_analiz_Aciklamalari.ipynb` | Veri çekme, olasılık hesaplama ve algoritmayı anlatan eğitim dosyası |

**Öğrenilen Konular:**
- Poisson olasılık dağılımı ($P(k; \lambda)$) ve Alt/Üst 2.5 hesaplamaları
- Form Decay (zaman ağırlıklı ortalama - $0.85^i$) ve Saha Avantajı katsayıları
- Türkçe tarih metinlerini ayrıştırıp `datetime.date` nesnesine çevirme ve gün farkı hesaplama
- Unicode birleştirme karakterleri hatasından (`\u0307`) kaçınarak SEO uyumlu URL üretimi

---

### 📂 Proje #10 — İnstagram Geri Takip Etmeyenler Uygulaması

Instagram hesabınızın takipçi (`followers.html`) ve takip edilenler (`following.html`) listelerini karşılaştırarak sizi geri takip etmeyen kişileri tespit eden, sonuçları Excel veya PDF olarak raporlayabilen masaüstü uygulaması:

| Dosya | Açıklama |
|-------|----------|
| `geri_takip_etmeyenler.py` | Geri takip etmeyenleri bulan Tkinter tabanlı uygulama |
| `geri_takip_etmeyenler_Aciklamalari.ipynb` | HTML ayrıştırma, küme farkı ve thread mantığını anlatan eğitim dosyası |

**Öğrenilen Konular:**
- Küme Farkı (Set Difference) işlemiyle geri takip etmeyenleri ($A \setminus B$) filtreleme
- `StringVar` değişkenlerine `trace_add` uygulayarak dinamik arama filtresi tasarlama
- `threading` kullanarak dosya okuma ve HTML ayrıştırma sırasında arayüz donmalarını önleme
- FPDF kütüphanesiyle profil bağlantıları içeren dinamik PDF ve Pandas ile Excel raporlama

---

### 📂 Proje #14 — Basit Keylogger Yapımı (Eğitim Amaçlı)

`keyboard` kütüphanesi kullanılarak geliştirilmiş, basit bir keylogger. Klavye girişlerini metin dosyasına kaydederek temel düzeyde klavye olaylarını dinleme mantığını açıklar.

| Dosya | Açıklama |
|-------|----------|
| `keylogger.py` | Klavye olaylarını dinleyerek metin dosyasına kaydeden temel keylogger uygulaması. `on_key_press()` fonksiyonu ile tuş girişlerini okur ve `keyboard.wait()` ile programı aktif tutar. |

**Öğrenilen Konular:**
- `keyboard` kütüphanesi ile klavye olaylarını dinleme (hooking)
- `on_press()` callback fonksiyonu ile tuş basımlarını yakalama
- `keyboard.wait()` ile programı bloklamadan (asenkron) dinleme modunda çalıştırma
- Temel dosya yazma işlemleri ve özel karakterlerin (space, enter) dosyaya kaydedilmesi

> **⚠️ Yasal Uyarı:** Bu proje yalnızca **eğitim amaçlı** ve **yasal izinler çerçevesinde** kullanılmalıdır. Başkalarının izni olmadan bilgisayar sistemlerine keylogger kurmak ve kullanmak yasa dışıdır ve etik değildir.

---

### 📂 Proje #19 — Kripto Botu (BETA)

BtcTurk API'si kullanılarak geliştirilmiş, 5 dakikalık periyotlarda fiyat gözlemleyerek otomatik alım-satım yapan ve detaylı log panelleri barındıran masaüstü uygulaması:

| Dosya | Açıklama |
|-------|----------|
| `app.py` | Tkinter arayüzü, 5 dakikalık gözlem döngüsü ve thread yönetimi içeren ana kod |
| `bot.py` | API bağlantısını ve anahtar doğrulamasını test eden yardımcı script |
| `btcturk_wrapper.py` | HMAC-SHA256 Base64 imzalama algoritması ve BtcTurk REST API entegrasyonu |
| `endpoints.py` | API istekleri için BtcTurk endpoint tanımları ve yetkilendirme grupları |
| `README.md` | Projenin mimarisini ve kullanım detaylarını içeren alt dokümantasyon |
| `kripto_bot_Aciklamalari.ipynb` | Projenin çalışmasını, imzalama mantığını ve akış şemasını anlatan eğitim notebook dosyası |

**Öğrenilen Konular:**
- HMAC-SHA256 ve Base64 algoritmaları ile BtcTurk API için güvenli imza (signature) üretimi
- BtcTurk REST API ile bakiye sorgulama, fiyat izleme, piyasa/limit emirleri gönderme ve iptal etme
- Çok iş parçacıklı (`threading`) mimari ile GUI donmasını engelleyen arka plan döngü tasarımı
- Arayüzde `Treeview` kullanımı ve verilerin (emirler, loglar, bakiyeler) dinamik olarak listelenip sıralanması
- Sistem loglarını (Sistem, Alım/Satım, Hata) 3 farklı kanalda ayrıştırarak görselleştirme

---

### 📂 Proje #21 — YouTube Video İndirici

yt-dlp kütüphanesi kullanılarak geliştirilmiş, belirtilen YouTube linkinden video (MP4) veya ses (MP3) indirebilen, threading altyapısı sayesinde işlem yaparken donmayan masaüstü uygulaması:

| Dosya | Açıklama |
|-------|----------|
| `video_indir.py` | Çok iş parçacıklı (threading) ve FFmpeg fallback destekli ana kod |
| `video_indir_Aciklamalari.ipynb` | Uygulama mantığını adım adım açıklayan eğitim notebook dosyası |

**Öğrenilen Konular:**
- `yt-dlp` modülü ile video/ses format analizi ve indirme
- `threading` kullanarak arka plan görevleri koşturma ve GUI donmasını engelleme
- `root.after` yardımıyla thread-safe olarak grafik arayüz elemanlarını güncelleme
- FFmpeg eksikliğinde alternatif formatlara (.m4a / best) yumuşak geçiş (fallback) yapma

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
python "01-Web-Sitelerinden-Veri-Cekme/1.1_web.py"

# Örnek: Dijital Saati çalıştırmak
python "02-Dijital-Masaüstü-Saati/2.1_dijital_saat.py"
```

---

## 🛠️ Teknolojiler

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Requests-2CA5E0?style=for-the-badge&logo=python&logoColor=white" alt="Requests"/>
  <img src="https://img.shields.io/badge/BeautifulSoup-59666C?style=for-the-badge&logo=python&logoColor=white" alt="BeautifulSoup"/>
  <img src="https://img.shields.io/badge/Tkinter-FF6F00?style=for-the-badge&logo=python&logoColor=white" alt="Tkinter"/>
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV"/>
</p>

| Kütüphane | Açıklama | Projeler |
|-----------|----------|----------|
| `requests` | HTTP istekleri göndermek için | #1, #8, #9 |
| `beautifulsoup4` | HTML/XML ayrıştırma | #1, #9, #10 |
| `tkinter` | Masaüstü GUI oluşturma (built-in) | #2, #3, #4, #5, #6, #7, #8, #9, #10 |
| `time` | Tarih/saat işlemleri (built-in) | #2 |
| `pyqrcode` | QR kod oluşturma ve dışa aktarma | #3 |
| `PyPDF2` | PDF okuma ve metin çıkarma | #4 |
| `gTTS` | Metni sese dönüştürme (Google TTS) | #4 |
| `opencv-python` | Görüntü işleme ve yüz algılama | #5 |
| `numpy` | Çok boyutlu dizi ve matris işlemleri | #5 |
| `Pillow` | Görüntü işleme (Tkinter entegrasyonu) | #3, #5 |
| `instaloader` | Instagram hesaplarından veri çekme | #6, #7 |
| `pyperclip` | Panoya (clipboard) metin kopyalama | #8 |
| `pandas` | Verileri Excel formatına aktarmak için | #10 |
| `fpdf` | PDF raporları oluşturmak için | #10 |
| `keyboard` | Klavye olaylarını dinleme | #14 |

---

## 📁 Proje Yapısı

```
21-Farkli-Python-Projeleri/
│
├── 📂 01-Web-Sitelerinden-Veri-Cekme/
│   ├── README.md                               # Proje açıklaması
│   ├── 1.1_web.py                              # Temel web scraping
│   ├── 1.1_web_Aciklamalari.ipynb              # Notebook eğitim materyali
│   ├── 1.2_korona_veri.py                      # Covid-19 veri çekme
│   ├── 1.2_korona_veri_Aciklamalari.ipynb      # Notebook eğitim materyali
│   ├── 1.3_itopya_islemci_fiyat_listesi_cekme.py  # E-ticaret veri çekme
│   └── 1.3_itopya_islemci_fiyat_listesi_cekme_Aciklamalari.ipynb # Notebook eğitim materyali
│
├── 📂 02-Dijital-Masaüstü-Saati/
│   ├── README.md                               # Proje açıklaması
│   ├── 2.1_dijital_saat.py                     # Dijital saat uygulaması
│   └── Dijital_Saat_Aciklamalari.ipynb         # Notebook eğitim materyali
│
├── 📂 03-QR-Kod/
│   ├── README.md                               # Proje açıklaması
│   ├── 3.1_qr_kod.py                           # QR kod uygulaması
│   └── QR_Kod_Aciklamalari.ipynb               # Notebook eğitim materyali
│
├── 📂 04-Sesli-PDF-Okuyucu/
│   ├── README.md                               # Proje açıklaması
│   ├── 4.1_sesli_pdf.py                        # Sesli PDF okuyucu kodu
│   └── Sesli_PDF_Okuyucu_Aciklamalari.ipynb    # Notebook eğitim materyali
│
├── 📂 05-Yüz-Algılama-Uygulaması/
│   ├── README.md                               # Proje açıklaması
│   ├── yuz_algilama.py                         # Yüz algılama kodu
│   ├── yuz_algilama_Aciklamalari.ipynb         # Notebook eğitim materyali
│   └── face_detector.xml                       # Haar Cascade modeli
│
├── 📂 06-Instagram-Bot-Yapimi/
│   ├── README.md                               # Proje açıklaması
│   ├── insta.py                                # Gönderi indirme botu kodu
│   └── insta_Aciklamalari.ipynb                # Notebook eğitim materyali
│
├── 📂 07-Instagram-Analiz-Uygulaması/
│   ├── README.md                               # Proje açıklaması
│   ├── insta_analiz.py                         # Instagram analiz kodu
│   └── insta_analiz_Aciklamalari.ipynb         # Notebook eğitim materyali
│
├── 📂 08-Link-Kısaltma-Uygulaması/
│   ├── README.md                               # Proje açıklaması
│   ├── link_kisaltma.py                        # Link kısaltma kodu
│   └── link_kisaltma_Aciklamalari.ipynb        # Notebook eğitim materyali
│
├── 📂 09-Bahis-Analiz-Uygulaması/
│   ├── README.md                               # Proje açıklaması
│   ├── bahis_analiz.py                         # Bahis analiz uygulaması kodu
│   └── bahis_analiz_Aciklamalari.ipynb         # Notebook eğitim materyali
│
├── 📂 10-Instagram-Geri-Takip-Etmeyenler-Uygulaması/
│   ├── README.md                               # Proje açıklaması
│   ├── geri_takip_etmeyenler.py                # Geri takip etmeyenleri bulan uygulama kodu
│   └── geri_takip_etmeyenler_Aciklamalari.ipynb # Notebook eğitim materyali
│
├── 📂 11-Stok-Takip-Uygulaması/
│   ├── README.md                               # Proje açıklaması
│   └── stok_takip.py                           # Stok takip uygulaması kodu
|
├── 📂 14-Basit-Keylogger-Yapimi-(Eğitim-Amacli)/
│   ├── README.md                               # Proje açıklaması
│   └── keylogger.py                            # Keylogger uygulaması kodu
|
├── 📂 19-Kripto-Botu-(Beta)/
│   ├── README.md                               # Proje açıklaması
│   ├── app.py                                  # Arayüz ve ana bot döngüsü
│   ├── bot.py                                  # API bağlantı testi
│   ├── btcturk_wrapper.py                      # BtcTurk API imzalama ve istek sarmalayıcısı
│   ├── endpoints.py                            # BtcTurk API endpoint tanımları
│   └── kripto_bot_Aciklamalari.ipynb           # Notebook eğitim materyali
│
├── 📂 21-Youtube-Video-İndirici/
│   ├── README.md                               # Proje açıklaması
│   ├── video_indir.py                          # YouTube video indirici kodu
│   └── video_indir_Aciklamalari.ipynb          # Notebook eğitim materyali
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
