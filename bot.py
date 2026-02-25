import yfinance as yf
import pandas as pd
import requests
import time

# بياناتك الصحيحة
TOKEN = "8705625892:AAFlwIENBqlMvJ2nuRrwJ2GW_u2IFJlTz54"
CHAT_ID = "8159011396"

def send_signal(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    try:
        requests.get(url)
    except:
        pass

# هذه الرسالة ستصلك فوراً عند الحفظ للتأكد من نجاح العملية
send_signal("🚀 مبروك يا أحمد! البوت يعمل الآن بنجاح وهو متصل بحسابك.. سأقوم بمراقبة سوق EUR/USD وإرسال التنبيهات فوراً.")

print("🚀 البوت بدأ العمل.. تم إرسال رسالة الترحيب.")

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
                    send_signal(f"✅ إشارة شراء (BUY)!\n📈 السعر: {price}\n🌍 زوج: EUR/USD")
            print(f"📊 نبض البوت: السعر الحالي {round(float(last['Close']), 5)}")
    except Exception as e:
        print(f"🔄 محاولة تحديث: ({e})")
    time.sleep(60)
