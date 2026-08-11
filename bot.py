#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
from datetime import datetime
import pytz

BOT_TOKEN = "8674008828:AAHCoFB_bJmEAmwWkt6rl8q5zKkude2RslQ"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

PALESTINE_TZ = pytz.timezone('Asia/Jerusalem')

def get_current_time():
    return datetime.now(PALESTINE_TZ)

def send_message(chat_id, text):
    try:
        requests.post(
            f"{API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            timeout=10
        )
    except:
        pass

def get_gold_price():
    try:
        response = requests.get(
            "https://api.metals.live/v1/spot/gold",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if "price" in data:
                price = float(data["price"])
                if 4000 < price < 5000:
                    return round(price, 2)
    except:
        pass
    return None

def handle_command(chat_id, command):
    current_time = get_current_time()
    time_str = current_time.strftime('%H:%M:%S %d-%m-%Y')
    
    if command == "/start":
        text = "🤖 مرحباً بك!\n\nبوت تحليل الذهب XAUUSD\n\n/help - المساعدة\n/status - الحالة\n/analyze - تحليل الآن"
    
    elif command == "/help":
        text = "الاوامر:\n/start - البدء\n/help - المساعدة\n/status - الحالة\n/analyze - تحليل الذهب"
    
    elif command == "/status":
        text = "البوت يعمل OK\nالرمز: XAUUSD\nالبيانات: حقيقية"
    
    elif command == "/analyze":
        price = get_gold_price()
        
        if price is None:
            text = "عذراً - لم نتمكن من جلب السعر\nحاول مجدداً بعد دقيقة"
        else:
            atr = price * 0.005
            stop_loss = round(price - atr, 2)
            target = round(price + (atr * 2), 2)
            risk = round(price - stop_loss, 2)
            reward = round(target - price, 2)
            ratio = round(reward / risk, 2) if risk > 0 else 0
            
            text = f"تحليل الذهب الآن\n\nالوقت: {time_str}\nالسعر: ${price:,.2f}\n\nالدخول: ${price:,.2f}\nالوقف: ${stop_loss:,.2f}\nالهدف: ${target:,.2f}\n\nRisk: ${risk:.2f}\nReward: ${reward:.2f}\nRatio: 1:{ratio}"
    
    else:
        text = "أمر غير معروف\n/help للمساعدة"
    
    send_message(chat_id, text)

def main():
    offset = 0
    
    while True:
        try:
            response = requests.post(
                f"{API_URL}/getUpdates",
                json={"offset": offset, "timeout": 30},
                timeout=35
            )
            
            data = response.json()
            
            if not data.get("ok"):
                time.sleep(2)
                continue
            
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                
                if "message" not in update:
                    continue
                
                message = update["message"]
                chat_id = message["chat"]["id"]
                text = message.get("text", "").strip()
                
                if text.startswith("/"):
                    handle_command(chat_id, text)
                else:
                    send_message(chat_id, "تم استقبال الرسالة\n/help للاوامر")
        
        except:
            time.sleep(2)

if __name__ == "__main__":
    main()
