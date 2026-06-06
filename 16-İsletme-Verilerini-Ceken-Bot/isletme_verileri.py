import tkinter as tk
from tkinter import ttk, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading
import pandas as pd
import webbrowser
import re

# Siyah beyaz stilinde tkinter UI oluşturma
class GoogleMapsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Haritalar Arama Botu")
        self.root.geometry("1080x720")
        self.root.configure(bg="#FFFFFF")

        # Üst tarafta arama kutusu ve veri çekme seçenekleri
        self.frame_top = tk.Frame(self.root, bg="#FFFFFF", bd=10, relief=tk.FLAT)
        self.frame_top.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.2)

        self.label_search = tk.Label(self.frame_top, text="Aramak İstediğiniz Kelime:", bg="#FFFFFF", font=("Helvetica", 10))
        self.label_search.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_search = tk.Entry(self.frame_top, font=("Helvetica", 10), bd=5, relief=tk.FLAT, fg="black", bg="#F8D8E8")
        self.entry_search.grid(row=0, column=1, padx=5, pady=5)
        
        self.label_count = tk.Label(self.frame_top, text="Çekilecek İşletme Sayısı:", bg="#FFFFFF", font=("Helvetica", 10))
        self.label_count.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_count = tk.Entry(self.frame_top, font=("Helvetica", 10), bd=5, relief=tk.FLAT, fg="black", bg="#F8D8E8")
        self.entry_count.grid(row=1, column=1, padx=5, pady=5)

        # Butonları yan yana koyma ve sola yaslama
        self.button_frame = tk.Frame(self.frame_top, bg="#FFFFFF")
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="w")

        self.button_start = tk.Button(self.button_frame, text="Verileri Çek", command=self.start_scraping_thread, font=("Helvetica", 10), bg="#FF0000", fg="#FFFFFF", relief=tk.RAISED, padx=5, pady=5)
        self.button_start.pack(side=tk.LEFT, padx=5)

        self.button_export = tk.Button(self.button_frame, text="Excel'e Aktar", command=self.export_to_excel, font=("Helvetica", 10), bg="#008000", fg="#FFFFFF", relief=tk.RAISED, padx=5, pady=5)
        self.button_export.pack(side=tk.LEFT, padx=5)

        # Alt tarafta çekilen verileri göstermek için tablo
        self.frame_bottom = tk.Frame(self.root, bg="#FFFFFF", bd=10, relief=tk.FLAT)
        self.frame_bottom.place(relx=0.02, rely=0.3, relwidth=0.96, relheight=0.65)

        self.tree = ttk.Treeview(self.frame_bottom, columns=("İşletme Adı", "Adres", "İletişim No", "Mesaj Atıldı Mı?", "Mesaj Gönder"), show='headings', height=15)
        self.tree.heading("İşletme Adı", text="İşletme Adı")
        self.tree.heading("Adres", text="Adres")
        self.tree.heading("İletişim No", text="İletişim No")
        self.tree.heading("Mesaj Atıldı Mı?", text="Mesaj Atıldı Mı?")
        self.tree.heading("Mesaj Gönder", text="Mesaj Gönder")
        self.tree.column("İşletme Adı", width=150)
        self.tree.column("Adres", width=250)
        self.tree.column("İletişim No", width=120)
        self.tree.column("Mesaj Atıldı Mı?", width=100)
        self.tree.column("Mesaj Gönder", width=100)

        # Scrollbar ekleme
        self.scrollbar = ttk.Scrollbar(self.frame_bottom, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Stil ayarları
        style = ttk.Style()
        style.configure("Treeview", background="#F5F5F5", foreground="black", rowheight=25, fieldbackground="#F5F5F5")
        style.map("Treeview", background=[('selected', '#000000')], foreground=[('selected', '#FFFFFF')])

        # Mesaj gönder butonlarını ekleme
        self.tree.bind("<Button-1>", self.on_tree_click)

    def _update_ui(self, func):
        """Thread-safe UI güncelleme: ana thread üzerinde çalıştırır."""
        try:
            self.root.after(0, func)
        except RuntimeError:
            pass

    def start_scraping_thread(self):
        # Butonu devre dışı bırak ve verileri çekmek için ayrı bir iş parçacığı oluşturma
        self.button_start.config(state=tk.DISABLED)
        thread = threading.Thread(target=self.scrape_data, daemon=True)
        thread.start()

    def scrape_data(self):
        search_query = self.entry_search.get()
        try:
            count = int(self.entry_count.get())
        except ValueError:
            count = 15

        # Edge veya Chrome WebDriver'ı başlat
        driver = None
        try:
            # Kullanıcının bilgisayarında Chrome yüklü olmadığı için Edge tercih ediyoruz
            options = webdriver.EdgeOptions()
            options.add_argument("--window-size=1280,1024")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            driver = webdriver.Edge(options=options)
            print("Edge tarayıcısı başarıyla başlatıldı.")
        except Exception as e_edge:
            print(f"Edge başlatılamadı: {e_edge}. Chrome deneniyor...")
            try:
                options = webdriver.ChromeOptions()
                options.add_argument("--window-size=1280,1024")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option("useAutomationExtension", False)
                driver = webdriver.Chrome(options=options)
                print("Chrome tarayıcısı başarıyla başlatıldı.")
            except Exception as e_chrome:
                print(f"Chrome da başlatılamadı: {e_chrome}")
                # Hata mesajı gösterip işlemi bitir ve butonu aktif et
                self.root.after(0, lambda: self.button_start.config(state=tk.NORMAL))
                return

        try:
            # Google Haritalar'ı aç
            driver.get("https://www.google.com.tr/maps/")

            # Çerez onay ekranını geç (varsa)
            try:
                # 1. Aşama: iframe kontrolü
                try:
                    WebDriverWait(driver, 4).until(
                        EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@src, 'consent.google') or contains(@title, 'Consent')]"))
                    )
                    print("Çerez onay iframe'ine geçiş yapıldı.")
                except:
                    pass

                # 2. Aşama: Kabul et butonunu bul ve tıkla
                accept_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//button[contains(., 'Tümünü kabul et') or contains(., 'Accept all') or contains(., 'Kabul et') or contains(., 'I agree') or contains(., 'Kabul ediyorum') or @id='introAgreeButton' or @aria-label='Tümünü kabul et' or @aria-label='Accept all']"
                    ))
                )
                accept_button.click()
                print("Çerez onayı kabul edildi.")
                time.sleep(2)
                
                # iframe'e geçildiyse ana içeriğe geri dön
                try:
                    driver.switch_to.default_content()
                except:
                    pass
            except Exception as e:
                print("Çerez onay ekranı doğrudan bulunamadı veya geçilemedi:", e)
                try:
                    driver.switch_to.default_content()
                except:
                    pass

            # Arama kutusunu bul
            search_box = None
            for selector_type, selector_val in [
                (By.ID, "searchboxinput"),
                (By.XPATH, "//form[contains(@jsaction, 'searchbox')]//input"),
                (By.XPATH, "//input[contains(@class, 'UGojuc')]"),
                (By.CSS_SELECTOR, "input.UGojuc"),
                (By.XPATH, "//input[@id='ucc-1']")
            ]:
                try:
                    search_box = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((selector_type, selector_val))
                    )
                    print(f"Arama kutusu bulundu (Selector: {selector_val})")
                    break
                except:
                    continue
            
            if not search_box:
                raise Exception("Arama kutusu bulunamadı.")

            # Kullanıcıdan alınan arama terimini arama kutusuna yaz
            search_box.send_keys(search_query)
            
            # Arama butonuna tıklayın veya Enter'a basarak arama yapın
            search_box.send_keys(Keys.ENTER)

            # Arama sonuçlarını beklemek için kısa bir süre uyutma
            time.sleep(4)

            # İlk 'count' kadar işletmeyi al ve her biri için bilgileri yazdır
            index = 1
            while index <= count:
                try:
                    # İşletmeleri bul
                    businesses = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Nv2PK")))
                    if index <= len(businesses):
                        business = businesses[index - 1]
                        driver.execute_script("arguments[0].scrollIntoView(true);", business)
                        time.sleep(0.5)
                        business.click()
                        time.sleep(2)  # Bilgilerin yüklenmesi için bekleme süresi

                        # İşletme adı, adresi ve iletişim numarasını bul
                        try:
                            # H1 başlığını bulmayı dene (DUwDvf sınıfıyla birlikte)
                            business_name = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'DUwDvf')]"))
                            ).text
                        except:
                            try:
                                business_name = driver.find_element(By.CLASS_NAME, "DUwDvf").text
                            except:
                                business_name = "Bilgi bulunamadı"
                        
                        try:
                            address = driver.find_element(By.CSS_SELECTOR, "button[data-item-id='address'] .Io6YTe").text
                        except:
                            address = "Bilgi bulunamadı"
                        
                        try:
                            phone_number = driver.find_element(By.CSS_SELECTOR, "button[data-item-id^='phone'] .Io6YTe").text
                            phone_number = re.sub(r'\D', '', phone_number)  # Sadece rakamları al
                            phone_number = f'+90{phone_number[-10:]}'  # Telefon numarasını WhatsApp formatına çevir
                        except:
                            phone_number = "Bilgi bulunamadı"
                        
                        # Verileri tabloya ekle (thread-safe)
                        row_data = (business_name, address, phone_number, "Hayır", "Mesaj Gönder")
                        self._update_ui(lambda d=row_data: self.tree.insert("", "end", values=d))

                        index += 1
                    else:
                        # Daha fazla işletme yüklenmesi için sonuç panelini bul ve kaydır
                        try:
                            panel = driver.find_element(By.XPATH, "//div[@role='feed']")
                        except:
                            try:
                                panel = driver.find_element(By.CSS_SELECTOR, "div[aria-label^='Results for'], div[aria-label^='Arama sonuçları']")
                            except:
                                panel = None
                        
                        if panel:
                            last_height = driver.execute_script("return arguments[0].scrollHeight", panel)
                            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", panel)
                            time.sleep(2)  # Yüklenmesi için bekleme süresi
                            new_height = driver.execute_script("return arguments[0].scrollHeight", panel)
                            
                            # Yeni veri gelmediyse sonlanmış demektir
                            if new_height == last_height:
                                print("Listenin sonuna gelindi.")
                                break
                        else:
                            # Panel bulunamadıysa sonsuz döngüden kaçınmak için break yapalım
                            print("Sonuç paneli bulunamadı.")
                            break
                except Exception as e:
                    print(f"Hata: {e}")
                    index += 1

        finally:
            # İşlemler bittikten sonra tarayıcıyı kapat ve butonu tekrar aktif et
            try:
                driver.quit()
            except:
                pass
            self._update_ui(lambda: self.button_start.config(state=tk.NORMAL))

    def export_to_excel(self):
        # Verileri Excel dosyasına aktarma işlemi
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            data = []
            for item in self.tree.get_children():
                values = self.tree.item(item, "values")
                data.append(values)
            
            df = pd.DataFrame(data, columns=["İşletme Adı", "Adres", "İletişim No", "Mesaj Atıldı Mı?", "Mesaj Gönder"])
            df.to_excel(file_path, index=False)
            print("Veriler Excel dosyasına aktardıldı.")

    def on_tree_click(self, event):
        region = self.tree.identify('region', event.x, event.y)
        if region == 'cell':
            column = self.tree.identify_column(event.x)
            if column == '#5':  # 'Mesaj Gönder' sütunu
                selected_item = self.tree.identify_row(event.y)
                if selected_item:
                    item = self.tree.item(selected_item)
                    values = item["values"]
                    phone_number = values[2]
                    if phone_number != "Bilgi bulunamadı" and phone_number:
                        # WhatsApp mesajı gönderme (numarayı WhatsApp web ile açma)
                        try:
                            webbrowser.open(f"https://wa.me/{phone_number}")
                            self.tree.set(selected_item, column="Mesaj Atıldı Mı?", value="Evet")
                            print(f"{phone_number} numarası WhatsApp'ta açıldı.")
                        except Exception as e:
                            print(f"Mesaj gönderilemedi: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GoogleMapsApp(root)
    root.mainloop()
