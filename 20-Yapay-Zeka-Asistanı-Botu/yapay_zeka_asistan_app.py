# =============================================================================
# Proje #20: Yapay Zeka Asistanı Botu (Alican Kaya Dijital İkizi)
# =============================================================================
# Bu proje, Flask web çatısı ve Google Gemini API (google-generativeai) kütüphanesi
# kullanarak oluşturulmuş, Alican Kaya'nın projelerini, yeteneklerini ve özgeçmişini
# tanıtan, oturum (session) bazlı çalışan interaktif bir web sohbet botu (chat bot)
# uygulamasıdır.
# =============================================================================

# ---- Kütüphanelerin İçe Aktarılması ----
from flask import Flask, render_template, request, session, redirect, url_for
import os
import contextlib

# stderr yönlendirmesi ile gRPC/Protobuf ve google-generativeai kütüphanesinin
# import aşamasında konsola bastırdığı uyarı loglarını bastırıyoruz.
with open(os.devnull, 'w') as devnull, contextlib.redirect_stderr(devnull):
    import google.generativeai as genai

# ---- Flask Uygulamasının Başlatılması ----
app = Flask(__name__)
# Flask üzerinde oturum (session) verilerini şifrelemek ve güvenli bir şekilde
# istemci tarafında (cookie) saklamak için gizli bir anahtar (secret key) tanımlıyoruz.
app.secret_key = "your_secret_key_here"  

# =============================================================================
# API CONFIGURATION & KEY DEFINITION
# =============================================================================
# API anahtarını doğrudan kod içine yazmak isterseniz bu değişkeni güncelleyin.
# Eğer değiştirilmezse, uygulama sırasıyla Çevre Değişkenini (GEMINI_API_KEY)
# veya HTML arayüzünden kullanıcının girdiği session API anahtarını kullanacaktır.
API_KEY_IN_CODE = "BURAYA APİ KEYİNİ GİR"

# =============================================================================
# GEMINI MODEL GENERATION CONFIGURATION
# =============================================================================
# Yapay zeka modelinin yanıt verme davranışlarını ve sınırlarını belirleyen yapılandırma.
generation_config = {
    "temperature": 1,           # Rastgelelik derecesi (1 = dengeli ve yaratıcı, düşük değerler daha tutarlı)
    "top_p": 0.95,              # Çekirdek örnekleme oranı (%95 ihtimalli kelimeleri seçer)
    "top_k": 40,                # Her adımda en yüksek ihtimalli 40 kelime arasından seçim sınırlandırması
    "max_output_tokens": 8192,  # Üretilecek maksimum yanıt uzunluğu (token cinsi)
    "response_mime_type": "text/plain", # Çıktı formatı (düz metin)
}

# =============================================================================
# CORPORATE IDENTITY & SYSTEM INSTRUCTION
# =============================================================================
# Modelin nasıl davranması gerektiğini, kim olduğunu ve hangi bilgileri sunması
# gerektiğini belirten kurumsal talimat metni. Bu metin her mesajda arka planda
# modele 'system_instruction' olarak iletilir.
corporate_text = (
    "Ben, Yapay Zeka Mühendisi ve Veri Bilimi Öğrencisi Alican Kaya'nın dijital ikiziyim (yani kendisiyim). "
    "Ziyaretçilere kendi projelerin, yeteneklerin, blog yazıların ve çalışma alanların hakkında birinci tekil şahıs ('ben', 'benim') olarak bilgi ver.\n\n"
    "Kendi Hakkında Bilgiler:\n"
    "- Çalışma Alanlarım: Yapay Zeka (AI), Veri Bilimi (Data Science), Makine Öğrenmesi (Machine Learning) ve Derin Öğrenme (Deep Learning).\n"
    "- Neler Yapıyorum: Web ve masaüstü bilgisayar uygulamaları geliştiriyorum, kullanıcı odaklı ve estetik arayüz tasarımlarına önem veriyorum.\n"
    "- Teknik Yeteneklerim (Stack):\n"
    "  * Programlama Dilleri: Python (Pandas, NumPy, Scikit-learn, Flask vb. kütüphaneler), C++, C#, SQL ve temel frontend teknolojileri.\n"
    "  * Araçlar & Kütüphaneler: TensorFlow, PyTorch, Git, Jupyter Notebook, VS Code.\n"
    "- Öne Çıkan Projelerim:\n"
    "  * \"21 Farklı Python Projesi\" (Şu anda incelediğin bu sohbet botu projesi de dahil olmak üzere; veri çekme botları, görüntü işleme araçları, driver bulucular ve kripto botları barındıran kapsamlı bir GitHub deposu).\n"
    "  * \"Data Science RoadMap\" (Sıfırdan ileri seviyeye veri bilimi yol haritam).\n"
    "  * \"AI Jobs Market Analysis\" (Yapay Zeka iş dünyası ve istihdam trendleri veri analizi projem).\n"
    "  * \"World Happiness Report Analysis\" (Dünya Mutluluk Raporu verilerini görselleştirdiğim ve incelediğim çalışmam).\n"
    "- Sosyal Medya & İletişim Kanallarım:\n"
    "  * GitHub: github.com/AlicanKaya192\n"
    "  * Kişisel Web Sitem: alican-kaya.com\n"
    "  * Medium Blogum: medium.com/@alicankaya268 (Yapay zeka iş trendleri ve veri analitiği üzerine yazılar yazıyorum).\n\n"
    "Kurallar ve Davranış Tarzı:\n"
    "1. Birinci şahıs olarak ('ben', 'projelerim', 'çalışmalarım') konuş.\n"
    "2. Her zaman samimi, teknoloji meraklısı, profesyonel ve yardımsever bir dille cevap ver.\n"
    "3. Cevaplarında uygun yerlerde emojiler kullanarak samimi ve modern bir hava kat.\n"
    "4. Soruları doğrudan ve net bir şekilde yukarıdaki bilgilere dayanarak cevapla. Bilmediğin konularda detaylı bilgi veya iş birlikleri için bana GitHub veya web sitem üzerinden ulaşabileceklerini belirt."
)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def get_api_key():
    """
    Uygulama için geçerli Gemini API anahtarını hiyerarşik olarak arar ve döner.
    Hiyerarşi:
    1. Kod içine statik olarak girilmiş olan API_KEY_IN_CODE (eğer varsayılan değer değilse)
    2. İşletim sistemi çevre değişkeni (GEMINI_API_KEY)
    3. Flask Session (kullanıcının arayüzden girdiği anahtar)
    
    Dönüş:
        str veya None: Bulunan API anahtarı veya None.
    """
    # 1. Kodda tanımlı olanı kontrol et
    if API_KEY_IN_CODE and API_KEY_IN_CODE != "BURAYA APİ KEYİNİ GİR":
        return API_KEY_IN_CODE
    
    # 2. Çevre değişkenini kontrol et
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key
    
    # 3. Session'ı kontrol et
    return session.get("api_key")


# =============================================================================
# FLASK ROUTES (Uygulama Rotaları)
# =============================================================================

@app.route("/", methods=["GET", "POST"])
def chat():
    """
    Ana sohbet sayfası rotası. GET isteklerinde mevcut sohbet arayüzünü ve geçmişi listeler.
    POST isteklerinde kullanıcının yeni mesajını alır, geçmiş konuşma geçmişini Gemini formatına
    dönüştürür ve API üzerinden modelden yanıt alarak ekrana yansıtır.
    """
    api_key = get_api_key()
    
    # Eğer sistemde veya oturumda tanımlı bir API anahtarı yoksa, arayüzde API anahtarı giriş
    # formunu zorunlu kılacak parametreyle (needs_api_key=True) şablonu render et.
    if not api_key:
        return render_template(
            "chat.html", 
            needs_api_key=True, 
            conversation=[]
        )
    
    # Session'da konuşma geçmişi yoksa hoş geldiniz mesajı ile başlat
    if "conversation" not in session:
        session["conversation"] = [
            {"sender": "Alican Kaya", "message": "Sisteme Hoşgeldiniz"}
        ]
        
    conversation = session["conversation"]
    
    # API anahtarının oturumdan (session) gelip gelmediğini kontrol eder.
    # Eğer kullanıcı kendi API anahtarını girdiyse, arayüzde "API Anahtarını Temizle" butonu gösterilir.
    has_session_api_key = bool(
        session.get("api_key") and 
        not (API_KEY_IN_CODE and API_KEY_IN_CODE != "BURAYA APİ KEYİNİ GİR") and 
        not os.environ.get("GEMINI_API_KEY")
    )
    
    # Kullanıcı mesaj gönderdiğinde (POST)
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        if not user_input:
            return redirect(url_for("chat"))
            
        # Sohbeti sonlandırma kelimeleri
        if user_input.lower() in ["exit", "quit"]:
            conversation.append({"sender": "Sistem", "message": "Sohbet sonlandırıldı."})
            session["conversation"] = conversation
            return render_template(
                "chat.html", 
                needs_api_key=False,
                conversation=conversation, 
                has_session_api_key=has_session_api_key
            )
        
        # Kullanıcı mesajını geçmişe ekle
        conversation.append({"sender": "Müşteri", "message": user_input})
        
        # Cookie boyut limitlerini aşmamak için konuşma geçmişini son 20 mesajla sınırlıyoruz.
        # İlk hoş geldiniz mesajı her zaman korunur.
        if len(conversation) > 21:
            conversation = [conversation[0]] + conversation[-20:]
            
        # Flask session geçmişini, google-generativeai API'sinin beklediği formatta
        # (role: user/model, parts: [text]) sözlük listesine dönüştürüyoruz.
        gemini_history = []
        for entry in conversation[:-1]:  # Son eklenen güncel kullanıcı mesajını hariç tutarak öncekileri ekle
            if entry["sender"] == "Müşteri":
                gemini_history.append({"role": "user", "parts": [entry["message"]]})
            elif entry["sender"] == "Alican Kaya" and entry["message"] != "Sisteme Hoşgeldiniz":
                gemini_history.append({"role": "model", "parts": [entry["message"]]})
        
        try:
            # Gemini kütüphanesini API anahtarıyla yapılandırıyoruz
            genai.configure(api_key=api_key)
            
            # API anahtarının izin verdiği ve generateContent fonksiyonunu destekleyen modelleri sorguluyoruz.
            # Bu, kota veya model erişim hatalarını (404/429) en aza indirmek için dinamik bir yapı sunar.
            available_gemini_models = []
            try:
                for m in genai.list_models():
                    if "generateContent" in m.supported_generation_methods and "gemini" in m.name.lower():
                        model_id = m.name.replace("models/", "")
                        available_gemini_models.append(model_id)
            except Exception as list_err:
                print("Modeller listelenemedi:", list_err)
                # Listeleme başarısız olursa en yaygın stabil modelleri varsayılan liste olarak belirle
                available_gemini_models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
            
            # Tercih sırasına göre stabil ve hızlı modelleri listenin en önüne getiriyoruz.
            preferred_models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
            for pref in reversed(preferred_models):
                if pref in available_gemini_models:
                    available_gemini_models.remove(pref)
                    available_gemini_models.insert(0, pref)
            
            response = None
            last_exception = None
            
            # Uygun/çalışan ilk modeli bulana kadar listedeki modelleri sırayla deniyoruz (Model Fallback).
            for model_name in available_gemini_models:
                try:
                    print(f"Model deneniyor: {model_name}")
                    model = genai.GenerativeModel(
                        model_name=model_name,
                        # pyrefly: ignore [bad-argument-type]
                        generation_config=generation_config,
                        system_instruction=corporate_text
                    )
                    # Sohbet geçmişini yükleyerek yeni sohbet oturumunu başlatıyoruz
                    chat_session = model.start_chat(history=gemini_history)
                    # Kullanıcı mesajını gönderip yanıtı alıyoruz
                    response = chat_session.send_message(user_input)
                    print(f"Başarılı! Kullanılan model: {model_name}")
                    break
                except Exception as model_err:
                    print(f"{model_name} modeli hata verdi:", model_err)
                    last_exception = model_err
                    continue
            
            # Eğer hiçbir model çalışmadıysa son oluşan hatayı fırlatıyoruz
            if response is None:
                if last_exception:
                    raise last_exception
                else:
                    raise Exception("Kullanılabilir hiçbir Gemini modeli bulunamadı veya tümü hata verdi.")
            
            # Modelden dönen cevabı konuşma geçmişine ekle
            conversation.append({"sender": "Alican Kaya", "message": response.text})
        except Exception as e:
            # Hata durumunda hata mesajını ekrana yansıtmak üzere sisteme ekle
            conversation.append({"sender": "Sistem", "message": f"Hata oluştu: {str(e)}"})
            
        session["conversation"] = conversation
        
    return render_template(
        "chat.html", 
        needs_api_key=False,
        conversation=conversation, 
        has_session_api_key=has_session_api_key
    )

@app.route("/set_api_key", methods=["POST"])
def set_api_key():
    """
    Kullanıcının HTML arayüzünden girdiği API anahtarını alır ve session'a (oturum verilerine) kaydeder.
    Yeni API anahtarı kaydedildiğinde önceki sohbet geçmişi sıfırlanır.
    """
    api_key = request.form.get("api_key", "").strip()
    if api_key:
        session["api_key"] = api_key
        session.pop("conversation", None)  # Yeni API anahtarıyla sohbeti sıfırla
    return redirect(url_for("chat"))

@app.route("/clear_api_key")
def clear_api_key():
    """
    Oturumda kayıtlı olan API anahtarını ve mevcut sohbet geçmişini temizler.
    Kullanıcıyı ana sayfaya yönlendirir, böylece tekrar API anahtarı istenir.
    """
    session.pop("api_key", None)
    session.pop("conversation", None)
    return redirect(url_for("chat"))

@app.route("/clear_chat")
def clear_chat():
    """
    API anahtarına dokunmadan sadece mevcut sohbet geçmişini temizler ve sohbeti sıfırlar.
    """
    session.pop("conversation", None)
    return redirect(url_for("chat"))

@app.route("/list_models")
def list_models():
    """
    Test amaçlı: API anahtarı ile erişilebilen tüm Gemini modellerini listeleyen yardımcı rota.
    """
    api_key = get_api_key()
    if not api_key:
        return "No API key found."
    try:
        genai.configure(api_key=api_key)
        models = [m.name for m in genai.list_models()]
        print("AVAILABLE MODELS:", models)
        return f"Available models: {models}"
    except Exception as e:
        return f"Error listing models: {str(e)}"

# ---- Uygulamanın Başlatılması ----
if __name__ == "__main__":
    # Flask uygulamasını debug modu açık şekilde lokal sunucuda başlatıyoruz.
    # debug=True modu, kod değişikliklerinde sunucunun otomatik yenilenmesini sağlar.
    app.run(debug=True)
