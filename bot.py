import yfinance as yf
import pandas as pd
import requests
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# خادم وهمي لإبقاء الخدمة تعمل مجاناً على Render
def run_dummy_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is Active")
    server = HTTPServer(('0.0.0.0', 10000), Handler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# بيانات التليجرام الخاصة بك
TOKEN = "8705625892:AAFlwIENBqlMvJ2nuRrwJ2GW_u2IFJlTz54"
CHAT_ID = "8159011396"

def send_signal(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    try: requests.get(url)
    except: pass

# رسالة اختبار فورية (ستصلك بمجرد الحفظ وتشغيل Render)
send_signal("🚨 اختبار الربط: إذا وصلت هذه الرسالة فالبوت مربوط بجوالك بنجاح وبدأ العمل على فريم 1 دقيقة.")

while True:
    try:
        # تغيير الفريم إلى دقيقة واحدة (1m) وجلب بيانات آخر ساعة
        df = yf.download(tickers="EURUSD=X", period="1h", interval="1m", progress=False)
        
        if not df.empty:
            # إعداد مؤشرات سريعة جداً لفريم الدقيقة
            df['SMA_Trend'] = df['Close'].rolling(window=50).mean() # ترند متوسط
            df['SMA_Fast'] = df['Close'].rolling(window=5).mean()  # سريع جداً
            df['SMA_Slow'] = df['Close'].rolling(window=10).mean() # بطيء نسبياً

            last = df.iloc[-1]
            prev = df.iloc[-2]

            # شرط التقاط الترند الصاعد على فريم 1 دقيقة
            if last['Close'] > last['SMA_Trend']:
                if prev['SMA_Fast'] < prev['SMA_Slow'] and last['SMA_Fast'] > last['SMA_Slow']:
                    price = round(float(last['Close']), 5)
                    send_signal(f"📈 فرصة شراء سريعة (فريم 1د)!\n🌍 الزوج: EUR/USD\n💰 السعر: {price}")

            print(f"🔄 مراقبة فريم الدقيقة.. السعر الحالي: {round(float(last['Close']), 5)}")

    except Exception as e:
        print(f"❌ خطأ: {e}")
    
    time.sleep(30) # فحص كل 30 ثانية لسرعة الاستجابة
