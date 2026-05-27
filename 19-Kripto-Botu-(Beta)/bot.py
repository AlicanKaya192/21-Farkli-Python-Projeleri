# =============================================================================
# BTCTurk API Bağlantı Test Scripti (bot.py)
# =============================================================================
# Bu script, yazılan BTCTurk API sarmalayıcısının (wrapper) ve girilen API 
# anahtarlarının düzgün çalışıp çalışmadığını test etmek için kullanılan basit
# bir konsol (terminal) uygulaması örneğidir.
# =============================================================================

from btcturk_wrapper import BTCTurk
import json

# -----------------------------------------------------------------------------
# API ANAHTARLARI: BtcTurk web sitesinden aldığınız API Key ve Secret Key 
# bilgilerini aşağıdaki değişkenlerin içerisine tırnak içinde yapıştırın.
# -----------------------------------------------------------------------------
public_key = "BURALARA APİ ANAHTARLARINI YAZINIZ"
private_key = "BURALARA APİ ANAHTARLARINI YAZINIZ"

# API Anahtarlarının doldurulup doldurulmadığını kontrol edelim
is_keys_placeholder = (
    "APİ" in public_key or "YAZINIZ" in public_key or
    "APİ" in private_key or "YAZINIZ" in private_key or
    not public_key.strip() or not private_key.strip()
)

if is_keys_placeholder:
    print("=============================================================================")
    print("UYARI: API Anahtarları yapılandırılmamış!")
    print("Lütfen bot.py dosyasının 16. ve 17. satırlarındaki public_key ve private_key")
    print("değerlerini kendi BtcTurk API anahtarlarınız ile güncelleyin.")
    print("=============================================================================")
    import sys
    sys.exit(1)

try:
    # Wrapper sınıfından (BTCTurk) bir örnek nesne türetelim.
    # Bu başlatma (initialization) anında borsa sembol bilgileri otomatik olarak sorgulanır.
    bt = BTCTurk(apiKey=public_key, apiSecret=private_key)
except Exception as e:
    print("=============================================================================")
    print("HATA: API Anahtarları başlatılırken bir sorun oluştu!")
    print(f"Hata detayı: {e}")
    print("Lütfen anahtarları doğru şekilde girdiğinizden emin olun.")
    print("=============================================================================")
    import sys
    sys.exit(1)

# -----------------------------------------------------------------------------
# TEST İŞLEMİ:
# BTCTurk API üzerinden USDT (Tether) kripto parasının güncel fiyat ve piyasa 
# özet verilerini (ticker) sorguluyoruz.
# -----------------------------------------------------------------------------
d = bt.get_ticker_currency("USDT")

# Çekilen karmaşık sözlük (dictionary) verisini, konsolda daha okunaklı (pretty-print) 
# görüntüleyebilmek için json.dumps yardımıyla 2 birim girintili JSON biçimine çevirip basıyoruz.
print(json.dumps(d, indent=2))
