# 📂 Proje #12 — İnstagram Etkileşim Saatini Analiz Eden Uygulama

![Instagram Analiz Excel Çıktısı](./public/Ekran%20görüntüsü%202026-06-01%20232604.png)

Belirtilen bir Instagram hesabının gönderilerini çekerek hangi gün, saat ve ayda paylaşım yapıldığını analiz eden, sonuçları Excel dosyasına yazıp koşullu biçimlendirme uygulayan uygulamadır.

## 📄 Klasör İçeriği
- `instagram_etkileşim_saat.py`: Instagram API'sinden veri çekip Excel raporu üreten ana Python kodu.
- `instagram_etkileşim_saat_Aciklamalari.ipynb`: Projenin yapısını ve çalışma mantığını adım adım açıklayan Jupyter Notebook eğitim dosyası.
- `public/`: Örnek Excel çıktısının ekran görüntüsünü barındıran klasör.

## 📦 Gerekli Kütüphaneler
- `instaloader`: Instagram profil verilerini çekmek için.
- `pandas`: Çekilen verileri tablo yapısına dönüştürmek için.
- `openpyxl`: Excel dosyasına yazma ve koşullu biçimlendirme uygulamak için.

## 🚀 Çalıştırma
```bash
python instagram_etkileşim_saat.py
```
