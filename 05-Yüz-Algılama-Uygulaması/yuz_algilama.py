import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np


# Arayüz üzerinden dosya seçip yüz algılama işlemini başlatan fonksiyon
def open_file():
    # Kullanıcıdan bir dosya (resim) seçmesini ister
    file_path = filedialog.askopenfilename()
    
    if file_path:
        # cv2.imread Windows'ta Türkçe karakterli yolları okuyamadığı için, dosyayı numpy ile bayt olarak okuyoruz
        img_array = np.fromfile(file_path, np.uint8)
        # Okunan bayt verisini OpenCV'nin kullanabileceği görüntü formatına çeviriyoruz
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        # Haar Cascade yüz algılama modelleri gri tonlamalı görüntülerde çalıştığı için görüntüyü griye çeviriyoruz
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Görüntüdeki ışık ve gölge farklılıklarını dengeleyerek yüzlerin daha net algılanmasını sağlıyoruz
        gray = cv2.equalizeHist(gray)
        
        # Yüz algılama işlemini gerçekleştiriyoruz
        # scaleFactor: Görüntü küçültme oranı (hassasiyet)
        # minNeighbors: Onay için gereken komşu tespit sayısı
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.30, minNeighbors=5, minSize=(30, 30))

        # Algılanan her bir yüz için x,y (başlangıç koordinatları) ve w,h (genişlik, yükseklik) değerlerini döngüye sokuyoruz
        for (x, y, w, h) in faces:
            # Yüzün etrafına mavi renkli (255, 0, 0) ve 2 piksel kalınlığında bir dikdörtgen çiziyoruz
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # Çizilen dikdörtgenin altına 'insan' metnini ekliyoruz
            cv2.putText(img, "insan", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # OpenCV BGR renk formatını kullanırken, Tkinter (Pillow) RGB kullanır. Bu yüzden renkleri düzeltiyoruz.
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Görüntüyü Pillow Image nesnesine dönüştürüyoruz
        img = Image.fromarray(img)
        # Görüntüyü arayüze sığması için 600x400 boyutlarına yeniden boyutlandırıyoruz (LANCZOS kaliteli küçültme sağlar)
        img = img.resize((600, 400), Image.LANCZOS)
        # Pillow görüntüsünü Tkinter'da gösterilebilecek formata çeviriyoruz
        img = ImageTk.PhotoImage(img)
        
        # Çöp toplayıcının (garbage collector) resmi hafızadan silmesini engellemek için referansını saklıyoruz
        canvas.img = img
        # Görüntüyü canvas (tuval) üzerine yerleştiriyoruz (NW: Kuzeybatı, yani sol üst köşe)
        canvas.create_image(0, 0, anchor=tk.NW, image=img)


# Önceden eğitilmiş Haar Cascade yüz algılama modelini (XML dosyası) yüklüyoruz
face_cascade = cv2.CascadeClassifier('face_detector.xml')


# --- Arayüz (GUI) Kurulumu ---

# Ana pencereyi oluşturuyoruz
root = tk.Tk()
root.title("Yüz Tanıma Uygulaması")

# Görüntünün gösterileceği 600x400 piksel boyutunda bir tuval (canvas) oluşturuyoruz
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()

# Dosya seçme işlemini (open_file fonksiyonunu) tetikleyecek butonu oluşturup pencereye ekliyoruz
open_button = tk.Button(root, text="Dosya Seç", command=open_file)
open_button.pack()

# Arayüzün sürekli açık kalmasını ve kullanıcı etkileşimlerini dinlemesini sağlayan sonsuz döngüyü başlatıyoruz
root.mainloop()