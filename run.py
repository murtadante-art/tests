#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import webbrowser
import sys
import socket
import threading
import json
from pathlib import Path

HOST       = '0.0.0.0'
START_PORT = 8080
DIRECTORY  = Path(__file__).parent.absolute()

# ============================================================
#  Handler — يخدم الملفات + endpoint خاص لإعطاء IP الزائر
# ============================================================

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def do_GET(self):
        # endpoint خاص: /get-ip → يرجع IP الجهاز الطالب
        if self.path == '/get-ip':
            client_ip = self.client_address[0]
            response  = json.dumps({"ip": client_ip}).encode('utf-8')

            self.send_response(200)
            self.send_header('Content-Type',                'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length',              str(len(response)))
            self.send_header('Cache-Control',               'no-cache')
            self.end_headers()
            self.wfile.write(response)
            return

        # باقي الطلبات → خدمة الملفات العادية
        super().do_GET()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma',        'no-cache')
        self.send_header('Expires',       '0')
        super().end_headers()

    def log_message(self, format, *args):
        if 'favicon' not in str(args):
            super().log_message(format, *args)

# ============================================================
#  المنافذ والشبكة
# ============================================================

def check_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, port))
            return False
        except socket.error:
            return True

def find_available_port(start_port):
    for port in range(start_port, start_port + 20):
        if not check_port_in_use(port):
            return port
    return None

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# ============================================================
#  Banner
# ============================================================

def print_banner(port, local_ip):
    print(f"""
╔══════════════════════════════════════════════════════╗
║              🌐  Andix — Dev Server                  ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  💻  على جهازك فقط:                                  ║
║      http://localhost:{port}/andix.html              ║
║                                                      ║
║  📡  من أي جهاز على نفس الشبكة:                      ║
║      http://{local_ip}:{port}/andix.html             ║
║                                                      ║
║  🔍  endpoint فحص IP:                                ║
║      http://{local_ip}:{port}/get-ip                 ║
║                                                      ║
║  🛑  للإيقاف:  Ctrl + C                              ║
╚══════════════════════════════════════════════════════╝
""")

def open_browser(port):
    url = f"http://localhost:{port}/andix.html"
    webbrowser.open(url)
    print(f"  ✅  تم فتح المتصفح على: {url}\n")

# ============================================================
#  Main
# ============================================================

def main():
    print("\n  🔍  جارٍ البحث عن منفذ متاح...")

    port = find_available_port(START_PORT)
    if port is None:
        print("  ❌  لا يمكن إيجاد منفذ متاح (8080-8099)!")
        sys.exit(1)

    required = ['andix.html', 'styles.css', 'script.js']
    missing  = [f for f in required if not (DIRECTORY / f).exists()]

    if missing:
        print("  ❌  الملفات التالية غير موجودة:")
        for f in missing:
            print(f"       - {f}")
        print(f"\n  📁  المجلد الحالي: {DIRECTORY}")
        sys.exit(1)

    print("  ✅  جميع الملفات موجودة")
    print(f"  📁  مسار المشروع: {DIRECTORY}")

    try:
        socketserver.TCPServer.allow_reuse_address = True
        server   = socketserver.TCPServer((HOST, port), MyHTTPRequestHandler)
        local_ip = get_local_ip()

        print_banner(port, local_ip)
        threading.Timer(1.5, open_browser, args=[port]).start()
        server.serve_forever()

    except KeyboardInterrupt:
        print("\n\n  👋  جارٍ إيقاف السيرفر...")
        server.shutdown()
        server.server_close()
        print("  ✅  تم الإيقاف بنجاح\n")
        sys.exit(0)

    except Exception as e:
        print(f"  ❌  خطأ غير متوقع: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
