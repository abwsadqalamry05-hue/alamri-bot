import pandas as pd
import pandas_ta as ta
import requests
import time
import yfinance as yf
from threading import Thread
from flask import Flask

# --- سيرفر وهمي للتشغيل المجاني ---
app = Flask('')
@app.route('/')
def home():
    return "الرادار يعمل بنجاح!"

def run():
    app.run(host='0.0.0.0', port=8080)

# --- بيانات التليجرام الخاصة بك ---
TOKEN = "8654440174:AAEt-SWp-O2SmsrYJHvbcAM0pej7Rc9cq6I"
CHAT_ID = "8159011396"

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error: {e}")

symbol_display = "AUD/NZD OTC"
symbol_data = "AUDNZD=X"

def main_bot():
    print(f"🚀 الرادار يعمل الآن على {symbol_display}...")
    while True:
        try:
            ticker = yf.Ticker(symbol_data)
            df = ticker.history(period="1d", interval="1m")
            if df.empty:
                time.sleep(10)
                continue

            bb = ta.bbands(df['Close'], length=20, std=2)
            lower_band = bb['BBL_20_2.0']
            
            prev_low = df['Low'].iloc[-2]
            prev_lower = lower_band.iloc[-2]
            is_green = df['Close'].iloc[-1] > df['Open'].iloc[-1]
            
            if prev_low <= prev_lower and is_green:
                msg = f"🟢 *إشارة صعود (ارتداد قاع)* \n\n📈 الزوج: {symbol_display} \n💰 السعر: {round(df['Close'].iloc[-1], 5)}"
                send_telegram(msg)
                time.sleep(60) 
                
            time.sleep(10) 
        except Exception as e:
            time.sleep(20)

if __name__ == "__main__":
    # تشغيل السيرفر في خيط منفصل
    t = Thread(target=run)
    t.start()
    # تشغيل البوت الأساسي
    main_bot()
