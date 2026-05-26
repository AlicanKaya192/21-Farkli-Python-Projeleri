import tkinter as tk # Arayüz penceresi oluşturmak için temel tkinter kütüphanesini içe aktarır
from tkinter import ttk, filedialog, messagebox, StringVar # Temalı bileşenleri ve işletim sistemi iletişim kutularını içe aktarır
import os # Dosya arama ve dizin birleştirme işlemleri için os modülünü içe aktarır
from bs4 import BeautifulSoup # HTML dosyalarını taramak ve içindeki verileri ayıklamak için BeautifulSoup nesnesini içe aktarır
from fpdf import FPDF # Sonuçları PDF formatında rapor olarak kaydetmek için fpdf kütüphanesini içe aktarır
import threading # Web scraping ve dosya okuma işlemleri sırasında arayüzün donmasını engellemek için threading kütüphanesini içe aktarır
import webbrowser # Kullanıcı adlarına tıklandığında Instagram profillerini tarayıcıda açmak için webbrowser kütüphanesini içe aktarır
import pandas as pd # Takipçileri Excel formatında raporlamak için pandas kütüphanesini içe aktarır

# Global Değişkenler
followers_list = [] # HTML dosyalarından ayıklanan tüm takipçilerin listesini saklar
active_list = [] # Tabloda o an aktif olarak listelenen (tüm takipçiler veya geri takip etmeyenler) verinin kopyasını tutar. Arama ve dosya kaydetme işlemleri bu liste üzerinden yapılır.
file_paths = [] # Kullanıcının seçtiği veya otomatik olarak dizinde bulunan followers.html dosya yolları

def update_table(data):
    """
    Parametre olarak aldığı veri listesini (data) temizledikten sonra Treeview tablosuna ekler.
    Her satıra bir sıra numarası (index) ve kullanıcı adı yerleştirir.
    """
    table.delete(*table.get_children()) # Tablonun içerisindeki mevcut tüm verileri temizler
    for index, item in enumerate(data, start=1):
        table.insert("", "end", values=(index, item)) # Sıra numarası ve ismi tabloya ekler

def open_files_and_show_followers():
    """
    Uygulama scripti ile aynı dizinde bulunan 'followers_1.html'den 'followers_99.html'ye kadar olan dosyaları
    otomatik olarak tarar ve bulduklarını listeye ekleyerek arayüzde gösterir.
    """
    global file_paths
    file_paths = []
    
    # Çalıştırılan python dosyasının (scriptinin) klasör dizinini tam yol olarak alır
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # followers_1.html, followers_2.html ... followers_99.html dosyalarını otomatik arar
    for i in range(1, 100):
        # Dosya yollarını işletim sistemine uygun şekilde birleştirir
        file_path = os.path.join(script_dir, f"followers_{i}.html")
        if os.path.exists(file_path):
            file_paths.append(file_path)
        else:
            break # Seri bozulduğunda (dosya bulunamadığında) aramayı durdurur
    
    if not file_paths:
        messagebox.showwarning("Uyarı", "followers_X.html dosyası bulunamadı!")
        return
    
    # Arayüzdeki seçili dosyalar listesini (listbox) günceller
    file_listbox.delete(0, tk.END)
    for file_path in file_paths:
        # Sadece dosya adını (örn: followers_1.html) listeler
        file_listbox.insert(tk.END, os.path.basename(file_path))
        
    # Otomatik olarak takipçileri yükleme işlemini arka planda tetikler
    show_all_followers()

def open_file_and_show_followers():
    """
    Kullanıcıya dosya seçme penceresi açarak elle HTML dosyalarını seçtirir ve yollarını kaydeder.
    """
    global file_paths
    # file_dialog ile kullanıcının çoklu HTML dosyası seçmesini sağlar
    file_paths = filedialog.askopenfilenames(title="Dosya Seç", filetypes=[("HTML Files", "*.html")])
    if not file_paths:
        return # Kullanıcı seçim yapmadan kapattıysa işlem yapmaz
        
    file_listbox.delete(0, tk.END)
    for file_path in file_paths:
        file_listbox.insert(tk.END, os.path.basename(file_path))
        
    # Takipçileri yükleme işlemini arka planda başlatır
    show_all_followers()

def show_all_followers():
    """
    Arayüzün donmaması için takipçi dosyası okuma işlemini bir arka plan iş parçacığı (Thread) olarak başlatır.
    """
    if not file_paths:
        messagebox.showwarning("Uyarı", "Lütfen önce dosyaları seçin veya otomatik çekmeyi deneyin.")
        return
    # show_followers fonksiyonunu arka planda çalıştırmak için Thread tanımlar ve başlatır
    t = threading.Thread(target=show_followers, args=(file_paths,))
    t.start()

def show_followers(file_paths):
    """
    Belirtilen HTML dosyalarını okuyarak içindeki takipçi isimlerini BeautifulSoup ile ayıklar.
    """
    global active_list
    followers_list.clear()
    progress_label.config(text="Takipçiler yükleniyor...")
    
    for file_path in file_paths:
        try:
            # HTML dosyasını utf-8 formatında okur
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
            # HTML etiketlerini ayrıştırır
            soup = BeautifulSoup(html_content, "html.parser")
            # Instagram HTML yapısında profil linkleri genelde target="_blank" olan a etiketleridir
            names = [item.get_text() for item in soup.find_all("a", target="_blank")]
            followers_list.extend(names)
        except Exception as e:
            messagebox.showerror("Hata", f"{os.path.basename(file_path)} dosyası okunurken hata oluştu:\n{e}")
            progress_label.config(text="Hata oluştu.")
            return

    # Aktif listeyi takipçiler listesi olarak kopyalar
    active_list = list(followers_list)
    # Arayüzdeki tabloyu günceller
    update_table(active_list)
    progress_label.config(text="Takipçiler başarıyla yüklendi.")
    show_followers_count() # Takipçi sayısını gösteren kutuyu açar

def show_followers_count():
    """Toplam takipçi sayısını bilgi mesajı olarak kullanıcıya gösterir."""
    if followers_list:
        messagebox.showinfo("Toplam Takipçi Sayısı", f"Toplam Takipçi Sayısı: {len(followers_list)}")
    else:
        messagebox.showwarning("Uyarı", "Henüz takipçi bulunmamaktadır.")

def show_non_followers():
    """
    Geri takip etmeyenleri bulma işlemini arka planda (Thread) başlatır.
    """
    if not file_paths:
        messagebox.showwarning("Uyarı", "Lütfen önce takipçi dosyalarını seçin.")
        return
    t = threading.Thread(target=find_non_followers)
    t.start()

def find_non_followers():
    """
    following.html (takip edilenler) dosyasını okur ve takipçiler listesinde (followers_list)
    olmayan kişileri belirleyerek 'Geri Takip Etmeyenler' listesini oluşturur.
    """
    global active_list
    progress_label.config(text="Takip etmeyenler bulunuyor...")
    
    # script_dir üzerinden following.html dosyasını arar
    script_dir = os.path.dirname(os.path.abspath(__file__))
    following_path = os.path.join(script_dir, "following.html")
    
    if not os.path.exists(following_path):
        # Alternatif olarak programın çalıştırıldığı aktif dizinde arar
        following_path = "following.html"
        if not os.path.exists(following_path):
            messagebox.showerror("Hata", "following.html dosyası bulunamadı!\nLütfen dosyayı script klasörüne ekleyin.")
            progress_label.config(text="Hata: following.html bulunamadı.")
            return

    try:
        # Takip edilenlerin HTML belgesini okur
        with open(following_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, "html.parser")
        following_list = [item.get_text() for item in soup.find_all("a", target="_blank")]
    except Exception as e:
        messagebox.showerror("Hata", f"following.html dosyası okunurken hata oluştu:\n{e}")
        progress_label.config(text="Hata oluştu.")
        return

    # Takipçileri de güncel tutmak için dosyalardan yeniden yükler
    followers_list.clear()
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
            soup = BeautifulSoup(html_content, "html.parser")
            names = [item.get_text() for item in soup.find_all("a", target="_blank")]
            followers_list.extend(names)
        except Exception:
            continue

    # Takip edilenler listesindeki kişilerden, bizi takip edenler listesinde bulunmayanları ayıklar
    non_followers_list = [follower for follower in following_list if follower not in followers_list]
    
    # Aktif olarak listelenen veriyi 'geri takip etmeyenler' olarak belirler
    active_list = list(non_followers_list)
    update_table(active_list)
    progress_label.config(text="Geri takip etmeyenler başarıyla listelendi.")

def search_followers():
    """
    Arama çubuğuna yazılan metne göre aktif liste (active_list) üzerinde
    büyük/küçük harf duyarsız arama yapar ve tabloyu filtreler.
    """
    search_text = search_var.get().lower()
    if search_text:
        # Aktif listedeki isimlerde arama kelimesinin geçip geçmediğini kontrol eder
        search_result = [item for item in active_list if search_text in item.lower()]
        update_table(search_result)
    else:
        # Arama kutusu boş ise tüm aktif listeyi tabloya basar
        update_table(active_list)

def clear_search():
    """Arama kutusunu sıfırlar ve aktif listenin tamamını yeniden yükler."""
    search_var.set("")
    update_table(active_list)

def export_to_excel():
    """
    Treeview tablosunda o an gösterilen aktif verileri Excel (.xlsx) formatında kaydeder.
    """
    if active_list:
        # pandas veri çerçevesi (DataFrame) oluşturur
        df = pd.DataFrame({"Kullanıcı Adı": active_list})
        excel_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if excel_file_path:
            try:
                # openpyxl motorunu kullanarak Excel dosyası yazar
                df.to_excel(excel_file_path, index=False)
                messagebox.showinfo("Başarılı", "Excel dosyası başarıyla oluşturuldu!")
            except Exception as e:
                messagebox.showerror("Hata", f"Excel kaydedilirken hata oluştu:\n{e}")
    else:
        messagebox.showwarning("Uyarı", "Aktarılacak herhangi bir veri bulunmamaktadır.")

def export_non_followers_to_pdf():
    """
    Treeview tablosunda listelenen kullanıcıları profillerinin bağlantılarıyla (URL)
    birlikte PDF rapor dosyası olarak dışa aktarır.
    """
    # Tablodaki tüm çocuk satırları alır
    table_rows = table.get_children()
    if table_rows:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # PDF başlığı ekler
        pdf.cell(200, 10, txt="Instagram Geri Takip Etmeyenler Listesi", ln=True, align='C')
        pdf.ln(10) # Satır boşluğu bırakır

        for row in table_rows:
            # Treeview satırındaki isim hücresini (index 1) çeker
            follower_username = table.item(row)["values"][1]
            pdf.cell(200, 8, txt=f"- {follower_username}", ln=True)
            # Tıklanabilir profil linkini PDF'e ekler
            pdf.cell(200, 8, txt=f"  Profil Linki: https://www.instagram.com/{follower_username}/", ln=True)
            pdf.ln(2)

        pdf_file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if pdf_file_path:
            try:
                pdf.output(pdf_file_path)
                messagebox.showinfo("Başarılı", "PDF dosyası başarıyla oluşturuldu!")
            except Exception as e:
                messagebox.showerror("Hata", f"PDF kaydedilirken hata oluştu:\n{e}")
    else:
        messagebox.showwarning("Uyarı", "Aktarılacak herhangi bir kişi bulunmamaktadır.")

def open_non_followers_in_browser():
    """
    Treeview tablosunda listelenen tüm kullanıcıların Instagram profillerini
    tarayıcıda yeni sekmeler olarak açar.
    """
    table_rows = table.get_children()
    if not table_rows:
        messagebox.showwarning("Uyarı", "Tarayıcıda açılacak herhangi bir kullanıcı bulunmamaktadır.")
        return
        
    for row in table_rows:
        follower_username = table.item(row)["values"][1]
        # Instagram adresini web tarayıcısında çağırır
        webbrowser.open(f"https://www.instagram.com/{follower_username}/")

# --- Tkinter Arayüz Kurulumu ---
app = tk.Tk()
app.title("Takipçi Analiz Uygulaması V2 @Tuncay.Lore")
app.geometry("1000x700")  # Geniş yerleşimli pencere boyutu
app.configure(bg="#0f0f0f")  # Hacker temalı koyu arka plan rengi

# Başlık Etiketi
title_label = tk.Label(app, text="Takipçi Karşılaştırma Uygulaması", font=("Courier", 24, "bold"), bg="#0f0f0f", fg="#4caf50", pady=20)
title_label.pack(fill="x")

# Butonlar için Taşıyıcı Çerçeve (Frame)
button_frame = tk.Frame(app, bg="#0f0f0f")
button_frame.pack(pady=20)

# Buton Tasarımları ve Konumlandırılması
select_file_button = tk.Button(button_frame, text="Dosyaları Seç ve Takipçileri Göster", command=open_file_and_show_followers, bg="#4caf50", fg="white", padx=10, pady=5, bd=0)
select_file_button.grid(row=0, column=0, padx=10)

select_auto_fetch_button = tk.Button(button_frame, text="Otomatik Çek", command=open_files_and_show_followers, bg="#4caf50", fg="white", padx=10, pady=5, bd=0)
select_auto_fetch_button.grid(row=0, column=1, padx=10)

show_all_button = tk.Button(button_frame, text="Tüm Takipçileri Göster", command=show_all_followers, bg="#4caf50", fg="white", padx=10, pady=5, bd=0)
show_all_button.grid(row=0, column=2, padx=10)

show_non_followers_button = tk.Button(button_frame, text="Takip Etmeyenleri Göster", command=show_non_followers, bg="#4caf50", fg="white", padx=10, pady=5, bd=0)
show_non_followers_button.grid(row=0, column=3, padx=10)

export_to_excel_button = tk.Button(button_frame, text="Excel'e Aktar", command=export_to_excel, bg="#4caf50", fg="white", padx=10, pady=5, bd=0)
export_to_excel_button.grid(row=0, column=4, padx=10)

export_to_pdf_button = tk.Button(button_frame, text="PDF'e Aktar", command=export_non_followers_to_pdf, bg="#4caf50", fg="white", padx=10, pady=5, bd=0)
export_to_pdf_button.grid(row=0, column=5, padx=10)

open_in_browser_button = tk.Button(button_frame, text="Tarayıcıda Aç", command=open_non_followers_in_browser, bg="#4caf50", fg="white", padx=10, pady=5, bd=0)
open_in_browser_button.grid(row=0, column=6, padx=10)

# Durum ve İlerleme Mesajı Etiketi
progress_label = tk.Label(app, text="", bg="#0f0f0f", fg="#4caf50")
progress_label.pack(pady=5)

# Seçilen Dosyaların Gösterildiği Liste Kutusu (Listbox)
file_listbox = tk.Listbox(app, width=90, height=4, bg="#212121", fg="white", borderwidth=0, highlightthickness=0)
file_listbox.pack(pady=10)

# Arama Çubuğu Tanımlamaları
search_var = tk.StringVar()
# search_var'da yazma (write) olayı gerçekleştiğinde arama fonksiyonunu tetikler
search_var.trace_add("write", lambda *args: search_followers())

search_entry = ttk.Entry(app, textvariable=search_var, width=70, font=("Courier", 12), style="search.TEntry")
search_entry.pack(pady=5)

clear_button = tk.Button(app, text="Aramayı Temizle", command=clear_search, bg="#4caf50", fg="#0f0f0f", bd=0, padx=10)
clear_button.pack(pady=5)

# Tablo Çerçevesi (Treeview) ve Kaydırma Çubuğu
frame = tk.Frame(app, bg="#0f0f0f")
frame.pack(padx=10, pady=10)

columns = ("Sıra No.", "İsim")
table = ttk.Treeview(frame, columns=columns, show="headings", style="Custom.Treeview")
table.heading("Sıra No.", text="Sıra No.")
table.heading("İsim", text="İsim")
table.column("Sıra No.", width=100, anchor="center")
table.column("İsim", width=400, anchor="w")
table.pack(side="left")

# Dikey Scrollbar (Kaydırma Çubuğu) Treeview'a bağlanır
vsb = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
vsb.pack(side="right", fill="y")
table.configure(yscrollcommand=vsb.set)

# Grafiksel Bileşenlerin Stil Tanımları
style = ttk.Style()
style.configure("search.TEntry", foreground="#4caf50", background="#212121", bordercolor="#4caf50")
style.configure("Custom.Treeview", background="#212121", foreground="white", fieldbackground="#212121", highlightthickness=0)

# Olay Döngüsünü Başlatma (Pencereyi açık tutar)
app.mainloop()
