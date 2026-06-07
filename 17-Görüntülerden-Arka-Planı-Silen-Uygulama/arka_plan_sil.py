# Gerekli Kütüphanelerin İçe Aktarılması
from tkinter import *  # Arayüz oluşturmak için standart GUI kütüphanesi
from tkinter import filedialog, messagebox  # Dosya seçme ve bilgi/hata mesaj kutuları
from rembg import remove  # Arka plan temizleme algoritması (U2-Net AI modeli kullanır)
from PIL import Image, ImageTk  # Görsel işleme kütüphanesi (Tkinter entegrasyonu için)
import os  # İşletim sistemi işlemleri (dosya yolları vb.) için

def arka_plan_kaldir():
    """
    Kullanıcıdan bir resim dosyası seçmesini isteyen,
    seçilen resmin arka planını yapay zeka yardımıyla silen
    ve temizlenmiş resmi kullanıcının belirteceği konuma PNG olarak kaydeden fonksiyon.
    """
    try:
        # 1. DOSYA SEÇME ADIMI
        # Kullanıcının bilgisayarından resim seçebilmesi için dosya diyalog penceresini açıyoruz
        dosya_yolu = filedialog.askopenfilename(
            title="Arka Planı Silinecek Resmi Seçin",
            filetypes=[
                ("Resim Dosyaları", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("Tüm Dosyalar", "*.*")
            ]
        )
        
        # Eğer kullanıcı dosya seçmeden pencereyi kapatırsa fonksiyonu sonlandırıyoruz
        if not dosya_yolu:
            return

        # 2. KAYIT YERİ SEÇME ADIMI
        # Temizlenen resmin nereye ve hangi adla kaydedileceğini kullanıcıya soruyoruz
        cikis_yolu = filedialog.asksaveasfilename(
            title="Temizlenmiş Resmi Kaydet",
            defaultextension=".png",  # Arka planı şeffaf (transparan) yapabilmek için PNG formatı şarttır
            filetypes=[("PNG Dosyası", "*.png")]
        )
        
        # Eğer kullanıcı kaydetmekten vazgeçerse işlemi sonlandırıyoruz
        if not cikis_yolu:
            return
            
        # 3. VERİ OKUMA VE MODEL İŞLEME ADIMI
        # Orijinal resmi ikili (binary) okuma modunda belleğe yüklüyoruz
        with open(dosya_yolu, 'rb') as i:
            girdi_veri = i.read()
            
        # rembg kütüphanesinin 'remove' fonksiyonunu kullanarak arka planı siliyoruz.
        # Bu işlem, arka planda ONNX Runtime üzerinde koşan u2net derin öğrenme modelini kullanır.
        cikti_veri = remove(girdi_veri)
        
        # 4. TİP DENETİMİ VE VERİ YAZMA ADIMI
        # Statik tip denetleyicileri (Pylance/Pyright gibi) 'remove' fonksiyonunun dönüş tipini
        # 'Image | bytes | ndarray' olarak gördüğünden, write() metoduna yazmadan önce
        # verinin kesinlikle 'bytes' tipinde olduğunu 'isinstance' ile doğruluyoruz.
        if isinstance(cikti_veri, bytes):
            with open(cikis_yolu, 'wb') as o:
                o.write(cikti_veri)
            # Kullanıcıya işlemin başarılı olduğunu bildiren mesaj gösteriyoruz
            messagebox.showinfo("Başarılı", "Arka plan başarıyla silindi ve yeni resim kaydedildi!")
        else:
            # Beklenmeyen bir veri tipi dönmesi durumunda kullanıcıyı uyarıyoruz
            messagebox.showerror("Hata", "Görüntü işleme sırasında beklenmeyen bir veri formatı döndürüldü.")
            
    except Exception as e:
        # İşlem sırasında oluşabilecek her türlü hatayı yakalayıp kullanıcıya gösteriyoruz
        messagebox.showerror("Hata", f"İşlem sırasında bir hata oluştu:\n{str(e)}")

# ==========================================
# TKINTER ARAYÜZÜNÜN OLUŞTURULMASI
# ==========================================

# Ana uygulama penceresini tanımlıyoruz
pencere = Tk()
pencere.title("Resim Arka Planı Silici")  # Pencere başlığı
pencere.geometry("400x200")  # Pencere genişlik ve yüksekliği
pencere.configure(bg="#f4f4f9")  # Arka plan rengi (Açık gri/mavi ton)

# Başlık Etiketi (Uygulamanın ana başlığı)
baslik = Label(
    pencere, 
    text="Arka Plan Silici", 
    font=("Helvetica", 16, "bold"), 
    bg="#f4f4f9", 
    fg="#333333"
)
baslik.pack(pady=(25, 5))  # Dikeyde üstten 25px, alttan 5px boşluk bırakıyoruz

# Açıklama Etiketi (Kullanıcıya yönerge verir)
aciklama = Label(
    pencere, 
    text="Resminizi seçin, arka plan otomatik olarak temizlenecektir.", 
    font=("Helvetica", 10), 
    bg="#f4f4f9", 
    fg="#666666"
)
aciklama.pack(pady=(0, 20))  # Alttan 20px boşluk

# İşlemi Başlatan Buton
buton = Button(
    pencere, 
    text="Resim Seç ve Arka Planı Sil", 
    command=arka_plan_kaldir,  # Tıklandığında yukarıda tanımladığımız fonksiyonu çalıştırır
    font=("Helvetica", 10, "bold"), 
    bg="#4a90e2",  # Butonun arka plan rengi (Mavi)
    fg="white",  # Yazı rengi
    activebackground="#357abd",  # Butona basıldığındaki arka plan rengi
    activeforeground="white",
    bd=0,  # Düz buton tasarımı için kenarlıkları kaldırıyoruz
    padx=15, 
    pady=8,
    cursor="hand2"  # İmlecin butonun üzerine geldiğinde el işaretine dönüşmesini sağlar
)
buton.pack()

# Uygulama penceresini kullanıcı kapatana kadar açık tutan ana döngü
pencere.mainloop()