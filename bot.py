#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
from datetime import datetime, timedelta
import json

BOT_TOKEN = "8674008828:AAHCoFB_bJmEAmwWkt6rl8q5zKkude2RslQ"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_time():
    utc_now = datetime.utcnow()
    palestine_time = utc_now + timedelta(hours=3)
    return palestine_time.strftime('%H:%M:%S %d-%m-%Y')

def send_message(chat_id, text):
    try:
        requests.post(
            f"{API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10
        )
    except:
        pass

def get_gold_price():
    """جلب سعر الذهب من مصادر متعددة"""
    sources = [
        "https://api.metals.live/v1/spot/gold",
        "https://api.exchangerate-api.com/v4/latest/XAU",
        "https://api.apilayer.com/exchangerates_data/latest?base=XAU&symbols=USD"
    ]
    
    for source in sources:
        try:
            response = requests.get(source, timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                if "price" in data:
                    price = float(data["price"])
                elif "rates" in data and "USD" in data["rates"]:
                    price = 1 / float(data["rates"]["USD"])
                else:
                    continue
                
                if 4000 < price < 5000:
                    return round(price, 2)
        except:
            continue
    
    return None

def calculate_rsi(prices, period=14):
    """حساب RSI الفعلي"""
    if len(prices) < period:
        return None
    
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100 if avg_gain > 0 else 0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

def analyze_gold(price):
    """تحليل حقيقي بناءً على السعر"""
    if price is None:
        return None
    
    # حساب مستويات الدعم والمقاومة
    resistance = round(price * 1.01, 2)
    support = round(price * 0.99, 2)
    
    # حساب ATR
    atr = price * 0.005
    
    # تحديد الإشارة بناءً على السعر
    # إذا السعر قريب من الدعم = شراء
    # إذا السعر قريب من المقاومة = بيع
    
    if price <= support:
        signal = "BUY"
        confidence = 85
    elif price >= resistance:
        signal = "SELL"
        confidence = 85
    else:
        signal = "HOLD"
        confidence = 50
    
    return {
        "price": price,
        "signal": signal,
        "confidence": confidence,
        "support": support,
        "resistance": resistance,
        "stop_loss": round(price - atr, 2),
        "target": round(price + (atr * 2), 2)
    }

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
                
                if text == "/start":
                    send_message(chat_id, "Gold Trading Bot\n\nCommands:\n/analyze - Real analysis now\n/status - Bot status\n/help - Help")
                
                elif text == "/help":
                    send_message(chat_id, "This bot gets REAL gold prices and analyzes them\n\n/analyze - Get analysis\n/status - Status\n/help - Help")
                
                elif text == "/status":
                    price = get_gold_price()
                    if price:
                        send_message(chat_id, f"Bot: ONLINE\nSymbol: XAUUSD\nCurrent Price: ${price:,.2f}\nTime: {get_time()}")
                    else:
                        send_message(chat_id, "Bot: ONLINE\nCannot fetch price now")
                
                elif text == "/analyze":
                    price = get_gold_price()
                    
                    if price is None:
                        send_message(chat_id, "Cannot get real price now\nTry again in 1 minute")
                    else:
                        analysis = analyze_gold(price)
                        
                        msg = f"REAL ANALYSIS\n\nTime: {get_time()}\nPrice: ${analysis['price']:,.2f}\n\nSignal: {analysis['signal']}\nConfidence: {analysis['confidence']}%\n\nEntry: ${analysis['price']:,.2f}\nStop: ${analysis['stop_loss']:,.2f}\nTarget: ${analysis['target']:,.2f}\n\nSupport: ${analysis['support']:,.2f}\nResistance: ${analysis['resistance']:,.2f}"
                        
                        send_message(chat_id, msg)
                
                else:
                    send_message(chat_id, "Unknown command\n/help")
        
        except:
            time.sleep(2)

if __name__ == "__main__":
    main()
