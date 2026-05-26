import tkinter as tk # Arayüz penceresi oluşturmak için tkinter kütüphanesini içe aktarır
from tkinter import ttk # Temalı (daha modern görünüşlü) tkinter bileşenlerini içe aktarır
from tkinter import messagebox # Hata ve bilgi pencereleri göstermek için messagebox sınıfını içe aktarır
import requests # Web sitelerine HTTP istekleri gönderip veri çekmek için requests kütüphanesini içe aktarır
from bs4 import BeautifulSoup # HTML kodlarını kolayca taramak ve ayrıştırmak için BeautifulSoup kütüphanesini içe aktarır
import os # İşletim sistemi komutlarını çalıştırmak amacıyla os kütüphanesini içe aktarır
import math # Poisson dağılımı hesaplamaları için matematiksel fonksiyonları içe aktarır
import datetime # Tarih ve saat karşılaştırmaları yapmak için datetime modülünü içe aktarır

# Analiz sırasında varsayılan olarak kullanılacak son maç sayısı sabiti
DEFAULT_MAC_SAYISI = 7

# Belirtilen takımın genel fikstür ve galibiyet bilgilerini Sporx sitesinden çeken fonksiyon
def takim_bilgilerini_cek(takim):
    clear_screen() # Konsol ekranını temizleme fonksiyonunu çalıştırır
    
    # Arama için takım adındaki Türkçe karakterleri temizler ve küçük harfe dönüştürür
    takim_seo = turkce_karakter_degistir(takim.lower())
    
    # Sporx sitesindeki ilgili takımın fikstür sayfasına ait URL'yi oluşturur
    url = f"https://www.sporx.com/{takim_seo}-fiksturu-ve-mac-sonuclari"
    
    # Web sitesinin güvenlik engellerine takılmamak için tarayıcı taklidi yapan başlık bilgisi
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # Belirlenen adrese 10 saniye zaman aşımı limitiyle GET isteği gönderir
        response = requests.get(url, headers=headers, timeout=10)
        # Gelen HTML içeriğini BeautifulSoup nesnesine dönüştürerek ayrıştırır
        soup = BeautifulSoup(response.content, "html.parser")
    except Exception:
        # Bağlantıda veya istekte hata oluşursa kullanıcıya görsel hata mesajı gösterir
        messagebox.showerror("Hata", f"{takim.capitalize()} takımı bilgileri çekilirken bağlantı hatası oluştu.")
        return None # Hata durumunda fonksiyonu durdurup None döndürür

    # HTML belgesindeki tüm satır (tr) etiketlerini bulur
    maclar = soup.find_all("tr")
    
    galibiyet_sayisi = 0 # Takımın kazandığı toplam maç sayısını tutar
    toplam_gol = 0 # Takımın attığı toplam gol sayısını tutar
    son_mac_skoru = None # Takımın oynadığı en son maçın skor metnini tutar
    
    # Bulunan tüm satırlar (maçlar) üzerinde döngüyle gezinir
    for mac in maclar:
        # Maçın skorunu içeren ve sınıfı 'score' olan link etiketini arar
        skor_element = mac.find("a", class_="score")
        if skor_element:
            # Skor metnindeki gereksiz boşlukları temizleyerek alır (örn: "2-1")
            skor = skor_element.get_text(strip=True)  
            # Skor metnini tire (-) işaretinden ikiye böler
            gol_sayisi = skor.split("-")
            
            # Skorun geçerli bir formatta (iki elemanlı ve boş olmayan) olduğunu doğrular
            if len(gol_sayisi) == 2 and gol_sayisi[0].strip() and gol_sayisi[1].strip():
                try:
                    # Gol sayılarını metinden tam sayı (integer) türüne dönüştürür
                    attigi_gol = int(gol_sayisi[0])
                    gol_sayisi_g2 = int(gol_sayisi[1])
                except ValueError:
                    # Sayıya dönüştürülemeyen geçersiz bir skor varsa o satırı atlar
                    continue
                
                # Ev sahibi ve deplasman takımlarının HTML bloklarını bulur
                ev_sahibi_div = mac.find("div", class_="team home")
                deplasman_div = mac.find("div", class_="team away")
                
                if ev_sahibi_div and deplasman_div:
                    # Takım isimlerinin link etiketlerini bulur
                    ev_sahibi_a = ev_sahibi_div.find("a", class_="team-name")
                    deplasman_a = deplasman_div.find("a", class_="team-name")
                    
                    if ev_sahibi_a and deplasman_a:
                        # Takım isimlerini alır ve temizler
                        ev_sahibi = ev_sahibi_a.get_text(strip=True)
                        deplasman = deplasman_a.get_text(strip=True)
                        
                        # Eğer sorguladığımız takım o maçta ev sahibi ise
                        if takim.lower() == turkce_karakter_degistir(ev_sahibi.lower()):
                            toplam_gol += attigi_gol # Ev sahibinin golünü toplam golümüze ekler
                            # Ev sahibi deplasmandan fazla gol attıysa maçı kazanmıştır
                            if attigi_gol > gol_sayisi_g2:
                                galibiyet_sayisi += 1 # Galibiyet sayısını artırır
                            # Son maç skor metnini günceller
                            son_mac_skoru = f"Son Maç: {ev_sahibi} {skor} {deplasman}\n"
                            
                        # Eğer sorguladığımız takım o maçta deplasman ise
                        elif takim.lower() == turkce_karakter_degistir(deplasman.lower()):
                            toplam_gol += gol_sayisi_g2 # Deplasmanın golünü toplam golümüze ekler
                            # Deplasman ev sahibinden fazla gol attıysa maçı kazanmıştır
                            if attigi_gol < gol_sayisi_g2:
                                galibiyet_sayisi += 1 # Galibiyet sayısını artırır
                            # Son maç skor metnini günceller
                            son_mac_skoru = f"Son Maç: {ev_sahibi} {skor} {deplasman}\n"
                            
    # Eğer takıma dair hiçbir galibiyet/bilgi bulunamazsa hata gösterir
    if galibiyet_sayisi == 0:
        messagebox.showerror("Hata", f"{takim.capitalize()} takımı için bilgi bulunamadı.")
        return None # İşlemi sonlandırır ve None döner
    else:
        # İlgili istatistikleri ve son maç skorunu demet (tuple) olarak döner
        return galibiyet_sayisi, toplam_gol, son_mac_skoru


# Konsol ekranını işletim sistemine uygun şekilde temizleyen fonksiyon
def clear_screen():
    # İşletim sistemi Windows ise 'cls', macOS/Linux ise 'clear' komutunu çalıştırır
    os.system('cls' if os.name == 'nt' else 'clear')


# Türkçe harfleri İngilizce harflere çeviren ve boşlukları tire (-) yapan fonksiyon
def turkce_karakter_degistir(takim_ad):
    # Büyük İ ve I harflerini güvenli şekilde küçük ingilizce i harfine dönüştürür
    takim_ad = takim_ad.replace("İ", "i").replace("I", "i")
    # Tüm metni küçük harfe çevirir
    takim_ad = takim_ad.lower()
    # Türkçe küçük harfleri İngilizce karşılıklarıyla değiştirir
    takim_ad = takim_ad.replace("ı", "i") # 'ı' harfini 'i' yapar
    takim_ad = takim_ad.replace("ç", "c") # 'ç' harfini 'c' yapar
    takim_ad = takim_ad.replace("ş", "s") # 'ş' harfini 's' yapar
    takim_ad = takim_ad.replace("ğ", "g") # 'ğ' harfini 'g' yapar
    takim_ad = takim_ad.replace("ü", "u") # 'ü' harfini 'u' yapar
    takim_ad = takim_ad.replace("ö", "o") # 'ö' harfini 'o' yapar
    return takim_ad.replace(" ", "-") # Boşluk karakterlerini tireye dönüştürüp sonucu döner


# Türkçe tarih formatını datetime.date nesnesine dönüştüren yardımcı fonksiyon
def turkce_tarih_ayristir(tarih_str):
    # Örnek girdi: "01 Haziran 2026, 20.30" veya "01 Haziran 2026"
    tarih_kismi = tarih_str.split(",")[0].strip() # Saati ve günü ayırmak için virgüle göre böler
    parcalar = tarih_kismi.split(" ") # Günü, ay adını ve yılı boşluktan ayırır
    if len(parcalar) >= 3:
        try:
            gun = int(parcalar[0]) # Günü tam sayıya çevirir
            ay_adi = parcalar[1].lower() # Ay ismini küçük harfe çevirir
            yil = int(parcalar[2]) # Yılı tam sayıya çevirir
            # Türkçe ay adlarının takvim karşılıklarını tutan sözlük
            aylar = {
                "ocak": 1, "subat": 2, "mart": 3, "nisan": 4, "mayis": 5, "haziran": 6,
                "temmuz": 7, "agustos": 8, "eylul": 9, "ekim": 10, "kasim": 11, "aralik": 12,
                "şubat": 2, "mayıs": 5, "ağustos": 8, "eylül": 9, "kasım": 11, "aralık": 12
            }
            ay = aylar.get(ay_adi, 1) # Ay numarasını alır, bulamazsa varsayılan 1 yapar
            return datetime.date(yil, ay, gun) # Oluşturulan tarih nesnesini döner
        except Exception:
            return None # Dönüşüm sırasında hata oluşursa None döner
    return None # Geçersiz biçim ise None döner


# İki takımın 1 hafta içerisinde birbirleriyle yapacağı bir maç olup olmadığını kontrol eden fonksiyon
def gelecek_mac_kontrol(takim1, takim2):
    # Takım ismini SEO uyumlu formata çevirir
    takim1_seo = turkce_karakter_degistir(takim1.lower())
    # Sporx sitesindeki takımın fikstür sayfasının adresini oluşturur
    url = f"https://www.sporx.com/{takim1_seo}-fiksturu-ve-mac-sonuclari"
    # Güvenlik engellerini aşmak için tarayıcı taklidi yapan başlık bilgisi
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        # Sayfaya 10 saniye zaman aşımı limitiyle GET isteği gönderir
        response = requests.get(url, headers=headers, timeout=10)
        # Gelen HTML içeriğini BeautifulSoup nesnesiyle ayrıştırır
        soup = BeautifulSoup(response.content, "html.parser")
    except Exception:
        # Bağlantı hatası durumunda fonksiyonu durdurup None döner
        return None

    # HTML içerisindeki tüm tablo satırlarını (tr) bulur
    maclar = soup.find_all("tr")
    # Bugünün tarih bilgisini alır
    today = datetime.date.today()

    # Bulunan tüm maç satırlarını tek tek inceler
    for mac in maclar:
        # Gelecekteki maçları bulmak için skor kısmında tire (-) işareti olmasını kontrol eder
        skor_element = mac.find("a", class_="score")
        if skor_element:
            skor = skor_element.get_text(strip=True)
            # Skor alanı tire (-) ise yani maç henüz oynanmamışsa
            if skor == "-":
                # Ev sahibi ve deplasman takımlarının HTML bloklarını bulur
                ev_sahibi_div = mac.find("div", class_="team home")
                deplasman_div = mac.find("div", class_="team away")
                if ev_sahibi_div and deplasman_div:
                    # Takım isimlerinin link etiketlerini bulur
                    ev_a = ev_sahibi_div.find("a", class_="team-name")
                    dep_a = deplasman_div.find("a", class_="team-name")
                    if ev_a and dep_a:
                        # Takım isimlerini SEO formatına çevirip girdi takımlarla karşılaştırır
                        ev_isim = turkce_karakter_degistir(ev_a.get_text(strip=True).lower())
                        dep_isim = turkce_karakter_degistir(dep_a.get_text(strip=True).lower())

                        t1_seo = turkce_karakter_degistir(takim1.lower())
                        t2_seo = turkce_karakter_degistir(takim2.lower())

                        # Eşleşme sorgulanan iki takım arasında ise
                        if (t1_seo == ev_isim and t2_seo == dep_isim) or (t1_seo == dep_isim and t2_seo == ev_isim):
                            # Maçın tarihini içeren span etiketini bulur
                            date_span = mac.find("span", class_="date")
                            if date_span:
                                tarih_str = date_span.get_text(strip=True) # Tarih metnini alır
                                mac_tarihi = turkce_tarih_ayristir(tarih_str) # Tarihi date nesnesine dönüştürür
                                if mac_tarihi:
                                    diff = mac_tarihi - today # İki tarih arasındaki gün farkını bulur
                                    # Maçın bugünden itibaren 0 ile 7 gün arasında olup olmadığını doğrular
                                    if 0 <= diff.days <= 7:
                                        # Eşleşen maç bilgilerini sözlük olarak döner
                                        return {
                                            "tarih": tarih_str,
                                            "ev_sahibi": ev_a.get_text(strip=True),
                                            "deplasman": dep_a.get_text(strip=True),
                                            "kalan_gun": diff.days
                                        }
    return None # Kriterlere uygun yaklaşan bir maç bulunamazsa None döner


# Poisson dağılımı formülü: P(k; λ) = (λ^k * e^(-λ)) / k!
# Bir takımın belirli sayıda gol atma olasılığını hesaplar
def poisson_olasilik(k, lam):
    # k: hedeflenen gol sayısı (0, 1, 2, 3...)
    # lam (λ): takımın beklenen ortalama gol sayısı
    return (lam ** k) * math.exp(-lam) / math.factorial(k)


# İki takımın gol verilerine göre Üst 2.5 gol olasılığını Poisson yöntemiyle hesaplar
# Doğruluğu artırmak için: (1) Ev/Deplasman avantajı ve (2) Zaman ağırlıklı (güncel form) Poisson modeli kullanır.
def ust_2_5_olasilik_hesapla(takim1_mac_verileri, takim2_mac_verileri):
    # takim1_mac_verileri ve takim2_mac_verileri (kendi_gol, rakip_gol, is_home) 3-lü demetlerinden oluşur
    # Zaman ağırlıklı ortalama fonksiyonu: En yeni maçlara (listenin başındakilere) daha fazla ağırlık verir (w = 0.85^i)
    def weighted_avg(veriler, filter_fn=None, get_rakip=False):
        total_val = 0.0 # Toplam gol değerini tutar
        total_weight = 0.0 # Toplam ağırlığı tutar
        for i, (kendi, rakip, is_home) in enumerate(veriler):
            if filter_fn is None or filter_fn(is_home):
                w = 0.85 ** i # Zaman azalım katsayısı (yeni maçlar daha değerli)
                total_val += (rakip if get_rakip else kendi) * w # Gol sayısı ile ağırlığı çarparak ekler
                total_weight += w # Ağırlık toplamını günceller
        return total_val / total_weight if total_weight > 0 else None # Ağırlıklı ortalamayı döner

    # Takım 1 (Ev Sahibi): Genel ve Ev Sahibi performansları
    t1_genel_atan = weighted_avg(takim1_mac_verileri, get_rakip=False) # Genel attığı ağırlıklı gol
    t1_genel_yiyen = weighted_avg(takim1_mac_verileri, get_rakip=True) # Genel yediği ağırlıklı gol
    t1_ev_atan = weighted_avg(takim1_mac_verileri, filter_fn=lambda h: h is True, get_rakip=False) # İç sahada attığı ağırlıklı gol
    t1_ev_yiyen = weighted_avg(takim1_mac_verileri, filter_fn=lambda h: h is True, get_rakip=True) # İç sahada yediği ağırlıklı gol
    
    # Eğer son maçlarda hiç iç saha maçı yoksa genel ortalamayı kullan
    if t1_ev_atan is None: t1_ev_atan = t1_genel_atan
    if t1_ev_yiyen is None: t1_ev_yiyen = t1_genel_yiyen

    # Ev Sahibi Ağırlıklı Güç: %40 Genel Performans + %60 İç Saha Performansı
    t1_combined_atan = 0.4 * t1_genel_atan + 0.6 * t1_ev_atan
    t1_combined_yiyen = 0.4 * t1_genel_yiyen + 0.6 * t1_ev_yiyen

    # Takım 2 (Deplasman): Genel ve Deplasman performansları
    t2_genel_atan = weighted_avg(takim2_mac_verileri, get_rakip=False) # Genel attığı ağırlıklı gol
    t2_genel_yiyen = weighted_avg(takim2_mac_verileri, get_rakip=True) # Genel yediği ağırlıklı gol
    t2_dep_atan = weighted_avg(takim2_mac_verileri, filter_fn=lambda h: h is False, get_rakip=False) # Dış sahada attığı ağırlıklı gol
    t2_dep_yiyen = weighted_avg(takim2_mac_verileri, filter_fn=lambda h: h is False, get_rakip=True) # Dış sahada yediği ağırlıklı gol
    
    # Eğer son maçlarda hiç dış saha maçı yoksa genel ortalamayı kullan
    if t2_dep_atan is None: t2_dep_atan = t2_genel_atan
    if t2_dep_yiyen is None: t2_dep_yiyen = t2_genel_yiyen

    # Deplasman Ağırlıklı Güç: %40 Genel Performans + %60 Dış Saha Performansı
    t2_combined_atan = 0.4 * t2_genel_atan + 0.6 * t2_dep_atan
    t2_combined_yiyen = 0.4 * t2_genel_yiyen + 0.6 * t2_dep_yiyen

    # Beklenen gol sayıları (λ): Hücum gücü ile rakip savunma zayıflığının ortalaması
    lambda_ev = (t1_combined_atan + t2_combined_yiyen) / 2  # Ev sahibinin beklenen golü
    lambda_dep = (t2_combined_atan + t1_combined_yiyen) / 2  # Deplasmanın beklenen golü

    # Alt 2.5 olasılığı: toplam gol ≤ 2 olan tüm skorların olasılıklarını toplar
    alt_2_5 = 0.0 # Alt olasılığını tutan sayaç
    for ev_gol in range(3): # Ev sahibinin 0, 1 veya 2 gol atması
        for dep_gol in range(3): # Deplasmanın 0, 1 veya 2 gol atması
            if ev_gol + dep_gol <= 2: # Toplam gol sayısı en fazla 2 ise
                # Her iki takımın belirtilen gol olasılıklarının çarpımını alt ihtimaline ekler
                alt_2_5 += poisson_olasilik(ev_gol, lambda_ev) * poisson_olasilik(dep_gol, lambda_dep)

    # Üst 2.5 olasılığı = 1 - Alt 2.5 olasılığı
    ust_2_5 = 1.0 - alt_2_5

    return lambda_ev, lambda_dep, ust_2_5 # Hesaplanan verileri geri döndürür

# Gol tahminine dayanarak iki takım arasındaki tahmini maç sonucunu hesaplayan fonksiyon
def tahmini_mac_sonucu(gol_tahmini):
    takim1_gol = int(gol_tahmini) # Gol tahminini tam sayıya dönüştürür
    # 2. takımın atacağı golü 1. takımdan 1 eksik olarak tahmin eder (en az 0)
    takim2_gol = takim1_gol - 1 if takim1_gol > 0 else 0
    # Arayüzdeki giriş alanlarından takım isimlerini alır ve temizler
    takim1 = turkce_karakter_degistir(takim1_entry.get())
    takim2 = turkce_karakter_degistir(takim2_entry.get())
    # Tahmin metnini oluşturup döndürür
    return f"Tahmini maç sonucu: {takim1.capitalize()} {takim1_gol} - {takim2_gol} {takim2.capitalize()} "

# İki takımın analizini yapan ve arayüzü güncelleyen temel fonksiyon
def iki_takimli_analiz():
    # Giriş kutularından takımları alır ve Türkçe karakter düzenlemesi uygular
    takim1 = turkce_karakter_degistir(takim1_entry.get())
    takim2 = turkce_karakter_degistir(takim2_entry.get())
    # Gol analizi için kullanılacak son maç sayısını giriş alanından alıp tam sayıya çevirir
    mac_sayisi = int(mac_sayisi_entry.get())
    
    # Takım isimlerinden biri eksikse hata mesajı verip çalışmayı durdurur
    if not takim1 or not takim2:
        messagebox.showerror("Hata", "Lütfen takımları girin.")
        return
    
    # Her iki takım için genel bilgileri çeker
    takim1_bilgileri = takim_bilgilerini_cek(takim1)
    takim2_bilgileri = takim_bilgilerini_cek(takim2)
    
    # Bilgilerin çekilememesi durumunda analiz yapmadan fonksiyondan çıkar
    if takim1_bilgileri is None or takim2_bilgileri is None:
        return
    
    # Dönen bilgileri (galibiyet, gol, son maç skoru) ilgili değişkenlere atar
    galibiyet_sayisi_g1, gol_sayisi_g1, son_mac_skoru_g1 = takim1_bilgileri
    galibiyet_sayisi_g2, gol_sayisi_g2, son_mac_skoru_g2 = takim2_bilgileri
    
    # Galibiyet sayısına göre takımların form durumunu (favori veya normal) belirler
    takim1_form = "favori" if galibiyet_sayisi_g1 > galibiyet_sayisi_g2 else "normal"
    takim2_form = "favori" if galibiyet_sayisi_g2 > galibiyet_sayisi_g1 else "normal"
    
    # Her iki takımın son 3 maçtaki gol durumlarını (kendi_golu, rakip_golu) listesi olarak alır
    takim1_son_3_mac = son_mac_bilgilerini_cek(takim1, 3)
    takim2_son_3_mac = son_mac_bilgilerini_cek(takim2, 3)
    
    # Son 3 maça dair yeterli veri yoksa analiz yapmayı durdurur ve hata verir
    if len(takim1_son_3_mac) < 3 or len(takim2_son_3_mac) < 3:
        messagebox.showerror("Hata", "Son 3 maç verisi bulunamadı.")
        return
    
    # Takım 1'in son 3 maçtaki galibiyet, beraberlik ve mağlubiyetlerini hesaplar
    # Her demet (kendi_golu, rakip_golu, is_home) olduğundan: kendi > rakip = galibiyet
    takim1_kazanma_sayisi = sum(1 for kendi, rakip, *is_home in takim1_son_3_mac if kendi > rakip)
    takim1_beraberlik_sayisi = sum(1 for kendi, rakip, *is_home in takim1_son_3_mac if kendi == rakip)
    takim1_malubiyet_sayisi = sum(1 for kendi, rakip, *is_home in takim1_son_3_mac if kendi < rakip)
    
    # Takım 2'nin son 3 maçtaki galibiyet, beraberlik ve mağlubiyetlerini hesaplar
    takim2_kazanma_sayisi = sum(1 for kendi, rakip, *is_home in takim2_son_3_mac if kendi > rakip)
    takim2_beraberlik_sayisi = sum(1 for kendi, rakip, *is_home in takim2_son_3_mac if kendi == rakip)
    takim2_malubiyet_sayisi = sum(1 for kendi, rakip, *is_home in takim2_son_3_mac if kendi < rakip)
    
    # Belirtilen maç sayısı kadar olan geçmiş maçlardaki gol bilgilerini çeker (Poisson hesabı için)
    takim1_tum_mac_gol = son_mac_bilgilerini_cek(takim1, mac_sayisi)
    takim2_tum_mac_gol = son_mac_bilgilerini_cek(takim2, mac_sayisi)
    
    # Belirtilen analiz maç sayısı kadar veri bulunamazsa işlemi sonlandırır
    if len(takim1_tum_mac_gol) < mac_sayisi or len(takim2_tum_mac_gol) < mac_sayisi:
        messagebox.showerror("Hata", "Gol tahmini yapmak için yeterli veri bulunamadı.")
        return
    
    # Takım 1'in son 3 maçında attığı toplam golü hesaplar (sadece kendi golleri)
    takim1_toplam_gol = sum(kendi for kendi, rakip, *is_home in takim1_son_3_mac)
    
    # Takım 2'nin son 3 maçında attığı toplam golü hesaplar (sadece kendi golleri)
    takim2_toplam_gol = sum(kendi for kendi, rakip, *is_home in takim2_son_3_mac)
    
    # Poisson dağılımı ile Üst 2.5 gol olasılığını hesaplar (son N maç verileriyle)
    lambda_ev, lambda_dep, ust_2_5 = ust_2_5_olasilik_hesapla(takim1_tum_mac_gol, takim2_tum_mac_gol)
    
    # Takımların maç başına ortalama gol sayıları
    t1_ort = sum(k for k, r, *is_home in takim1_tum_mac_gol) / len(takim1_tum_mac_gol)
    t2_ort = sum(k for k, r, *is_home in takim2_tum_mac_gol) / len(takim2_tum_mac_gol)
    
    # Sonuç metnini hazırlamaya başlar ve form/galibiyet istatistiklerini ekler
    sonuc = f"{takim1.capitalize()} Takımı Form Durumu: {takim1_form}\n"
    sonuc += f"{takim2.capitalize()} Takımı Form Durumu: {takim2_form}\n\n"
    sonuc += f"{takim1.capitalize()} Son 3 Maçta:\nKazanma Sayısı: {takim1_kazanma_sayisi}\nBeraberlik Sayısı: {takim1_beraberlik_sayisi}\nMalubiyet Sayısı: {takim1_malubiyet_sayisi}\nAttığı Gol Sayısı: {takim1_toplam_gol}\n\n"
    sonuc += f"{takim2.capitalize()} Son 3 Maçta:\nKazanma Sayısı: {takim2_kazanma_sayisi}\nBeraberlik Sayısı: {takim2_beraberlik_sayisi}\nMalubiyet Sayısı: {takim2_malubiyet_sayisi}\nAttığı Gol Sayısı: {takim2_toplam_gol}\n\n"
    sonuc += f"{takim1.capitalize()} Maç Başına Ort. Gol: {t1_ort:.2f}\n"
    sonuc += f"{takim2.capitalize()} Maç Başına Ort. Gol: {t2_ort:.2f}\n\n"
    sonuc += f"Beklenen Gol (Poisson): {takim1.capitalize()} {lambda_ev:.2f} - {lambda_dep:.2f} {takim2.capitalize()}\n"
    sonuc += "(Poisson: Takımların gol atma ve yeme ortalamalarını analiz ederek, bu maçta atabilecekleri tahmini gol sayılarını hesaplayan matematiksel modeldir.)\n\n"
    
    # Poisson ile hesaplanan Üst 2.5 olasılığına göre yorum ekler
    ust_yuzde = ust_2_5 * 100
    if ust_yuzde >= 70:
        sonuc += f"Maçın Üst 2.5 Bitme Olasılığı: %{ust_yuzde:.1f} (Çok Yüksek)\n"
    elif ust_yuzde >= 50:
        sonuc += f"Maçın Üst 2.5 Bitme Olasılığı: %{ust_yuzde:.1f} (Yüksek)\n"
    elif ust_yuzde >= 35:
        sonuc += f"Maçın Üst 2.5 Bitme Olasılığı: %{ust_yuzde:.1f} (Orta)\n"
    else:
        sonuc += f"Maçın Üst 2.5 Bitme Olasılığı: %{ust_yuzde:.1f} (Düşük)\n"
    sonuc += f"Maçın Alt 2.5 Bitme Olasılığı: %{(100 - ust_yuzde):.1f}\n"
    
    # 1 hafta içinde birbirleriyle maçları olup olmadığını kontrol eder
    gelecek_mac = gelecek_mac_kontrol(takim1, takim2)
    if gelecek_mac:
        tarih_str = gelecek_mac["tarih"] # Maçın tarihini alır
        ev = gelecek_mac["ev_sahibi"] # Ev sahibi takım adını alır
        dep = gelecek_mac["deplasman"] # Deplasman takım adını alır
        
        # Olası sonuç tahmini yorumunu belirler
        if lambda_ev > lambda_dep + 0.3:
            tahmin_yorum = f"Ev sahibi {ev} ekibi galibiyete daha yakın görünüyor."
        elif lambda_dep > lambda_ev + 0.3:
            tahmin_yorum = f"Deplasman {dep} ekibi galibiyete daha yakın görünüyor."
        else:
            tahmin_yorum = "Mücadele oldukça dengeli, beraberlik olasılığı yüksek görünüyor."
            
        # Maçın alt/üst durumunu olasılığa göre değerlendirir
        if ust_yuzde >= 50:
            gol_tahmin_yorum = f"maçın Üst 2.5 Gol (%{ust_yuzde:.1f}) bitme ihtimali daha yüksektir."
        else:
            gol_tahmin_yorum = f"maçın Alt 2.5 Gol (%{100 - ust_yuzde:.1f}) bitme ihtimali daha yüksektir."
            
        # Sonuç ekranı metnine yaklaşan maç detaylarını ekler
        sonuc += f"\n📣 YAKLAŞAN MAÇ BİLGİSİ ({tarih_str}):\n"
        sonuc += f"Bu iki takımın 1 hafta içerisinde karşı karşıya geleceği bir maçı bulunuyor.\n"
        sonuc += f"Mevcut oranlara göre: {tahmin_yorum}\n"
        sonuc += f"Ayrıca {gol_tahmin_yorum}\n"
    else:
        # Yakın zamanda maç yoksa bunu belirten mesajı ekler
        sonuc += f"\n📣 YAKLAŞAN MAÇ BİLGİSİ:\n"
        sonuc += f"Bu iki takımın yakın zamanda (1 hafta içerisinde) karşılaşacağı bir maç bulunmuyor.\n"

    # Arayüzdeki sonuç etiketinin metnini günceller
    sonuc_label.config(text=sonuc)
    # Arayüz penceresinin eklenen yeni metne göre otomatik genişlemesini zorunlu kılar
    root.geometry("") 


# Belirli sayıda son maçın gol bilgilerini fikstür sayfasından çeken fonksiyon
# Her maç için (kendi_golu, rakip_golu) şeklinde bir demet (tuple) listesi döner
def son_mac_bilgilerini_cek(takim, mac_sayisi):
    # Takım ismini Türkçe karakterlerden arındırır ve küçük harfe çevirir
    takim_seo = turkce_karakter_degistir(takim.lower())
    # Sporx sitesindeki takımın fikstür sayfa adresini oluşturur
    url = f"https://www.sporx.com/{takim_seo}-fiksturu-ve-mac-sonuclari"
    # Sunucu engellemelerini aşmak için User-Agent başlığını ekler
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        # Sayfaya 10 saniye zaman aşımı limitiyle GET isteği gönderir
        response = requests.get(url, headers=headers, timeout=10)
        # HTML içeriğini BeautifulSoup ile ayrıştırır
        soup = BeautifulSoup(response.content, "html.parser")
    except Exception:
        # Bağlantı hatası durumunda boş liste döner
        return []

    # HTML içerisindeki tüm tablo satırlarını (tr) bulur
    maclar = soup.find_all("tr")
    mac_sonuclari = [] # Her maç için (kendi_golu, rakip_golu) demetlerini tutan liste
    mac_sayaci = 0 # İşlenen maç sayısını takip eden sayaç

    # Bulunan tüm satırları ters sırada (en yeni maçtan en eskiye) inceler
    for mac in reversed(maclar):
        # Skor bilgisini tutan 'score' sınıflı link etiketini bulur
        skor_element = mac.find("a", class_="score")
        if skor_element:
            # Skor metnini alır ve temizler
            skor = skor_element.get_text(strip=True)
            # Skoru '-' işaretine göre ikiye böler
            gol_sayisi = skor.split("-")

            # Skorun iki elemanlı ve geçerli değerlerden oluştuğunu kontrol eder
            if len(gol_sayisi) == 2 and gol_sayisi[0].strip() and gol_sayisi[1].strip():
                try:
                    # Ev sahibi ve deplasman gol sayılarını integer tipine dönüştürür
                    ev_gol = int(gol_sayisi[0])
                    dep_gol = int(gol_sayisi[1])
                except ValueError:
                    # Hatalı bir skor gelirse bu satırı es geçer
                    continue

                # Ev sahibi ve deplasman takım isimlerini HTML'den bulur
                ev_sahibi_div = mac.find("div", class_="team home")
                deplasman_div = mac.find("div", class_="team away")

                if ev_sahibi_div and deplasman_div:
                    ev_a = ev_sahibi_div.find("a", class_="team-name")
                    dep_a = deplasman_div.find("a", class_="team-name")

                    if ev_a and dep_a:
                        # Takım isimlerini alır ve SEO formatına dönüştürür
                        ev_isim = turkce_karakter_degistir(ev_a.get_text(strip=True).lower())
                        dep_isim = turkce_karakter_degistir(dep_a.get_text(strip=True).lower())

                        # Bizim takımımız ev sahibi ise: kendi golü = ev_gol, rakip golü = dep_gol, is_home = True
                        if takim.lower() == ev_isim:
                            mac_sonuclari.append((ev_gol, dep_gol, True))
                            mac_sayaci += 1
                        # Bizim takımımız deplasman ise: kendi golü = dep_gol, rakip golü = ev_gol, is_home = False
                        elif takim.lower() == dep_isim:
                            mac_sonuclari.append((dep_gol, ev_gol, False))
                            mac_sayaci += 1

                # Eğer istenen maç sayısına ulaşıldıysa döngüyü sonlandırır
                if mac_sayaci >= mac_sayisi:
                    break
    # Her maç için (kendi_golu, rakip_golu) demetlerinden oluşan listeyi döndürür
    return mac_sonuclari

# Arayüz Bileşenlerinin Oluşturulması ve Yapılandırılması
root = tk.Tk() # Ana Tkinter penceresini oluşturur
root.title("Futbol Analiz Programı") # Pencerenin başlığını belirler
root.resizable(False, False)  # Kullanıcının fare ile pencereyi manuel boyutlandırmasını kilitler

# Widget'ları düzenli gruplamak için bir Frame (çerçeve) oluşturur
frame = ttk.Frame(root)
# Çerçeveyi grid yerleşim sistemine göre konumlandırır ve kenar boşlukları verir
frame.grid(row=0, column=0, padx=10, pady=10)

# Ev sahibi takım yazısı etiketini oluşturur ve sola hizalar
takim1_label = ttk.Label(frame, text="Ev Sahibi Takım:")
takim1_label.grid(row=0, column=0, sticky="w")

# Ev sahibi takımı girmek için metin giriş kutusunu oluşturur
takim1_entry = ttk.Entry(frame)
takim1_entry.grid(row=0, column=1, padx=5, pady=5) # Giriş kutusunu konumlandırır

# Deplasman takımı yazısı etiketini oluşturur ve sola hizalar
takim2_label = ttk.Label(frame, text="Deplasman Takım:")
takim2_label.grid(row=1, column=0, sticky="w")

# Deplasman takımı girmek için metin giriş kutusunu oluşturur
takim2_entry = ttk.Entry(frame)
takim2_entry.grid(row=1, column=1, padx=5, pady=5) # Giriş kutusunu konumlandırır

# Maç sayısı açıklaması etiketini oluşturur ve sola hizalar
mac_sayisi_label = ttk.Label(frame, text="Gol analizi için kullanılacak son maç sayısı:")
mac_sayisi_label.grid(row=2, column=0, sticky="w")

# Analiz edilecek maç sayısı giriş kutusunu oluşturur
mac_sayisi_entry = ttk.Entry(frame)
# Varsayılan maç sayısı sabitini metin olarak kutunun içine yerleştirir
mac_sayisi_entry.insert(0, str(DEFAULT_MAC_SAYISI))
mac_sayisi_entry.grid(row=2, column=1, padx=5, pady=5) # Giriş kutusunu konumlandırır

# Analiz tetikleme butonunu oluşturur ve iki sütun genişliğinde konumlandırır
analiz_button = ttk.Button(frame, text="Analiz Yap", command=iki_takimli_analiz)
analiz_button.grid(row=3, column=0, columnspan=2, pady=10)

# Analiz sonuçlarının yazdırılacağı boş etiket alanını hazırlar (Sola hizalı)
sonuc_label = ttk.Label(frame, text="", justify="left", anchor="w")
# Etiket alanını pencereye yerleştirir ve kenar boşlukları ekler
sonuc_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=10)

# Arayüz ana olay döngüsünü başlatır (pencereyi ekranda açık tutar)
root.mainloop()