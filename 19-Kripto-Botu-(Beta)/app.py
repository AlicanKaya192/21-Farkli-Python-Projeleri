# =============================================================================
# BTCTurk Kripto Al-Sat Botu Arayüzü (app.py)
# =============================================================================
# Bu program, Tkinter arayüz kütüphanesini kullanarak BtcTurk borsasında işlem
# yapan gelişmiş bir bot kontrol panelidir.
# 
# Botun Temel Özellikleri:
# 1. 3 Farklı Log Ekranı: Genel durum logları, Alım logları ve Satış logları.
# 2. Durum Saklama: Loglar, aktif bot durumları ve maliyetler JSON dosyasında saklanır.
# 3. Canlı TRY Bakiyesi: Her 40 saniyede bir bakiyeyi günceller.
# 4. Pariteler Tablosu: BtcTurk üzerindeki tüm TRY paritelerini ve aktif bot durumunu listeler.
# 5. Varlıklarım Tablosu: Cüzdandaki varlıkları, kilitli/serbest miktarları ve anlık değerlerini gösterir.
# 6. 5 Dakikalık Gözlem Algoritması: Otomatik ticaret modu açıldığında, önce 5 dakika fiyat toplar,
#    en dip noktayı tespit eder, alım yapar ve belirlenen kâr oranına ulaşınca satış gerçekleştirir.
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
import json
import time
import threading
import os
# pyrefly: ignore [missing-import]
from btcturk_wrapper import BTCTurk

# -----------------------------------------------------------------------------
# API ANAHTARLARI: BtcTurk API Key ve Secret Key değerlerinizi buraya girin.
# -----------------------------------------------------------------------------
PUBLIC_KEY = "APİ ANAHTARLARINI GİRİN"
PRIVATE_KEY = "APİ ANAHTARLARINI GİRİN"

# API Anahtarlarının doldurulup doldurulmadığını kontrol edelim
is_keys_placeholder = (
    "GİRİN" in PUBLIC_KEY or "APİ" in PUBLIC_KEY or
    "GİRİN" in PRIVATE_KEY or "APİ" in PRIVATE_KEY or
    not PUBLIC_KEY.strip() or not PRIVATE_KEY.strip()
)

if is_keys_placeholder:
    import sys
    root_temp = tk.Tk()
    root_temp.withdraw()
    messagebox.showerror(
        "API Anahtarı Eksik",
        "Lütfen öncelikle app.py içerisindeki PUBLIC_KEY ve PRIVATE_KEY "
        "değerlerini kendi BtcTurk API anahtarlarınız ile güncelleyin!"
    )
    root_temp.destroy()
    sys.exit(1)

try:
    bt = BTCTurk(apiKey=PUBLIC_KEY, apiSecret=PRIVATE_KEY)
except Exception as e:
    import sys
    root_temp = tk.Tk()
    root_temp.withdraw()
    messagebox.showerror(
        "API Bağlantı Hatası",
        f"API Anahtarları başlatılırken hata oluştu:\n{e}\n\n"
        "Lütfen PUBLIC_KEY ve PRIVATE_KEY değerlerini doğru formatta girdiğinizden emin olun."
    )
    root_temp.destroy()
    sys.exit(1)

# Bot durumunun kaydedileceği yerel dosya
STATE_FILE = "bot_state.json"

# Botun çalışma durumu ve log verilerini tutan küresel durum sözlüğü (state)
bot_state = {
    "auto_running": {},       # Parite bazlı otomatik botun aktiflik durumu (True/False)
    "avg_buy_price": {},      # Coin bazlı ortalama alım/maliyet fiyatları
    "logs": {
        "general": "",        # Genel işlem log geçmişi
        "buy": "",            # Alım işlem log geçmişi
        "sell": ""            # Satış işlem log geçmişi
    }
}

def load_state():
    """Bot durumunu ve geçmiş logları diskteki JSON dosyasından geri yükler."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            bot_state["auto_running"] = data.get("auto_running", {})
            bot_state["avg_buy_price"] = data.get("avg_buy_price", {})
            bot_state["logs"] = data.get("logs", {"general":"", "buy":"", "sell":""})
        except:
            pass

def save_state():
    """Botun güncel durumunu ve log verilerini diskteki JSON dosyasına kaydeder."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(bot_state, f, indent=2, ensure_ascii=False)

# Program başlarken geçmiş durumu yükle
load_state()

# -----------------------------------------------------------------------------
# ARAYÜZ (GUI) KURULUMU
# -----------------------------------------------------------------------------
root = tk.Tk()
root.title("Gelişmiş Kripto Ticaret Botu - BtcTurk API")
root.geometry("1300x800")

# ------------------------- LOG PENCERELERİ (3 AYRI EKRAN)
# Genel Loglar, Alım İşlemleri ve Satış İşlemleri ayrı metin kutularında gösterilir.
frame_logs = ttk.LabelFrame(root, text="İşlem Logları (Genel / Alım / Satış)")
frame_logs.pack(fill="both", expand=True, padx=10, pady=5)

text_log_general = tk.Text(frame_logs, wrap="none", height=6, width=60, font=("Consolas", 9))
text_log_buy = tk.Text(frame_logs, wrap="none", height=6, width=60, font=("Consolas", 9), fg="green")
text_log_sell = tk.Text(frame_logs, wrap="none", height=6, width=60, font=("Consolas", 9), fg="blue")

text_log_general.grid(row=0, column=0, sticky="nsew")
text_log_buy.grid(row=0, column=1, sticky="nsew")
text_log_sell.grid(row=0, column=2, sticky="nsew")

frame_logs.rowconfigure(0, weight=1)
frame_logs.columnconfigure(0, weight=1)
frame_logs.columnconfigure(1, weight=1)
frame_logs.columnconfigure(2, weight=1)

# Log ekleme yardımcı fonksiyonları
def log_general(msg):
    """Genel durum log ekranına tarihli mesaj ekler."""
    t_str = time.strftime('%H:%M:%S')
    text_log_general.insert(tk.END, f"[{t_str}] {msg}\n")
    text_log_general.see(tk.END)
    bot_state["logs"]["general"] += f"[{t_str}] {msg}\n"

def log_buy(msg):
    """Alım log ekranına mesaj ekler."""
    t_str = time.strftime('%H:%M:%S')
    text_log_buy.insert(tk.END, f"[{t_str}] {msg}\n")
    text_log_buy.see(tk.END)
    bot_state["logs"]["buy"] += f"[{t_str}] {msg}\n"

def log_sell(msg):
    """Satış log ekranına mesaj ekler."""
    t_str = time.strftime('%H:%M:%S')
    text_log_sell.insert(tk.END, f"[{t_str}] {msg}\n")
    text_log_sell.see(tk.END)
    bot_state["logs"]["sell"] += f"[{t_str}] {msg}\n"

# Geçmişten yüklenen logları pencerelere doldur
text_log_general.insert(tk.END, bot_state["logs"]["general"])
text_log_buy.insert(tk.END, bot_state["logs"]["buy"])
text_log_sell.insert(tk.END, bot_state["logs"]["sell"])

def clear_logs():
    """Tüm log ekranlarını temizler ve diskteki JSON verisini sıfırlar."""
    text_log_general.delete("1.0", tk.END)
    text_log_buy.delete("1.0", tk.END)
    text_log_sell.delete("1.0", tk.END)
    bot_state["logs"]["general"] = ""
    bot_state["logs"]["buy"] = ""
    bot_state["logs"]["sell"] = ""
    save_state()
    log_general("Loglar temizlendi.")

btn_log_clear = ttk.Button(frame_logs, text="Logları Temizle", command=clear_logs)
btn_log_clear.grid(row=1, column=0, padx=5, pady=5, sticky="w")

# ------------------------- ORAN VE YÜZDE AYARLARI
frame_ratio = ttk.LabelFrame(root, text="Al-Sat Strateji Oranları")
frame_ratio.pack(fill="x", padx=10, pady=5)

# Satış Hedef Yüzdesi (Örn: Alınan coin fiyatı %2 artınca satılsın)
label_sell_ratio = ttk.Label(frame_ratio, text="Hedef Kâr Oranı (%):")
label_sell_ratio.pack(side="left", padx=5)
entry_sell_ratio = ttk.Entry(frame_ratio, width=5)
entry_sell_ratio.pack(side="left")
entry_sell_ratio.insert(0, "2")  # Varsayılan değer: %2

def get_sell_ratio():
    try:
        val = float(entry_sell_ratio.get().strip())
        if val <= 0:
            val = 2.0
        return val
    except:
        return 2.0

# Alım Yüzdesi (Kullanılabilir toplam TRY bakiyesinin yüzde kaçıyla alım yapılsın)
label_purchase_ratio = ttk.Label(frame_ratio, text="Kullanılacak Bakiye Oranı (%):")
label_purchase_ratio.pack(side="left", padx=20)
entry_purchase_ratio = ttk.Entry(frame_ratio, width=5)
entry_purchase_ratio.pack(side="left")
entry_purchase_ratio.insert(0, "50")  # Varsayılan değer: %50

def get_purchase_ratio():
    try:
        val = float(entry_purchase_ratio.get().strip())
        if val <= 0:
            val = 50.0
        return val
    except:
        return 50.0

# ------------------------- TRY BAKİYESİ PANELİ (Her 40 saniyede bir güncellenir)
label_try_balance = ttk.Label(root, text="Güncel TRY Bakiyesi: Hesaplananıyor...", font=("Helvetica", 11, "bold"))
label_try_balance.pack(pady=5)

def update_try_balance():
    """BtcTurk cüzdanındaki Türk Lirası bakiyesini sorgular ve arayüze yazar."""
    try:
        bals = bt.get_balances(nonzero=False)
        val = 0.0
        for b in bals:
            if b["asset"] == "TRY":
                val = float(b["balance"])
                break
        label_try_balance.config(text=f"Güncel TRY Bakiyesi: {val:.2f} TRY")
    except Exception as e:
        label_try_balance.config(text=f"TRY Bakiyesi Hata: {e}")
    # 40 saniye (40.000 ms) sonra tekrar tetiklenir
    root.after(40000, update_try_balance)

update_try_balance()

# ------------------------- TABLO SIRALAMA YARDIMCISI
def to_float_safe(v):
    """String verileri sayısal sıralama için güvenli float'a çevirir."""
    if v == "ON": return 1
    if v == "OFF": return 0
    try:
        return float(v)
    except:
        return v

def sort_treeview(tv: ttk.Treeview, col: str, reverse_dict: dict):
    """Treeview tablosundaki sütunları alfabetik veya sayısal olarak sıralar."""
    data_list = []
    for cid in tv.get_children():
        vals = tv.item(cid, "values")
        col_idx = tv["columns"].index(col)
        data_list.append((cid, vals[col_idx]))
    
    curr_reverse = reverse_dict.get(col, False)
    data_list.sort(key=lambda x: to_float_safe(x[1]), reverse=curr_reverse)
    reverse_dict[col] = not curr_reverse
    for i, (cid, val) in enumerate(data_list):
        tv.move(cid, "", i)

# ------------------------- PARİTELER TABLOSU (Market verileri)
frame_pairs = ttk.LabelFrame(root, text="Aktif TRY Çiftleri / Pariteler")
frame_pairs.pack(fill="x", padx=10, pady=5)

cols_pairs = ("real_pair", "norm_pair", "last_price", "dailyPercent", "auto")
tree_pairs = ttk.Treeview(frame_pairs, columns=cols_pairs, show="headings", height=8)
tree_pairs.pack(side="left", fill="x", expand=True)

# Sütun başlıkları ve sıralama özellikleri
pairs_reverse_state = {}
for c in cols_pairs:
    tree_pairs.heading(c, text=c, command=lambda col=c: sort_treeview(tree_pairs, col, pairs_reverse_state))
    tree_pairs.column(c, width=100)

scroll_p = ttk.Scrollbar(frame_pairs, orient="vertical", command=tree_pairs.yview)
scroll_p.pack(side="right", fill="y")
tree_pairs.configure(yscrollcommand=scroll_p.set)

pairs_row_map = {}

def load_try_pairs():
    """Borsadaki tüm aktif Türk Lirası paritelerini listeler ve tabloya doldurur."""
    for rid in tree_pairs.get_children():
        tree_pairs.delete(rid)
    pairs_row_map.clear()
    try:
        resp = bt.get_ticker()
        dt = resp.get("data", [])
        for d in dt:
            rp = d["pair"]
            np = d["pairNormalized"]
            lp = d["last"]
            dd = d["dailyPercent"]
            # Sadece TRY ile biten pariteleri tabloya ekle
            if np.endswith("_TRY"):
                is_on = bot_state["auto_running"].get(rp, False)
                status = "ON" if is_on else "OFF"
                rid = tree_pairs.insert("", tk.END, values=(
                    rp, np, f"{float(lp):.4f}", f"{float(dd):.2f}", status
                ))
                pairs_row_map[rp] = rid
    except Exception as e:
        log_general(f"Pariteleri yüklerken hata: {e}")

# ------------------------- VARLIKLAR TABLOSU (Cüzdan Bakiyeleri)
frame_bal = ttk.LabelFrame(root, text="Cüzdan Varlıkları ve Maliyetler")
frame_bal.pack(fill="x", padx=10, pady=5)

cols_bal = ("asset", "balance", "locked", "free", "buy_price", "total_try", "auto")
tree_balances = ttk.Treeview(frame_bal, columns=cols_bal, show="headings", height=8)
tree_balances.pack(side="left", fill="x", expand=True)

balances_reverse_state = {}
for c in cols_bal:
    tree_balances.heading(c, text=c, command=lambda col=c: sort_treeview(tree_balances, col, balances_reverse_state))
    tree_balances.column(c, width=100)

scroll_b = ttk.Scrollbar(frame_bal, orient="vertical", command=tree_balances.yview)
scroll_b.pack(side="right", fill="y")
tree_balances.configure(yscrollcommand=scroll_b.set)

label_total_try = ttk.Label(frame_bal, text="Toplam Portföy Değeri (TRY): 0.0", font=("Helvetica", 10, "bold"))
label_total_try.pack(anchor="e", pady=3)

balances_row_map = {}

def parse_asset(pair_real):
    """Parite isminden coin sembolünü ayıklar (Örn: BTCTRY -> BTC)."""
    if pair_real.endswith("TRY"):
        return pair_real[:-3]
    elif pair_real.endswith("USDT"):
        return pair_real[:-4]
    return pair_real

def get_last_price(pair_real):
    """Verilen paritenin anlık son işlem fiyatını getirir."""
    try:
        resp = bt.get_ticker(pair_real)
        dt = resp.get("data", [])
        if not dt: return 0
        return float(dt[0]["last"])
    except:
        return 0

def get_coin_balance(asset):
    """Seçilen coin'in cüzdandaki toplam miktarını döner."""
    bals = bt.get_balances(nonzero=False)
    for x in bals:
        if x["asset"] == asset:
            return float(x["balance"])
    return 0.0

def show_my_balances():
    """Cüzdandaki sıfırdan büyük tüm coin varlıklarını, ortalama maliyetlerini ve TRY değerlerini listeler."""
    for rid in tree_balances.get_children():
        tree_balances.delete(rid)
    balances_row_map.clear()

    total_val = 0.0
    allb = bt.get_balances(nonzero=False)
    
    # Boştaki nakit TRY miktarını bul
    try_bal = 0.0
    for x in allb:
        if x["asset"] == "TRY":
            try_bal = float(x["balance"])
    total_val += try_bal

    # Diğer kripto varlıkları listele
    for item in allb:
        asset = item["asset"]
        bal = float(item["balance"])
        locked = float(item["locked"])
        free_amt = bal - locked
        if bal > 0.0 and asset != "TRY":
            buy_p = bot_state["avg_buy_price"].get(asset, 0.0)
            pair_real = asset + "TRY"
            lp = get_last_price(pair_real)
            val_try = lp * bal if lp > 0 else 0
            total_val += val_try
            
            is_on = bot_state["auto_running"].get(pair_real, False)
            status = "ON" if is_on else "OFF"
            
            rid = tree_balances.insert("", tk.END, values=(
                asset, f"{bal:.6f}", f"{locked:.6f}", f"{free_amt:.6f}",
                f"{buy_p:.4f}", f"{val_try:.2f}", status
            ))
            balances_row_map[asset] = rid

    label_total_try.config(text=f"Toplam Portföy Değeri: {total_val:.2f} TRY")

def update_pair_auto_status(rp, auto: bool):
    """Parite tablosundaki ON/OFF durum hücresini günceller."""
    if rp in pairs_row_map:
        rid = pairs_row_map[rp]
        vals = list(tree_pairs.item(rid)["values"])
        vals[4] = "ON" if auto else "OFF"
        tree_pairs.item(rid, values=vals)

def update_balance_auto_status(asset, auto: bool):
    """Varlık tablosundaki ON/OFF durum hücresini günceller."""
    if asset in balances_row_map:
        rid = balances_row_map[asset]
        vals = list(tree_balances.item(rid)["values"])
        vals[6] = "ON" if auto else "OFF"
        tree_balances.item(rid, values=vals)

def get_selected_balance_asset():
    """Varlık tablosunda seçili olan coin sembolünü döner."""
    sel = tree_balances.selection()
    if not sel: return None
    vals = tree_balances.item(sel[0])["values"]
    return vals[0]

def auto_refresh_balances():
    """Her 40 saniyede bir varlık listesini ve portföy değerini günceller."""
    show_my_balances()
    root.after(40000, auto_refresh_balances)

# Program başlarken tabloları yükle
auto_refresh_balances()

# ------------------------- MANUAL SATIŞ İŞLEMLERİ
def sell_selected_coin():
    """Varlık listesinde seçili olan kripto paranın tamamını anında market fiyatından satar."""
    asset = get_selected_balance_asset()
    if not asset:
        messagebox.showwarning("Uyarı", "Seçili coin yok.")
        return
    if asset == "TRY":
        messagebox.showinfo("Bilgi", "Türk Lirası satılamaz.")
        return
    qty = get_coin_balance(asset)
    if qty < 0.00001:
        messagebox.showinfo("Bilgi", "Satılacak bakiye yetersiz.")
        return
    pair = asset + "TRY"
    try:
        resp = bt.market_sell(pair, qty)
        log_sell(f"Manuel Satış => {asset}, Miktar: {qty:.6f}, Cevap: {resp}")
        bot_state["avg_buy_price"][asset] = 0.0
        save_state()
        show_my_balances()
    except Exception as e:
        log_general(f"{asset} satılırken hata: {e}")

def sell_all_coins():
    """Cüzdandaki (TRY hariç) tüm coin varlıklarını tek tuşla anında piyasadan satar."""
    allb = bt.get_balances(nonzero=False)
    for x in allb:
        asset = x["asset"]
        if asset == "TRY":
            continue
        bal = float(x["balance"])
        if bal > 0.00001:
            pair = asset + "TRY"
            try:
                resp = bt.market_sell(pair, bal)
                log_sell(f"Toplu Satış => {asset}, Miktar: {bal:.6f}, Cevap: {resp}")
                bot_state["avg_buy_price"][asset] = 0.0
            except Exception as ex:
                log_general(f"{asset} toplu satışında hata: {ex}")
    save_state()
    show_my_balances()

# -----------------------------------------------------------------------------
# OTOMATİK TİCARET ALGORİTMASI (5 DAKİKA GÖZLEM + ORANSAL AL-SAT)
# -----------------------------------------------------------------------------
def auto_trade(pair_real, pair_norm):
    """
    Otomatik al-sat algoritması ana döngüsü.
    
    Çalışma Prensibi:
    1. 5 Dakikalık Gözlem: 300 saniye boyunca her 10 saniyede bir fiyat sorgulanır.
       Bu 5 dakika içindeki en düşük (min) fiyat tespit edilir.
    2. Alım Kararı: 5 dakika sonunda anlık fiyat üzerinden, belirlenen bakiye
       oranıyla market alışı gerçekleştirilir. Alım maliyeti kaydedilir.
    3. Takip & Satış: Her 5 saniyede bir fiyat takip edilir. Fiyat, maliyetin
       '%hedef kâr oranı' kadar üzerine çıktığında anında market satışı yapılır.
    4. Satışın ardından döngü başa döner.
    """
    bot_state["auto_running"][pair_real] = True
    save_state()
    log_general(f"{pair_norm} => Otomatik Al-Sat başladı. İlk 5 dakikalık gözlem devrede...")

    update_pair_auto_status(pair_real, True)
    asset = parse_asset(pair_real)
    update_balance_auto_status(asset, True)

    # 5 Dakikalık Fiyat Toplama Döngüsü
    observe_prices = []
    t0 = time.time()
    while time.time() - t0 < 300:
        if not bot_state["auto_running"].get(pair_real, False):
            break
        dt = bt.get_ticker(pair_real).get("data", [])
        if dt:
            price_now = float(dt[0]["last"])
            observe_prices.append(price_now)
            log_general(f"{pair_norm} [Gözlem] Fiyat: {price_now:.4f} | Örnek: {len(observe_prices)}/30")
        time.sleep(10)

    # Gözlem verisi yoksa sonlandır
    if not observe_prices:
        log_general(f"{pair_norm} => Gözlem verisi alınamadığından bot sonlandırıldı.")
        bot_state["auto_running"][pair_real] = False
        save_state()
        update_pair_auto_status(pair_real, False)
        update_balance_auto_status(asset, False)
        return

    min_price = min(observe_prices)
    max_price = max(observe_prices)
    log_general(f"{pair_norm} => Gözlem Bitti. En Düşük: {min_price:.4f}, En Yüksek: {max_price:.4f}")

    # Kullanıcının belirlediği oranları al
    ratio = get_sell_ratio()     
    purchase_pct = get_purchase_ratio()

    # Kullanıcı gözlem sürerken botu kapatmış mı kontrolü
    if not bot_state["auto_running"].get(pair_real, False):
        log_general(f"{pair_norm} => Bot kapatıldığı için alım iptal edildi.")
        update_pair_auto_status(pair_real, False)
        update_balance_auto_status(asset, False)
        return

    # Hesap bakiyesi kontrolü
    bals = bt.get_balances(nonzero=False)
    try_val = 0.0
    for b in bals:
        if b["asset"] == "TRY":
            try_val = float(b["balance"])
            break
            
    if try_val < 10:
        log_general(f"{pair_norm} => TRY bakiyesi yetersiz (Min: 10 TRY). Otomatik işlem iptal edildi.")
        bot_state["auto_running"][pair_real] = False
        update_pair_auto_status(pair_real, False)
        update_balance_auto_status(asset, False)
        return

    # Belirlenen yüzde oranında TRY ile Market Alışı yap
    amt = try_val * (purchase_pct / 100.0)
    try:
        resp_buy = bt.market_buy(pair_real, amt)
        new_price = float(bt.get_ticker(pair_real).get("data", [{"last": "0"}])[0]["last"])
        bot_state["avg_buy_price"][asset] = new_price
        save_state()
        log_buy(f"{pair_norm} => Alım Yapıldı. Tutar: {amt:.2f} TRY | Alış Fiyatı: {new_price:.4f} | Gözlem Min: {min_price:.4f}")
    except Exception as e:
        log_general(f"{pair_norm} => Alım işleminde hata: {e}")
        bot_state["auto_running"][pair_real] = False
        update_pair_auto_status(pair_real, False)
        update_balance_auto_status(asset, False)
        return

    buy_price = new_price

    # Fiyat Takip ve Satış Döngüsü
    try:
        while bot_state["auto_running"].get(pair_real, False):
            time.sleep(5)
            dt2 = bt.get_ticker(pair_real).get("data", [])
            if not dt2:
                continue
            current_price = float(dt2[0]["last"])

            # Kâr hedefi hesaplanıyor
            target = buy_price * (1 + ratio / 100.0)
            if current_price >= target:
                coin_bal = get_coin_balance(asset)
                if coin_bal > 0.00001:
                    try:
                        resp_sell = bt.market_sell(pair_real, coin_bal)
                        log_sell(f"{pair_norm} => Hedef kâr (%{ratio}) gerçekleşti. Miktar: {coin_bal:.6f} | Satış Fiyatı: {current_price:.4f}")
                        bot_state["avg_buy_price"][asset] = 0.0
                        save_state()
                        break  # Al-Sat döngüsü tamamlandı, bot kapatılır veya tekrar gözleme başlar
                    except Exception as ex:
                        log_general(f"{pair_norm} => Satış hatası: {ex}")
                        bot_state["auto_running"][pair_real] = False
                        break
                else:
                    log_general(f"{pair_norm} => Satılacak bakiye bulunamadığından durduruldu.")
                    bot_state["auto_running"][pair_real] = False
                    break
            else:
                log_general(f"{pair_norm} => Beklemede | Alış: {buy_price:.4f} | Güncel: {current_price:.4f} | Hedef: {target:.4f}")
    finally:
        bot_state["auto_running"][pair_real] = False
        save_state()
        update_pair_auto_status(pair_real, False)
        update_balance_auto_status(asset, False)
        log_general(f"{pair_norm} => Otomatik döngü sonlandırıldı.")

# ------------------------- OTOMATİK BAŞLAT / DURDUR TETİKLEYİCİLERİ
def start_auto_trade_pair():
    """Seçilen parite için otomatik gözlem ve al-sat sürecini arka planda başlatır."""
    sel = tree_pairs.selection()
    if not sel:
        messagebox.showwarning("Uyarı", "Tablodan bir parite seçmelisiniz.")
        return
    vals = tree_pairs.item(sel[0])["values"]
    rp = vals[0]
    np = vals[1]
    if bot_state["auto_running"].get(rp, False):
        messagebox.showinfo("Bilgi", f"{np} için bot zaten çalışıyor.")
        return
    t = threading.Thread(target=auto_trade, args=(rp, np), daemon=True)
    t.start()

def stop_auto_trade_pair():
    """Seçilen parite için aktif olan otomatik ticaret sürecini durdurur."""
    sel = tree_pairs.selection()
    if not sel:
        messagebox.showwarning("Uyarı", "Tablodan bir parite seçmelisiniz.")
        return
    vals = tree_pairs.item(sel[0])["values"]
    rp = vals[0]
    np = vals[1]
    if not bot_state["auto_running"].get(rp, False):
        messagebox.showinfo("Bilgi", f"{np} zaten durdurulmuş.")
        return
    bot_state["auto_running"][rp] = False
    save_state()
    log_general(f"{np} => Otomatik durduruluyor...")
    update_pair_auto_status(rp, False)
    asset = parse_asset(rp)
    update_balance_auto_status(asset, False)

def start_auto_from_balance():
    """Varlık listesinde seçili olan coin için otomatik al-sat sürecini başlatır."""
    asset = get_selected_balance_asset()
    if not asset:
        messagebox.showwarning("Uyarı", "Varlık listesinden bir coin seçmelisiniz.")
        return
    if asset == "TRY":
        messagebox.showinfo("Bilgi", "Türk Lirası için otomatik bot başlatılamaz.")
        return
    rp = asset + "TRY"
    if bot_state["auto_running"].get(rp, False):
        messagebox.showinfo("Bilgi", f"{rp} için bot zaten aktif.")
        return
    np = asset + "_TRY"
    t = threading.Thread(target=auto_trade, args=(rp, np), daemon=True)
    t.start()

def stop_auto_from_balance():
    """Varlık listesinde seçili olan coin için otomatik botu durdurur."""
    asset = get_selected_balance_asset()
    if not asset:
        messagebox.showwarning("Uyarı", "Varlık listesinden bir coin seçmelisiniz.")
        return
    if asset == "TRY":
        messagebox.showinfo("Bilgi", "Türk Lirası için otomatik bot bulunmamaktadır.")
        return
    rp = asset + "TRY"
    if not bot_state["auto_running"].get(rp, False):
        messagebox.showinfo("Bilgi", f"{rp} zaten aktif değil.")
        return
    bot_state["auto_running"][rp] = False
    save_state()
    log_general(f"{rp} => Otomatik bot durduruluyor...")
    update_pair_auto_status(rp, False)
    update_balance_auto_status(asset, False)

def reinit_auto_threads():
    """Uygulama açıldığında, eğer geçmişte yarım kalmış aktif botlar varsa onları yeniden başlatır."""
    for pr, onoff in bot_state["auto_running"].items():
        if onoff:
            asset = parse_asset(pr)
            np = asset + "_TRY"
            t = threading.Thread(target=auto_trade, args=(pr, np), daemon=True)
            t.start()

# Açılıştan 1 saniye sonra aktif botları canlandır
root.after(1000, reinit_auto_threads)

def on_closing():
    """Pencere kapatılırken son log ve durum verilerini dosyaya kaydeder."""
    log_general("Uygulama kapatılıyor. Durumlar kaydedildi.")
    save_state()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# ------------------- KONTROL PANELİ BUTONLARI VE GRID LAYOUT
frame_actions = ttk.Frame(root)
frame_actions.pack(fill="x", pady=5)

btn_pairs_refresh = ttk.Button(frame_actions, text="Pariteleri Yenile", command=load_try_pairs)
btn_pairs_refresh.grid(row=0, column=0, padx=5)

btn_bal_refresh = ttk.Button(frame_actions, text="Varlıklar Yenile", command=show_my_balances)
btn_bal_refresh.grid(row=0, column=1, padx=5)

btn_sel_sell = ttk.Button(frame_actions, text="Seçili Coin'i Sat", command=sell_selected_coin)
btn_sel_sell.grid(row=0, column=2, padx=5)

btn_all_sell = ttk.Button(frame_actions, text="Tüm Coinleri Sat", command=sell_all_coins)
btn_all_sell.grid(row=0, column=3, padx=5)

btn_auto_parite_start = ttk.Button(frame_actions, text="Auto (Parite) Start", command=start_auto_trade_pair)
btn_auto_parite_start.grid(row=0, column=4, padx=5)

btn_auto_parite_stop = ttk.Button(frame_actions, text="Auto (Parite) Stop", command=stop_auto_trade_pair)
btn_auto_parite_stop.grid(row=0, column=5, padx=5)

btn_auto_bal_start = ttk.Button(frame_actions, text="Auto (Varlık) Start", command=start_auto_from_balance)
btn_auto_bal_start.grid(row=0, column=6, padx=5)

btn_auto_bal_stop = ttk.Button(frame_actions, text="Auto (Varlık) Stop", command=stop_auto_from_balance)
btn_auto_bal_stop.grid(row=0, column=7, padx=5)

# Pariteleri ilk yükleme
load_try_pairs()

root.mainloop()
