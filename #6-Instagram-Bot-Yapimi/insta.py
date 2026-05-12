import instaloader # Instagram verilerini çekmek için kullanılan kütüphane
import tkinter as tk # GUI (Arayüz) oluşturmak için kullanılan kütüphane
from tkinter import messagebox, ttk # Hata ve bilgi mesajları göstermek için


def download_post():
    # Kullanıcıdan arayüzdeki giriş alanlarından verileri alıyoruz
    username = entry_username.get() # İndirilecek hesabın kullanıcı adı
    ig_user = entry_iguser.get() # Kendi Instagram kullanıcı adımız
    ig_pass = entry_igpass.get() # Kendi Instagram şifremiz

    try:
        # Instaloader botunu başlatıyoruz
        bot = instaloader.Instaloader()
        # Kendi hesabımıza giriş yapıyoruz (Gizli profillerdeki gönderileri çekebilmek için gereklidir)
        bot.login(ig_user, ig_pass)
        # Hedef profilin bilgilerini alıyoruz
        profile = instaloader.Profile.from_username(bot.context, username)
        # Hedef profilin gönderilerini çekiyoruz
        posts = profile.get_posts()

        # Her bir gönderiyi sırayla indiriyoruz
        for index, post in enumerate(posts, 1):
            bot.download_post(post, target=f"{profile.username}_{index}") # Gönderiyi hedef klasöre kaydediyoruz

        # İşlem başarılı olursa bilgi mesajı gösteriyoruz
        messagebox.showinfo("Başarılı", "Gönderiler İndirildi")
    except Exception as e:
        # Hata oluşursa hata mesajı gösteriyoruz
        messagebox.showerror("Hata", str(e))


# Ana pencereyi oluşturuyoruz
root = tk.Tk()
root.title("Instagram Gönderi İndirici") # Pencere başlığı
root.geometry("500x450") # Pencere boyutu
root.resizable(False, False) # Pencerenin boyutunun değiştirilmesini engelliyoruz

# İndirilecek Kullanıcı Adı için etiket ve giriş alanı
tk.Label(root, text="İndirilecek Kullanıcı Adı:").pack(pady=5)
entry_username = tk.Entry(root, width=30)
entry_username.pack()

# Kendi Instagram Kullanıcı Adımız için etiket ve giriş alanı
tk.Label(root, text="Kendi Instagram Kullanıcı Adın:").pack(pady=5)
entry_iguser = tk.Entry(root, width=30)
entry_iguser.pack()

# Kendi Instagram Şifremiz için etiket ve giriş alanı
tk.Label(root, text="Kendi Instagram Şifren:").pack(pady=5)
entry_igpass = tk.Entry(root, show="*", width=30) # Şifrenin görünmemesi için show="*" kullanıyoruz
entry_igpass.pack()

# İndirme işlemini başlatacak buton
tk.Button(root, text="Bilgileri İndir", command=download_post, width=20).pack(pady=10)

# ─── Uyarı Tablosu ───────────────────────────────────────────────
# Dikkat edilmesi gerekenler başlığı
tk.Label(root, text="⚠️ Dikkat Edilmesi Gerekenler",
         font=("Arial", 10, "bold"), fg="orange").pack(pady=(5, 2))

# Uyarı tablosunu içerecek çerçeve (frame)
frame_table = tk.Frame(root, bd=1, relief="solid")
frame_table.pack(padx=15, pady=5, fill="x")

# Tablo başlıkları ve içerik verileri
headers = ["Durum", "Açıklama"]
rows = [
    ("2FA",            "İki faktörlü doğrulama açıksa bot.two_factor_login(code) gerekir"),
    ("Rate Limit",     "Çok fazla indirme yaparsan hesabın geçici bloklanabilir"),
    ("Oturum Kaydetme","save_session_to_file() ile tekrar giriş yapmaktan kaçınabilirsin"),
    ("Gizli Profil",   "Hedef profil gizliyse ve takip etmiyorsan yine hata alırsın"),
]

# Tablonun başlık satırını oluşturuyoruz
for col, h in enumerate(headers):
    tk.Label(frame_table, text=h, font=("Arial", 9, "bold"),
             bg="#f0f0f0", relief="ridge", padx=6, pady=4,
             anchor="w", width=18 if col == 0 else 42
             ).grid(row=0, column=col, sticky="nsew")

# Tablonun veri satırlarını oluşturuyoruz
for row_i, (durum, aciklama) in enumerate(rows, start=1):
    bg = "#ffffff" if row_i % 2 == 0 else "#fafafa" # Satır renklerini farklılaştırıyoruz (Zebra deseni)
    tk.Label(frame_table, text=durum, font=("Arial", 9),
             bg=bg, relief="ridge", padx=6, pady=4,
             anchor="w", width=18
             ).grid(row=row_i, column=0, sticky="nsew")
    tk.Label(frame_table, text=aciklama, font=("Arial", 9),
             bg=bg, relief="ridge", padx=6, pady=4,
             anchor="w", width=42, wraplength=300
             ).grid(row=row_i, column=1, sticky="nsew")

# Uygulamayı sonsuz döngüye sokarak çalışmasını sağlıyoruz
root.mainloop()