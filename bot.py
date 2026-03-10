import yfinance as yf
import requests
import time
from threading import Thread
from flask import Flask
from datetime import datetime

# سيرفر وهمي لتجاوز قيود Render المجانية
app = Flask('')
@app.route('/')
def home(): return "الرادار الصاروخي يعمل!"

def run(): app.run(host='0.0.0.0', port=8080)

# بيانات التليجرام الخاصة بك
TOKEN = "8654440174:AAEt-SWp-O2SmsrYJHvbcAM0pej7Rc9cq6I"
CHAT_ID = "8159011396"

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
    except: pass

def main_bot():
    print("🚀 تم تفعيل الرادار السريع... الصيد بدأ!")
    send_telegram("🚀 *تم تحديث البوت:* الرادار الآن أسرع ويراقب السعر كل 5 ثوانٍ!")
    
    while True:
        try:
            # جلب البيانات لزوج AUD/NZD (البيانات العالمية الأقرب للـ OTC)
            data = yf.download("AUDNZD=X", period="1d", interval="1m", progress=False)
            
            if not data.empty:
                current_price = data['Close'].iloc[-1]
                # طباعة السعر في الـ Logs عشان تتأكد إنه شغال
                print(f"🕒 {datetime.now().strftime('%H:%M:%S')} | السعر الحالي: {round(current_price, 5)}")
                
                # حساب البولينجر باند (فترة 20)
                ma = data['Close'].rolling(window=20).mean()
                std = data['Close'].rolling(window=20).std()
                lower_band = ma - (std * 2)
                
                # إعدادات الاستراتيجية المعدلة (أسرع وأذكى)
                last_low = data['Low'].iloc[-1]
                target_lower = lower_band.iloc[-1]
                
                # شرط الدخول: إذا السعر لمس أو اقترب جداً (بفارق بسيط) من الخط السفلي
                if last_low <= (target_lower * 1.0001): # هامش بسيط لعدم ضياع الفرص
                    # إذا كانت الشمعة الحالية خضراء (سعر الإغلاق أكبر من الافتتاح)
                    if data['Close'].iloc[-1] > data['Open'].iloc[-1]:
                        msg = f"🔔 *إشارة صيد مؤكدة!* 🔔\n\n📈 الزوج: AUD/NZD\n💰 السعر الحالي: {round(current_price, 5)}\n🚀 الهدف: صعود (ارتداد من القاع)"
                        send_telegram(msg)
                        print("✅ تم إرسال تنبيه للتليجرام!")
                        time.sleep(60) # توقف دقيقة بعد الإشارة عشان ما يزعجك برسائل مكررة
            
            time.sleep(5) # فحص كل 5 ثوانٍ (سرعة خرافية)
            
        except Exception as e:
            print(f"⚠️ تنبيه بسيط: {e}")
            time.sleep(10)

if __name__ == "__main__":
    Thread(target=run).start()
    main_bot()
