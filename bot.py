import yfinance as yf
import pandas as pd
import requests
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# خادم وهمي لمنع Render من إغلاق البوت
def run_dummy_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is Running")
    server = HTTPServer(('0.0.0.0', 10000), Handler)
    server.serve_forever()

# تشغيل الخادم في الخلفية
threading.Thread(target=run_dummy_server, daemon=True).start()

# بياناتك
TOKEN = "8705625892:AAFlwIENBqlMvJ2nuRrwJ2GW_u2IFJlTz54"
CHAT_ID = "8159011396"

def send_signal(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    try: requests.get(url)
    except: pass

send_signal("🚀 مبروك يا أحمد! البوت يعمل الآن مجاناً 100% وبدأ مراقبة السوق.")

while True:
    try:
        df = yf.download(tickers="EURUSD=X", period="1d", interval="15m", progress=False)
        if not df.empty:
            df['SMA_Trend'] = df['Close'].rolling(window=200).mean()
            df['SMA_Fast'] = df['Close'].rolling(window=10).mean()
            df['SMA_Slow'] = df['Close'].rolling(window=20).mean()
            last = df.iloc[-1]
            prev = df.iloc[-2]
            if last['Close'] > last['SMA_Trend']:
                if prev['SMA_Fast'] < prev['SMA_Slow'] and last['SMA_Fast'] > last['SMA_Slow']:
                    price = round(float(last['Close']), 5)
                    send_signal(f"✅ إشارة شراء!\n📈 السعر: {price}")
    except: pass
    time.sleep(60)
