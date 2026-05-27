# =============================================================================
# BTCTurk API Endpoint Tanımlamaları (endpoints.py)
# =============================================================================
# Bu dosya, BTCTurk borsasının API'sine yapılacak HTTP isteklerinin endpoint
# yollarını, HTTP metot tiplerini (GET/POST/DELETE) ve BtcTurk API anahtarı
# için gereken yetkilendirme (izin) seviyelerini tanımlar.
# =============================================================================

ENDPOINTS = {
    # Hesap Bakiye Bilgileri: Kullanıcının cüzdanındaki tüm TRY ve kripto varlık miktarlarını çeker.
    # Yetki: "Total Funds" (Toplam Varlık) izni gereklidir.
    "balances": {
        "ep": "/api/v1/users/balances",
        "type": "GET",
        "permission": "Total Funds (Toplam Varlık)"
    },
    # Geçmiş Emirler Listesi: Tüm tamamlanmış veya iptal edilmiş emirlerin geçmişini çeker.
    # Yetki: "Trade" (Al-Sat) izni gereklidir.
    "all_orders": {
        "ep": "/api/v1/allOrders",
        "type": "GET",
        "permission": "Trade (Al-Sat)"
    },
    # Tekil Emir Sorgulama: ID'si belirtilen belirli bir emrin güncel durumunu çeker.
    # Yetki: "Trade" (Al-Sat) izni gereklidir.
    "order": {
        "ep": "/api/v1/order",
        "type": "GET",
        "permission": "Trade (Al-Sat)"
    },
    # Emir İptal Etme: Açık bir emri iptal etmek için kullanılır (HTTP DELETE metodu).
    # Yetki: "Trade" (Al-Sat) izni gereklidir.
    "cancel_order": {
        "ep": "/api/v1/order",
        "type": "DELETE",
        "permission": "Trade (Al-Sat)"
    },
    # Yeni Emir Gönderme: Alış veya satış emri (Limit/Market) oluşturmak için kullanılır (HTTP POST metodu).
    # Yetki: "Trade" (Al-Sat) izni gereklidir.
    "new_order": {
        "ep": "/api/v1/order",
        "type": "POST",
        "permission": "Trade (Al-Sat)"
    },
    # Güncel Açık Emirler: Henüz gerçekleşmemiş (bekleyen) tüm açık emirleri listeler.
    # Yetki: "Trade" (Al-Sat) izni gereklidir.
    "open_orders": {
        "ep": "/api/v1/openOrders",
        "type": "GET",
        "permission": "Trade (Al-Sat)"
    },
    # Kullanıcı Al-Sat İşlemleri: Gerçekleşmiş olan tüm işlemlerin (trade history) dökümünü alır.
    # Yetki: "Account" (Hesap) izni gereklidir.
    "get_trades": {
        "ep": "/api/v1/users/transactions/trade",
        "type": "GET",
        "permission": "Account (Hesap)"
    },
    # İtibari Para (Fiat) Hareketleri: TRY yatırma/çekme geçmişi işlemlerini sorgular.
    # Yetki: "Account" (Hesap) izni gereklidir.
    "get_fiats": {
        "ep": "/api/v1/users/transactions/fiat",
        "type": "GET",
        "permission": "Account (Hesap)"
    },
    # Kripto Para Yatırma/Çekme Hareketleri: Kripto para transfer geçmişi işlemlerini sorgular.
    # Yetki: "Account" (Hesap) izni gereklidir.
    "get_cryptos": {
        "ep": "/api/v1/users/transactions/crypto",
        "type": "GET",
        "permission": "Account (Hesap)"
    },
    # Borsa Genel Bilgileri (v2): Borsadaki aktif semboller, basamak hassasiyetleri, min limit fiyatları vb.
    # Genel Bilgi (Herkese Açık) - İzin/Kimlik Doğrulama gerekmez.
    "exchange_info": {
        "ep": "/api/v2/server/exchangeinfo",
        "type": "GET",
        "version": "v2",
        "permission": ""
    },
    # Günlük Ticker Fiyat Özetleri (v2): Son fiyat, 24 saatlik değişim yüzdesi, hacim vb. veriler.
    # Genel Bilgi (Herkese Açık) - İzin/Kimlik Doğrulama gerekmez.
    "ticker": {
        "ep": "/api/v2/ticker",
        "type": "GET",
        "version": "v2",
        "permission": ""
    },
    # Kripto Para Bazlı Fiyat Bilgisi (v2): Belirli kripto para birimleri bazında ticker bilgilerini getirir.
    # Genel Bilgi (Herkese Açık) - İzin/Kimlik Doğrulama gerekmez.
    "ticker_currency": {
        "ep": "/api/v2/ticker/currency",
        "type": "GET",
        "version": "v2",
        "permission": ""
    },
    # Tahta Derinliği / Emir Defteri (v2): Alış ve satış tekliflerinin kademeli listesini getirir.
    # Genel Bilgi (Herkese Açık) - İzin/Kimlik Doğrulama gerekmez.
    "orderbook": {
        "ep": "/api/v2/orderbook",
        "type": "GET",
        "version": "v2",
        "permission": ""
    },
    # Son Gerçekleşen İşlemler (v2): Borsada gerçekleşen en son genel alım-satım işlemlerini sorgular.
    # Genel Bilgi (Herkese Açık) - İzin/Kimlik Doğrulama gerekmez.
    "trades": {
        "ep": "/api/v2/trades",
        "type": "GET",
        "version": "v2",
        "permission": ""
    },
    # Grafik Mum Verileri (OHLC): Grafik çizimi için Açılış-Yüksek-Düşük-Kapanış verilerini getirir.
    # Farklı bir alt alan adı (graph-api) kullanır.
    "ohlcs": {
        "ep": "/v1/ohlcs",
        "type": "GET",
        "permission": "",
        "base": "https://graph-api.btcturk.com"
    },
    # TradingView Mum Geçmişi: TradingView kütüphanesiyle uyumlu grafik geçmiş verileri.
    # Farklı bir alt alan adı (graph-api) kullanır.
    "klines": {
        "ep": "/v1/klines/history",
        "type": "GET",
        "permission": "",
        "base": "https://graph-api.btcturk.com"
    }
}
