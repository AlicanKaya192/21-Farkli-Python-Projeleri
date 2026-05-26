from tkinter import Label, Tk # Arayüz için gerekli sınıflar
import time # Anlık saat verisi için

def digital_clock():
    # Saati al ve etikete yaz
    time_live = time.strftime("%H:%M:%S")
    label.config(text=time_live)

    # Tarihi al ve etikete yaz
    date_info = time.strftime("%d %B %Y")
    date_label.config(text=date_info)

    # Her 200ms'de bir bu fonksiyonu tekrar çalıştır (canlı saat)
    label.after(200, digital_clock)

# Ana pencereyi oluştur ve ayarlarını yap
app_window = Tk()
app_window.title("Dijital Saat")
app_window.geometry("350x300")
app_window.resizable(False, False) # Boyutlandırmayı engelle
app_window.configure(bg="black") # Arka planı siyah yap

# Ortak tasarım ayarları
text_font = ("Boulder", 36, 'bold')
background = "black"
foreground = "White"
border_width = 20

# Saat etiketini oluştur ve yerleştir
label = Label(app_window, font=text_font, bg=background, fg=foreground, border=border_width)
label.grid(row=0, column=1, padx=10, pady=10)

# Tarih etiketini oluştur ve yerleştir
date_label = Label(app_window, font=text_font, bg=background, fg=foreground, border=border_width)
date_label.grid(row=1, column=1, padx=10, pady=10)

# Saati başlat
digital_clock()

# Uygulamayı dinleme modunda açık tut
app_window.mainloop()