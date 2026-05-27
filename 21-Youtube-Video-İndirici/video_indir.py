import tkinter as tk           # Tkinter: Python'ın standart GUI (Arayüz) kütüphanesidir.
from tkinter import ttk, messagebox  # Gelişmiş widget'lar (ttk) ve mesaj pencereleri (messagebox).
import os                      # Dosya ve dizin işlemleri için standart kütüphane.
import re                      # Düzenli ifadeler (Regex) ile dosya adlarındaki geçersiz karakterleri temizlemek için.
import io                      # Bellek içi bayt akışları (thumbnail görselini indirmek ve açmak için).
import shutil                  # FFmpeg'in sistem PATH'inde olup olmadığını kontrol etmek için.
import threading               # Arayüzün donmasını engellemek amacıyla ağ ve indirme işlemlerini arka planda çalıştırmak için.
import requests                # Thumbnail resmini web üzerinden indirmek için HTTP istek kütüphanesi.
from PIL import Image, ImageTk  # Pillow: Resim işleme ve Tkinter'da resim göstermek için.
from yt_dlp import YoutubeDL     # yt-dlp: YouTube videolarını ve seslerini indirmek için gelişmiş motor.

# ffmpeg.exe kütüphanesinin bulunabileceği varsayılan konum (kullanıcı değiştirebilir)
FFMPEG_LOCATION = r"C:\ffmpeg\bin"

def get_ffmpeg_path() -> str:
    """
    Sistemde FFmpeg yazılımının kurulu olup olmadığını ve yolunu kontrol eder.
    Sistem PATH'inde varsa None döner (yt-dlp otomatik algılar).
    Yaygın Windows dizinlerini kontrol ederek bir yol bulursa o dizini döner.
    """
    if shutil.which("ffmpeg"):
        return None  # yt-dlp sistem yolundakini otomatik kullanır.
        
    # Windows için yaygın FFmpeg kurulum yolları
    common_paths = [
        FFMPEG_LOCATION,
        r"C:\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin",
        r"C:\Program Files (x86)\ffmpeg\bin",
    ]
    for path in common_paths:
        if os.path.exists(os.path.join(path, "ffmpeg.exe")):
            return path
    return None

def sanitize_filename(name: str) -> str:
    r"""
    Dosya adlarında işletim sistemleri tarafından yasaklanmış olan
    \ / * ? : " < > | karakterlerini temizler.
    """
    return re.sub(r'[\\/*?:"<>|]', "", name)


class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video & Ses İndirici")
        self.root.geometry("680x600")
        self.root.configure(bg="#f2f2f7")  # iOS tarzı açık gri arka plan
        self.info_dict = None              # İndirilecek videonun metaverilerini tutar
        self.thumbnail_img = None          # Tkinter'da garbage collector'a takılmaması için resim nesnesi
        self.create_ui()

    def create_ui(self):
        """Uygulamanın grafiksel arayüzünü (GUI) oluşturur ve stillendirir."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#f2f2f7")
        style.configure("TLabel", background="#f2f2f7", foreground="#1c1c1e", font=("Helvetica", 11))
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))
        style.configure("TButton", font=("Helvetica", 11, "bold"), foreground="#ffffff",
                        background="#007aff", padding=6)
        style.map("TButton", background=[("active", "#005bb5")])
        style.configure("TProgressbar", troughcolor="#d1d1d6", background="#007aff", thickness=8)

        # Ana Taşıyıcı Çerçeve (Frame)
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(expand=True, fill="both")

        # Uygulama Başlığı
        ttk.Label(main_frame, text="YouTube Video & Ses İndirme Botu", style="Header.TLabel").pack(pady=(0,20))

        # URL Giriş Alanı
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill="x", pady=(0,10))
        ttk.Label(url_frame, text="YouTube Linki:", style="TLabel").pack(side="left")
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=45)
        self.url_entry.pack(side="left", padx=10)
        self.fetch_button = ttk.Button(url_frame, text="Bilgileri Getir", command=self.fetch_info)
        self.fetch_button.pack(side="left")

        # Bilgi ve Önizleme Alanı
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill="x", pady=(10,10))
        self.title_label = ttk.Label(info_frame, text="Başlık: Bekleniyor...", font=("Helvetica", 12, "bold"), wraplength=600)
        self.title_label.pack(anchor="w", pady=(0, 10))
        self.thumbnail_label = ttk.Label(info_frame, text="Önizleme resmi için yukarıdaki butona tıklayın.", anchor="center")
        self.thumbnail_label.pack(pady=10)

        # İndirme Seçenekleri (Tür ve Çözünürlük)
        option_frame = ttk.Frame(main_frame)
        option_frame.pack(fill="x", pady=(10,10))
        self.download_option = tk.StringVar(value="video")
        ttk.Label(option_frame, text="İndirilecek Tür:", style="TLabel").pack(side="left")
        
        # Radyo Butonları
        self.video_radio = ttk.Radiobutton(option_frame, text="Video (MP4)", variable=self.download_option, value="video", command=self.toggle_resolution_combobox)
        self.video_radio.pack(side="left", padx=10)
        self.audio_radio = ttk.Radiobutton(option_frame, text="Ses (MP3)", variable=self.download_option, value="audio", command=self.toggle_resolution_combobox)
        self.audio_radio.pack(side="left", padx=10)
        
        # Çözünürlük Seçim Kutusu (Combobox)
        self.res_label = ttk.Label(option_frame, text="Çözünürlük:")
        self.res_label.pack(side="left", padx=(20,0))
        self.resolution_var = tk.StringVar(value="En İyi")
        self.res_combobox = ttk.Combobox(option_frame, textvariable=self.resolution_var, values=["En İyi", "1080p", "720p", "480p"], state="readonly", width=8)
        self.res_combobox.pack(side="left", padx=10)

        # Butonlar
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(15,10))
        self.download_button = ttk.Button(button_frame, text="İndirmeyi Başlat", command=self.download_media, state="disabled")
        self.download_button.pack(side="left", padx=10)
        self.open_folder_button = ttk.Button(button_frame, text="İndirilenleri Aç", command=self.open_download_folder)
        self.open_folder_button.pack(side="left")

        # Durum ve İlerleme (Progress) Göstergeleri
        self.status_label = ttk.Label(main_frame, text="Kullanıma hazır.", font=("Helvetica", 10, "italic"))
        self.status_label.pack(pady=(10,5))
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=500, mode="determinate", variable=self.progress_var)
        self.progress_bar.pack()

    def toggle_resolution_combobox(self):
        """Ses veya Video türü seçildiğinde çözünürlük kutusunu aktif veya pasif yapar."""
        if self.download_option.get() == "audio":
            self.res_combobox.config(state="disabled")
        else:
            self.res_combobox.config(state="readonly")

    def fetch_info(self):
        """Girilen YouTube adresinden video bilgilerini arka planda (thread) sorgular."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Hata", "Lütfen geçerli bir YouTube linki girin.")
            return

        self.status_label.config(text="Video bilgileri alınıyor, lütfen bekleyin...")
        self.fetch_button.config(state="disabled")
        self.download_button.config(state="disabled")
        
        # Arayüzün donmasını engellemek için işlemi arka planda (Thread) çalıştırıyoruz
        def run():
            try:
                opts = {'quiet': True, 'skip_download': True}
                ffmpeg_path = get_ffmpeg_path()
                if ffmpeg_path:
                    opts['ffmpeg_location'] = ffmpeg_path
                
                with YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                
                # İşlem başarılı ise ana thread'e geçerek arayüzü güncelle
                self.root.after(0, lambda: self.on_fetch_success(info))
            except Exception as e:
                # Hata durumunda kullanıcıyı bilgilendir
                self.root.after(0, lambda: self.on_fetch_error(e))

        threading.Thread(target=run, daemon=True).start()

    def on_fetch_success(self, info):
        """Bilgi çekme başarılı olduğunda çalışan callback fonksiyonu."""
        self.info_dict = info
        title = info.get('title', 'Bilinmiyor')
        self.title_label.config(text=f"Başlık: {title}")
        self.fetch_button.config(state="normal")
        self.download_button.config(state="normal")
        self.status_label.config(text="Bilgiler başarıyla alındı.")

        # Thumbnail resmini indirip yerleştirmek için de arka plan thread'i kullanıyoruz
        thumb_url = info.get('thumbnail')
        if thumb_url:
            self.thumbnail_label.config(text="Resim yükleniyor...")
            def load_thumbnail():
                try:
                    response = requests.get(thumb_url, timeout=10)
                    img = Image.open(io.BytesIO(response.content)).resize((320, 180), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.root.after(0, lambda: self.update_thumbnail(photo))
                except:
                    self.root.after(0, lambda: self.thumbnail_label.config(text="Önizleme resmi yüklenemedi."))
            threading.Thread(target=load_thumbnail, daemon=True).start()
        else:
            self.thumbnail_label.config(text="Önizleme resmi yok.")

    def update_thumbnail(self, photo):
        """Önizleme resmini günceller."""
        self.thumbnail_img = photo
        self.thumbnail_label.config(image=self.thumbnail_img, text="")

    def on_fetch_error(self, err):
        """Bilgi çekme başarısız olduğunda çalışan callback fonksiyonu."""
        self.fetch_button.config(state="normal")
        self.status_label.config(text="Bilgiler alınamadı.")
        messagebox.showerror("Hata", f"Video bilgileri alınırken hata oluştu:\n{err}")

    def download_media(self):
        """Kullanıcının seçtiği ayarlara göre video veya ses dosyasını arka planda indirir."""
        if not self.info_dict:
            messagebox.showerror("Hata", "Önce 'Bilgileri Getir' butonuna basmalısınız.")
            return

        title = sanitize_filename(self.info_dict.get('title', 'video'))
        dtype = self.download_option.get()
        resolution = self.resolution_var.get()
        
        # FFmpeg varlığı kontrolü
        ffmpeg_path = get_ffmpeg_path()
        has_ffmpeg = (ffmpeg_path is not None) or (shutil.which("ffmpeg") is not None)

        if not has_ffmpeg:
            # Ses indirirken veya en iyi kalite harici spesifik kalite seçildiğinde FFmpeg gerekir
            if dtype == 'audio' or resolution != 'En İyi':
                confirm = messagebox.askyesno(
                    "FFmpeg Bulunamadı",
                    "Sisteminizde FFmpeg kurulu bulunamadı.\n\n"
                    "FFmpeg olmadan yüksek çözünürlüklü video birleştirme ve MP3 dönüştürme işlemleri başarısız olabilir.\n"
                    "Yine de indirmeye devam etmek istiyor musunuz? (Olası en iyi kalitede tek parça dosya indirilecektir.)"
                )
                if not confirm:
                    return

        # Format ve postprocessor ayarlarını yapıyoruz
        if dtype == 'video':
            if resolution == 'En İyi':
                if not has_ffmpeg:
                    # FFmpeg yoksa, birleştirmeye ihtiyaç duymayan en iyi tek parça formatı indir
                    fmt = 'best[ext=mp4]/best'
                else:
                    # En iyi görüntü ve en iyi sesi ayrı ayrı indirip birleştir
                    fmt = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'
            else:
                height = resolution.replace('p', '')
                if not has_ffmpeg:
                    # Çözünürlük sınırlı, birleştirme gerektirmeyen tek dosyayı indir
                    fmt = f'best[height<={height}][ext=mp4]/best'
                else:
                    # Çözünürlük sınırlı, ayrı görüntü ve ses indirip birleştir
                    fmt = f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best'
            
            out = f"{title}.mp4"
            post = []
        else:
            if not has_ffmpeg:
                # FFmpeg yoksa MP3'e dönüştüremeyiz, ses dosyasını ham formatında (genelde .m4a) indiririz
                fmt = 'bestaudio'
                out = f"{title}.m4a"
                post = []
                messagebox.showwarning("Bilgi", "FFmpeg kurulu olmadığından dönüştürme yapılamadı. Dosya orijinal ses formatında (.m4a) indirilecektir.")
            else:
                fmt = 'bestaudio[ext=m4a]/bestaudio'
                out = f"{title}.mp3"
                post = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]

        opts = {
            'format': fmt,
            'outtmpl': out,
            'progress_hooks': [self.progress_hook],
            'postprocessors': post,
            'quiet': True,
        }
        if ffmpeg_path:
            opts['ffmpeg_location'] = ffmpeg_path

        self.status_label.config(text="İndirme işlemi başlatılıyor...")
        self.progress_var.set(0)
        self.download_button.config(state="disabled")
        self.fetch_button.config(state="disabled")

        # İndirme işlemini arka planda (Thread) çalıştırıyoruz
        def run():
            try:
                with YoutubeDL(opts) as ydl:
                    ydl.download([self.info_dict['webpage_url']])
                self.root.after(0, lambda: self.on_download_success(out))
            except Exception as e:
                self.root.after(0, lambda: self.on_download_error(e))

        threading.Thread(target=run, daemon=True).start()

    def on_download_success(self, out_file):
        """İndirme işlemi başarıyla bittiğinde çalışan callback."""
        self.status_label.config(text=f"İndirme tamamlandı: {out_file}")
        self.download_button.config(state="normal")
        self.fetch_button.config(state="normal")
        messagebox.showinfo("Başarılı", f"Dosya başarıyla indirildi:\n{out_file}")

    def on_download_error(self, err):
        """İndirme işlemi başarısız olduğunda çalışan callback."""
        self.status_label.config(text="İndirme başarısız oldu.")
        self.download_button.config(state="normal")
        self.fetch_button.config(state="normal")
        messagebox.showerror("Hata", f"İndirme sırasında bir hata oluştu:\n{err}")

    def progress_hook(self, d):
        """İndirme ilerleme durumunu yt-dlp üzerinden yakalayıp GUI'ye ileten kanca (hook)."""
        if d['status'] == 'downloading':
            try:
                # Yüzde değerini dize içinden ayıkla
                p = float(d.get('_percent_str', '').replace('%', '').strip())
            except:
                p = 0
            
            speed = d.get('_speed_str', 'Bilinmiyor')
            eta = d.get('eta', 0)
            
            # Thread-safe şekilde arayüzü güncellemek için root.after kullanıyoruz
            self.root.after(0, lambda: self.update_progress(p, speed, eta))
        elif d['status'] == 'finished':
            self.root.after(0, self.on_download_finished_hook)

    def update_progress(self, percent, speed, eta):
        """Arayüzdeki ilerleme çubuğunu ve durum etiketini günceller."""
        self.progress_var.set(percent)
        self.status_label.config(text=f"İndiriliyor: %{percent:.1f} | Hız: {speed} | Kalan Süre: {eta} sn")

    def on_download_finished_hook(self):
        """İndirme bittiğinde ve dönüştürme/birleştirme sürerken gösterilen kanca."""
        self.progress_var.set(100)
        self.status_label.config(text="İndirme tamamlandı, dosya birleştiriliyor/işleniyor...")

    def open_download_folder(self):
        """İndirilen dosyaların kaydedildiği mevcut çalışma dizinini dosya gezgininde açar."""
        try:
            os.startfile(os.getcwd())
        except:
            import subprocess
            subprocess.Popen(['xdg-open', os.getcwd()])


def main():
    root = tk.Tk()
    YouTubeDownloaderApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
