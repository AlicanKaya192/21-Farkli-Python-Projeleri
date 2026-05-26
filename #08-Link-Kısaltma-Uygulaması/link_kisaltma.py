# GUI (Arayüz) oluşturmak için kullanılan kütüphane
import tkinter as tk
# Hata veya bilgi mesajları (pop-up) göstermek için
from tkinter import messagebox
# İnternet üzerinden veri çekmek ve göndermek (TinyURL API'sine bağlanmak) için
import requests
# Kısaltılan linki panoya (ctrl+c) kopyalamak için
import pyperclip


# 1. Aşama: Linki Kısaltan Fonksiyon
def shorten_url():
    # Kullanıcının arayüzdeki kutuya yapıştırdığı uzun linki alıyoruz
    long_url = entry.get()
    
    try:
        # TinyURL'nin ücretsiz API servisine uzun linkimizi gönderip cevabını (kısa linki) istiyoruz
        response = requests.get(f'http://tinyurl.com/api-create.php?url={long_url}')
        
        # Gelen cevabın içindeki metni (text) alıyoruz, bu bizim kısa linkimiz oluyor
        short_url = response.text
        
        # Arayüzdeki boş etiketin içine kısalan linkimizi yazdırıyoruz (Baştaki metin tam 17 karakterdir)
        result_label.config(text=f"Kısa URL Adresi: {short_url}")
        
        # Kısaltma başarılı olduğu için başlangıçta pasif (DISABLED) olan "Kopyala" butonunu aktif (NORMAL) hale getiriyoruz
        copy_button.config(state=tk.NORMAL)
    except Exception as e:
        # Eğer internet yoksa veya API çökerse hata mesajı gösteriyoruz
        messagebox.showerror("Hata", f"Link kısaltılırken hata oluştu: {e}")


# 2. Aşama: Kısa Linki Panoya Kopyalayan Fonksiyon
def copy_to_clipboard():
    # Ekranda yazan "Kısa URL Adresi: https://tinyurl..." metnini alıyoruz
    # Başındaki 17 karakterlik ("Kısa URL Adresi: ") kısmı kesip atarak [17:] sadece linki alıyoruz
    short_url = result_label.cget("text")[17:]
    
    # pyperclip kütüphanesi sayesinde linki panoya kopyalıyoruz (Sanki CTRL+C yapmışız gibi)
    pyperclip.copy(short_url)
    
    # Kullanıcıya kopyalandığına dair bir bilgi mesajı gösteriyoruz
    messagebox.showinfo("Kopyalandı", "Kısa URL Kopyalandı")


# 3. Aşama: Tkinter Arayüzünün (GUI) Oluşturulması
# Ana pencereyi oluşturuyoruz
app = tk.Tk()
app.title("Link Kısaltma") # Pencere başlığı

# Uzun linkin girileceği alanı belirten metin (Etiket)
label = tk.Label(app, text="Uzun Linki Giriniz: ")
label.pack(pady=10)

# Kullanıcının uzun linki yapıştıracağı giriş kutusu (Entry)
entry = tk.Entry(app, width=40)
entry.pack()

# "Kısalt" butonu, tıklandığında shorten_url fonksiyonunu çalıştırır
shorten_button = tk.Button(app, text="Kısalt", command=shorten_url)
shorten_button.pack()

# Kısaltılmış URL'nin ekranda gösterileceği etiket (Başlangıçta içi boş)
result_label = tk.Label(app, text="")
result_label.pack()

# "Kopyala" butonu, tıklandığında copy_to_clipboard fonksiyonunu çalıştırır
# state=tk.DISABLED diyerek başlangıçta tıklanamaz (pasif) yapıyoruz çünkü henüz kopyalanacak bir link yok
copy_button = tk.Button(app, text="Kopyala", command=copy_to_clipboard, state=tk.DISABLED)
copy_button.pack()

# Uygulamayı sonsuz döngüye sokarak çalışmasını ve beklemesini sağlıyoruz
app.mainloop()