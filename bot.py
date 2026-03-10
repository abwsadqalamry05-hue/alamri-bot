import yfinance as yf
import requests
import time
from threading import Thread
from flask import Flask
from datetime import datetime
import os

app = Flask('')

# بيانات التليجرام
TOKEN = "8654440174:AAEt-SWp-O2SmsrYJHvbcAM0pej7Rc9cq6I"
CHAT_ID = "8159011396"

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
    except: pass

@app.route('/')
def home():
    return "✅ الرادار الصاروخي يعمل بنشاط!"

# دالة الصيد الأساسية
def start_hunting():
    print("🚀 انطلق الرادار... جاري فحص الأسعار كل 5 ثوانٍ")
    send_telegram("🚀 *الرادار استيقظ:* جاري صيد الفرص الآن!")
    
    while True:
        try:
            data = yf.download("AUDNZD=X", period="1d", interval="1m", progress=False)
            if not data.empty:
                current_price = data['Close'].iloc[-1]
                # طباعة السعر في اللوجز فوراً
                print(f"🕒 {datetime.now().strftime('%H:%M:%S')} | السعر: {round(current_price, 5)}")
                
                # حساب البولينجر
                ma = data['Close'].rolling(window=20).mean()
                std = data['Close'].rolling(window=20).std()
                lower_band = ma - (std * 2)
                
                last_low = data['Low'].iloc[-1]
                target_lower = lower_band.iloc[-1]
                
                # شرط الصيد (لمس أو اقتراب + شمعة خضراء)
                if last_low <= (target_lower * 1.0002): 
                    if data['Close'].iloc[-1] > data['Open'].iloc[-1]:
                        msg = f"🔔 *إشارة صيد!* 🔔\n💰 السعر: {round(current_price, 5)}\n📈 الاتجاه: صعود"
                        send_telegram(msg)
                        time.sleep(60)
            
            time.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

# تشغيل الصيد في الخلفية أول ما يشتغل السيرفر
Thread(target=start_hunting).start()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
