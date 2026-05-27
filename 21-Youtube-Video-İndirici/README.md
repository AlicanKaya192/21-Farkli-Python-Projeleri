# 📂 Proje #21 — YouTube Video & Ses İndirme Botu

yt-dlp motoru kullanarak YouTube videolarını istenilen çözünürlükte (1080p, 720p vb. MP4) veya ses formatında (MP3) hızlı ve donmasız bir şekilde bilgisayara indiren Tkinter masaüstü botudur.

## 📄 Klasör İçeriği
- `video_indir.py`: Çoklu iş parçacığı (threading) ve FFmpeg fallback desteğine sahip ana program kodu.
- `video_indir_Aciklamalari.ipynb`: Arayüz tasarımı, threading mimarisi ve indirme mantığını açıklayan detaylı notebook rehberi.

## 📦 Gerekli Kütüphaneler
- `yt-dlp`
- `requests`
- `Pillow`

## 🚀 Çalıştırma
```bash
python video_indir.py
```
