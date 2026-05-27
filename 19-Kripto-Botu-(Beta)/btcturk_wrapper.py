# =============================================================================
# BTCTurk REST API Wrapper / Sarmalayıcı Sınıfı (btcturk_wrapper.py)
# =============================================================================
# Bu sınıf, BTCTurk borsasının API'si ile haberleşmek, kimlik doğrulama imzaları
# (HMAC-SHA256) oluşturmak, istek göndermek ve sipariş / bakiye işlemlerini
# kolayca yapmak için yazılmış bir sarmalayıcı (wrapper) kütüphanedir.
# =============================================================================

import requests
import base64
import time
import hashlib
import hmac
from endpoints import ENDPOINTS

# BTCTurk Rest API ve Websocket temel adresleri
base = "https://api.btcturk.com"
base_ws = "wss://ws-feed-pro.btcturk.com"

class BTCTurk:
    def __init__(self, apiKey: str, apiSecret: str):
        """
        BTCTurk API Nesnesini başlatır ve borsa sembol bilgilerini önbelleğe alır.
        
        Parametreler:
        - apiKey (str): BTCTurk hesabınızdan oluşturduğunuz Public Key.
        - apiSecret (str): BTCTurk hesabınızdan oluşturduğunuz Private/Secret Key (Base64 formatında).
        """
        self.apiKey = apiKey
        # BtcTurk API'si Secret Key'i Base64 ile decode edilmiş olarak bekler.
        try:
            self.apiSecret = base64.b64decode(apiSecret)
        except Exception as e:
            raise ValueError(
                "Secret Key (Private Key) geçerli bir Base64 formatı olmalıdır! "
                "Eğer anahtarları henüz girmediyseniz lütfen girin."
            ) from e

        # Borsadaki tüm çiftlerin kurallarını (hassasiyet, limit vb.) çekip saklıyoruz.
        self.symbols = {}
        self.exchange_info = self.get_exchange_info()["data"]

        # Aktif coin çiftlerinin minimum sipariş fiyatlarını ve basamak limitlerini önbelleğe alalım.
        for e in self.exchange_info["symbols"]:
            digit = e["denominatorScale"]
            # minimumLimitOrderPrice * 10 formülüyle tahmini bir başlangıç limit fiyatı ayarlanıyor.
            e["price"] = self.round_pair(pair="", val=e["minimumLimitOrderPrice"] * 10, digit=digit)
            self.symbols[e["name"]] = e

    def qty_check(self, pair: str, qty: float) -> bool:
        """
        Verilen miktarın, ilgili paritenin minimum işlem hacim filtresini (minExchangeValue)
        karşılayıp karşılamadığını kontrol eder.
        """
        min_val = float(self.symbols[pair]["filters"][0]["minExchangeValue"])
        last_price = float(self.symbols[pair]["price"])
        val = qty * last_price
        return val >= min_val

    def round_pair(self, pair: str, val: float, digit: int = 0) -> float:
        """
        Verilen float değeri paritenin hassasiyet kurallarına göre aşağı doğru yuvarlar.
        
        Parametreler:
        - pair (str): Yuvarlanacak parite adı (örn: BTC_TRY). Boş ise 'digit' parametresi kullanılır.
        - val (float): Yuvarlanacak sayısal değer.
        - digit (int): Parite verilmediğinde kullanılacak basamak sayısı.
        """
        if pair == "":
            numeratorScale = digit
        else:
            numeratorScale = self.symbols[pair]["numeratorScale"]
        dgt = 10 ** numeratorScale
        return int(val * dgt) / dgt

    def numerator_scale(self, pair: str, val: float) -> float:
        """Kripto para miktarı (pay) basamak hassasiyetine göre yuvarlar."""
        numeratorScale = self.symbols[pair]["numeratorScale"]
        dgt = 10 ** numeratorScale
        return int(val * dgt) / dgt

    def denominator_scale(self, pair: str, val: float) -> float:
        """İtibari para miktarı (payda) basamak hassasiyetine göre yuvarlar (TRY/USDT cinsinden)."""
        denominatorScale = self.symbols[pair]["denominatorScale"]
        dgt = 10 ** denominatorScale
        return int(val * dgt) / dgt

    def send(self, cmd: str, act: str = "", payload: dict = None, order_id: int = 0) -> dict:
        """
        BTCTurk API'sine kimlik doğrulamalı (imzalı) istek gönderen temel fonksiyondur.
        
        BTCTurk API İmzası Oluşturma:
        1. API Anahtarı ve milisaniye cinsinden zaman damgası (Stamp) birleştirilir.
        2. Bu metin, Base64 decode edilmiş Secret Key ile HMAC-SHA256 algoritması kullanılarak imzalanır.
        3. Oluşan imza Base64 formatına çevrilerek HTTP başlığına (X-Signature) eklenir.
        """
        # Milisaniye cinsinden zaman damgası oluşturma
        stamp = str(int(time.time()) * 1000)
        data = "{}{}".format(self.apiKey, stamp).encode("utf-8")
        
        # HMAC-SHA256 imzası oluşturuluyor
        signature = hmac.new(self.apiSecret, data, hashlib.sha256).digest()
        signature = base64.b64encode(signature)

        # Gerekli HTTP Başlıkları
        headers = {
            "X-PCK": self.apiKey,
            "X-Stamp": stamp,
            "X-Signature": signature,
            "Content-Type": "application/json"
        }

        # endpoints.py dosyasındaki sözlükten endpoint ayarlarını çekiyoruz.
        e = ENDPOINTS[cmd]
        ep = e["ep"]
        t = e["type"]
        
        # Eğer endpoint'in özel bir base URL'i varsa (örn: graph-api) onu kullan, yoksa varsayılanı al.
        if "base" in e:
            host = e["base"]
        else:
            host = base
        url = f"{host}{ep}"

        # URL parametreleri (Query string) veya dinamik ID ekleme
        if act != "":
            if cmd == "order" and t == "GET":
                # Örn: /api/v1/order/12345
                url += "/" + act
            else:
                # Örn: /api/v1/allOrders?pairSymbol=BTC_TRY
                url += "?" + act

        # HTTP metot tipine göre requests üzerinden çağrı yapıyoruz
        if t == "GET":
            r = requests.get(url, headers=headers)
        elif t == "POST":
            r = requests.post(url, headers=headers, json=payload)
        elif t == "DELETE":
            r = requests.delete(url, headers=headers)
        else:
            return {}

        return r.json()

    def get_balances(self, nonzero: bool = True) -> list:
        """
        Kullanıcı cüzdanındaki tüm bakiyeleri sorgular.
        - nonzero (bool): True ise sadece bakiyesi 0'dan büyük olan varlıkları getirir.
        """
        r = self.send("balances")
        b = r["data"]
        if nonzero:
            return [s for s in b if float(s["balance"]) > 0.0]
        else:
            return b

    def get_ticker_currency(self, pair: str = "") -> dict:
        """Belirtilen kripto para birimi bazında (V2) anlık piyasa fiyat detaylarını sorgular."""
        act = ""
        if pair != "":
            act = f"symbol={pair}"
        return self.send("ticker_currency", act)

    def get_ticker(self, pair: str = "") -> dict:
        """
        Borsadaki tüm paritelerin veya belirli bir paritenin piyasa özetini (V2) getirir.
        Örn: pair='BTC_TRY' derseniz sadece o çiftin verisi gelir.
        """
        act = ""
        if pair:
            act = f"pairSymbol={pair}"
        return self.send("ticker", act)

    def get_open_orders(self, pair: str = "") -> dict:
        """Kullanıcının aktif olarak bekleyen (açık) limit emirlerini listeler."""
        act = ""
        if pair != "":
            act = f"pairSymbol={pair}"
        return self.send("open_orders", act)

    def get_exchange_info(self) -> dict:
        """BTCTurk borsasındaki tüm çiftlerin genel kurallarını ve limit detaylarını döner."""
        return self.send("exchange_info")

    def submit_order(self, pair: str, price: float, qty: float, orderType: str, orderMethod: str, stopPrice: float = 0.0) -> dict:
        """
        API'ye yeni alım/satım emri göndermek için parametreleri hazırlayan ortak metottur.
        
        Parametreler:
        - pair (str): İşlem yapılacak parite (örn: BTC_TRY).
        - price (float): Limit emrin fiyatı (market emirlerde 0.0).
        - qty (float): Alınacak/satılacak miktar (market buy için harcanacak TRY miktarı).
        - orderType (str): 'buy' veya 'sell'.
        - orderMethod (str): 'limit' veya 'market'.
        - stopPrice (float): Varsa stop-limit emrinin tetiklenme fiyatı.
        """
        # Market buy emirlerinde miktar coin cinsinden değil, harcanacak itibari para (TRY) cinsindendir.
        if orderMethod == "market" and orderType == "buy":
            val = self.denominator_scale(pair, qty)
        else:
            val = self.numerator_scale(pair, qty)

        payload = {
            "quantity": val,
            "newOrderClientId": "BtcTurk API Wrapper",
            "orderMethod": orderMethod,
            "orderType": orderType,
            "pairSymbol": pair
        }

        if price > 0.0:
            payload["price"] = price
        if stopPrice > 0.0:
            payload["stopPrice"] = stopPrice

        return self.send("new_order", payload=payload)

    def limit_buy(self, pair: str, price: float, qty: float) -> dict:
        """Belirtilen fiyattan Limit Alış emri gönderir."""
        return self.submit_order(pair, price, qty, orderMethod="limit", orderType="buy")

    def limit_sell(self, pair: str, price: float, qty: float) -> dict:
        """Belirtilen fiyattan Limit Satış emri gönderir."""
        return self.submit_order(pair, price, qty, orderMethod="limit", orderType="sell")

    def market_buy(self, pair: str, amount: float) -> dict:
        """Piyasa fiyatından belirtilen tutarda (TRY/USDT) Market Alış emri gönderir."""
        return self.submit_order(pair, price=0.0, qty=amount, orderMethod="market", orderType="buy")

    def market_sell(self, pair: str, qty: float) -> dict:
        """Piyasa fiyatından belirtilen miktarda coin için Market Satış emri gönderir."""
        return self.submit_order(pair, price=0.0, qty=qty, orderMethod="market", orderType="sell")
