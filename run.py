# run.py
from installer import install_or_update
from discovery import start_discovery_threads
from webapp import app
from utils import get_local_ip
import webbrowser
import threading
from config import HTTP_PORT

def main():
    # تثبيت/تحديث عند التشغيل الأولي
    try:
        deployed = install_or_update()
    except Exception:
        deployed = None

    # تشغيل خيوط الاكتشاف
    stop_event = start_discovery_threads()  # note: we return an event in new discovery implementation
    # افتح المتصفح
    try:
        webbrowser.open(f"http://{get_local_ip()}:{HTTP_PORT}")
    except:
        pass
    # شغّل فلاسكس
    app.run(host="0.0.0.0", port=HTTP_PORT)

if __name__ == "__main__":
    main()
