import yfinance as yf
import requests
import time
from threading import Thread
from flask import Flask

# سيرفر وهمي للتشغيل المجاني
app = Flask('')
@app.route('/')
def home(): return "الرادار يعمل!"

def run(): app.run(host='0.0.0.0', port=8080)

# بياناتك الصحيحة من الصور
TOKEN = "8654440174:AAEt-SWp-O2SmsrYJHvbcAM0pej7Rc9cq6I"
CHAT_ID = "8159011396"

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
    except: pass

def main_bot():
    # رسالة ترحيبية فور التشغيل
    print("🚀 الرادار انطلق...")
    send_telegram("✅ *تم تشغيل الرادار بنجاح!* \nأنا الآن أراقب سوق AUD/NZD OTC وسأرسل لك أي إشارة فور حدوثها.")
    
    while True:
        try:
            data = yf.download("AUDNZD=X", period="1d", interval="1m", progress=False)
            if not data.empty:
                close = data['Close']
                # حساب البولينجر يدويًا لتجنب أخطاء المكتبات الخارجية
                ma = close.rolling(window=20).mean()
                std = close.rolling(window=20).std()
                lower_band = ma - (std * 2)
                
                last_low = data['Low'].iloc[-2]
                last_lower = lower_band.iloc[-2]
                is_green = data['Close'].iloc[-1] > data['Open'].iloc[-1]

                if last_low <= last_lower and is_green:
                    send_telegram(f"🟢 *إشارة صعود AUD/NZD OTC* \nالسعر الحالي: {round(data['Close'].iloc[-1], 5)}")
                    time.sleep(60)
            time.sleep(15)
        except: time.sleep(20)

if __name__ == "__main__":
    Thread(target=run).start()
    main_bot()
