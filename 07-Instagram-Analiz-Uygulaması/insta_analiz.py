# Instagram verilerini çekmek için kullanılan kütüphane
import instaloader
# GUI (Arayüz) oluşturmak için kullanılan kütüphane
import tkinter as tk
# Hata mesajları ve gelişmiş tablo (Treeview) arayüzü için
from tkinter import ttk, messagebox


# 1. Aşama: Kullanıcı Bilgilerini Çeken Fonksiyon
def get_user_info(username):
    # Instaloader botunu başlatıyoruz
    bot = instaloader.Instaloader()
    
    try:
        # Hedef profilin bilgilerini Instagram'dan çekiyoruz
        profile = instaloader.Profile.from_username(bot.context, username)
    except instaloader.exceptions.ProfileNotExistsException:
        # Eğer böyle bir kullanıcı yoksa uyarı mesajı döndürüyoruz
        return "Girdiğiniz kullanıcı bulunamadı."
    except Exception as e:
        # Diğer olası hataları yakalıyoruz
        return f"Bir hata oluştu: {e}"

    # Çektiğimiz bilgileri bir sözlük (dictionary) içinde topluyoruz
    user_info = {
        "Username" : profile.username,          # Kullanıcı adı
        "Followers" : profile.followers,        # Takipçi sayısı
        "Followees" : profile.followees,        # Takip edilen sayısı
        "Post Count" : profile.mediacount,      # Toplam gönderi sayısı
        "Last Post Date" : get_last_post_date(profile) # Son gönderi tarihi (Aşağıdaki fonksiyondan gelir)
    }

    # Toplanan bilgileri geri döndürüyoruz
    return user_info


# 2. Aşama: Kullanıcının Son Gönderi Tarihini Çeken Fonksiyon
def get_last_post_date(profile):
    last_post = None

    # Profildeki tüm gönderileri döngüye alıyoruz
    for post in profile.get_posts():
        # İlk gönderiyi veya tarihi daha yeni olan bir gönderiyi last_post olarak güncelliyoruz
        if not last_post or post.date_utc > last_post.date_utc:
            last_post = post
            
    # Eğer hesabın en az 1 gönderisi varsa tarihini YYYY-MM-DD HH:MM:SS formatında döndürüyoruz
    if last_post:
        return last_post.date_utc.strftime("%Y-%m-%d %H:%M:%S")
    
    # Hiç gönderisi yoksa bu mesajı döndürüyoruz
    return "Gönderi Yok"


# 3. Aşama: Kullanıcı Bilgilerini Arayüzde (Tabloda) Gösterme
def show_user():
    # Arayüzdeki giriş kutusundan (Entry) yazılan kullanıcı adını alıyoruz
    username = entry_username.get()
    
    # Kullanıcı bilgilerini çekmek için ana fonksiyonumuzu çalıştırıyoruz
    user_info = get_user_info(username)

    # Eğer fonksiyonumuz başarılı olup bize bir Sözlük (dict) döndürdüyse
    if isinstance(user_info, dict):
        # Tablodaki (Treeview) eski verileri temizliyoruz
        for widget in tree.get_children():
            tree.delete(widget)
            
        # Tabloya yeni çekilen kullanıcı verilerini ekliyoruz
        tree.insert("","end",values=(
            user_info["Username"],
            user_info["Followers"],
            user_info["Followees"],
            user_info["Post Count"],
            user_info["Last Post Date"]
        ))
    else:
        # Eğer bir sözlük dönmediyse (hata mesajı string döndüyse), ekranda hata kutusu gösteriyoruz
        messagebox.showerror("Hata", user_info)


# 4. Aşama: Tkinter Arayüzünün (GUI) Oluşturulması
# Ana pencereyi oluşturuyoruz
root = tk.Tk()
root.title("Instagram Kullanıcı Bilgi Görüntüleyicisi") # Pencere başlığı

# Arayüzü daha düzenli tutmak için bir çerçeve (Frame) ekliyoruz
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Kullanıcı Adı Etiketi
label = tk.Label(frame, text="Kullanıcı Adı: ")
label.grid(row=0, column=0, padx=5, pady=5)

# Kullanıcı adı yazılacak giriş kutusu
entry_username = tk.Entry(frame)
entry_username.grid(row=0, column=1, padx=5, pady=5)

# Arama işlemini tetikleyecek "Bilgileri Görüntüle" butonu
search_button = tk.Button(frame, text="Bilgileri Görüntüle", command=show_user)
search_button.grid(row=0, column=2, padx=5, pady=5)

# Bilgilerin gösterileceği tablo (Treeview) oluşturuluyor ve sütunlar belirleniyor
tree = ttk.Treeview(root, columns=("Username","Followers","Followees","Post Count","Last Post Date"))

# Tablonun başlıkları isimlendiriliyor
tree.heading("Username",text="Kullanıcı adı")
tree.heading("Followers", text="Takipçiler")
tree.heading("Followees",text="Takip Edilenler")
tree.heading("Post Count", text="Gönderi Sayısı")
tree.heading("Last Post Date",text="Son Gönderi Tarihi")

# Tablo ekrana yerleştiriliyor
tree.pack(padx=20, pady=20)

# Uygulamayı sonsuz döngüye sokarak çalışmasını ve beklemesini sağlıyoruz
root.mainloop()