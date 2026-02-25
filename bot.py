import yfinance as yf
import pandas_ta as ta
import requests
import time

# بياناتك الصحيحة التي تعمل بنجاح
TOKEN = "8705625892:AAFlwIENBqlMvJ2nuRrwJ2GW_u2IFJhZxWA"
CHAT_ID = "8159011396"

def send_signal(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    try:
        requests.get(url)
    except:
        pass

print("🚀 البوت بدأ العمل على الخادم.. المراقبة مستمرة 24/7")

while True:
    try:
        # جلب البيانات لزوج اليورو دولار العالمي
        df = yf.download(tickers="EURUSD=X", period="1d", interval="1m", progress=False)
        
        # إضافة مؤشرات الترند والتقاطع
        df['SMA_Trend'] = ta.sma(df['Close'], length=200)
        df['SMA_Fast'] = ta.sma(df['Close'], length=10)
        df['SMA_Slow'] = ta.sma(df['Close'], length=30)
        
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        # شرط الشراء فقط مع الاتجاه الصاعد
        if last['Close'] > last['SMA_Trend']:
            if prev['SMA_Fast'] < prev['SMA_Slow'] and last['SMA_Fast'] > last['SMA_Slow']:
                send_signal(f"✅ إشارة شراء (BUY)!\n💰 السعر: {last['Close']:.5f}\n📈 الترند صاعد")
        
        print(f"📊 نبض البوت: السعر الحالي {last['Close']:.5f}")
    except Exception as e:
        print(f"🔄 محاولة تحديث: {e}")
        
    time.sleep(60)
