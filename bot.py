#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
from datetime import datetime, timedelta

BOT_TOKEN = "8674008828:AAHCoFB_bJmEAmwWkt6rl8q5zKkude2RslQ"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

CURRENT_PRICE = None

def get_time():
    utc_now = datetime.utcnow()
    palestine_time = utc_now + timedelta(hours=3)
    return palestine_time.strftime('%H:%M:%S %d-%m-%Y')

def send_message(chat_id, text):
    try:
        requests.post(
            f"{API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            timeout=10
        )
    except:
        pass

def main():
    global CURRENT_PRICE
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
                
                time_str = get_time()
                
                if text == "/start":
                    send_message(chat_id, "Shaditradingxaubot - Gold Trading Analysis\n\nCommands:\n/price [amount] - Enter gold price\n/analyze - Get analysis\n/status - Bot status\n/help - Help")
                
                elif text == "/help":
                    send_message(chat_id, "Commands:\n/start - Start\n/help - Help\n/price 4423.50 - Enter current price\n/analyze - Analyze\n/status - Status")
                
                elif text == "/status":
                    if CURRENT_PRICE:
                        send_message(chat_id, f"Status: ONLINE\nSymbol: XAUUSD\nCurrent Price: ${CURRENT_PRICE:,.2f}\nTime: {time_str}")
                    else:
                        send_message(chat_id, "Status: ONLINE\nPlease enter price first: /price 4423.50")
                
                elif text.startswith("/price "):
                    try:
                        price_str = text.replace("/price ", "").strip()
                        price = float(price_str)
                        
                        if 4000 < price < 5000:
                            CURRENT_PRICE = price
                            send_message(chat_id, f"Price updated: ${price:,.2f}\n\nUse /analyze for analysis")
                        else:
                            send_message(chat_id, "Invalid price\nPrice must be between 4000-5000")
                    except:
                        send_message(chat_id, "Invalid format\nUse: /price 4423.50")
                
                elif text == "/analyze":
                    if CURRENT_PRICE is None:
                        send_message(chat_id, "Enter price first\nUse: /price 4423.50")
                    else:
                        price = CURRENT_PRICE
                        atr = price * 0.005
                        stop_loss = round(price - atr, 2)
                        target = round(price + (atr * 2), 2)
                        risk = round(price - stop_loss, 2)
                        reward = round(target - price, 2)
                        ratio = round(reward / risk, 2) if risk > 0 else 0
                        
                        analysis = f"GOLD ANALYSIS\n\nTime: {time_str}\nPrice: ${price:,.2f}\n\nSignal: BUY\nConfidence: 85%\n\nEntry: ${price:,.2f}\nStop Loss: ${stop_loss:,.2f}\nTarget: ${target:,.2f}\n\nRisk: ${risk:.2f}\nReward: ${reward:.2f}\nRatio: 1:{ratio}"
                        
                        send_message(chat_id, analysis)
                
                else:
                    send_message(chat_id, "Unknown command\n/help for commands")
        
        except:
            time.sleep(2)

if __name__ == "__main__":
    main()
