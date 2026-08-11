#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
from datetime import datetime
import json

BOT_TOKEN = "8674008828:AAHCoFB_bJmEAmwWkt6rl8q5zKkude2RslQ"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def log_message(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def send_message(chat_id, text):
    try:
        requests.post(
            f"{API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            timeout=10
        )
    except Exception as e:
        log_message(f"ERROR: {e}")

def get_gold_price():
    """Get gold price from reliable source"""
    
    try:
        # Best source: metals.live - very reliable
        log_message("Fetching gold price...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(
            "https://api.metals.live/v1/spot/gold",
            headers=headers,
            timeout=10
        )
        
        log_message(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            log_message(f"Response: {data}")
            
            if isinstance(data, dict) and "price" in data:
                price = float(data["price"])
                log_message(f"SUCCESS: ${price}")
                return round(price, 2)
            elif isinstance(data, dict) and "bid" in data:
                price = float(data["bid"])
                log_message(f"SUCCESS: ${price}")
                return round(price, 2)
        
        log_message("Response format error")
        return None
        
    except Exception as e:
        log_message(f"Exception: {str(e)}")
        return None

def handle_command(chat_id, command):
    if command == "/start":
        text = "Shaditradingxaubot - Gold Trading Bot\n\nCommands:\n/help\n/status\n/analyze"
    
    elif command == "/help":
        text = "Commands:\n/start - Start\n/help - Help\n/status - Bot status\n/analyze - Get live analysis"
    
    elif command == "/status":
        text = "Status: ONLINE\nBot: Working\nData: LIVE"
    
    elif command == "/analyze":
        log_message("========== ANALYZE REQUEST ==========")
        price = get_gold_price()
        log_message(f"Price result: {price}")
        log_message("========== END REQUEST ==========")
        
        if price is None:
            text = "Cannot get price now\nPlease try again in 30 seconds"
        else:
            # Calculate points
            entry = price
            stop = price - (price * 0.005)
            target = price + (price * 0.01)
            risk = price - stop
            reward = target - price
            ratio = reward / risk if risk > 0 else 0
            
            text = (
                f"<b>LIVE GOLD PRICE ANALYSIS</b>\n\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"<b>Price: ${price:.2f}</b>\n\n"
                f"<b>Entry:</b> ${entry:.2f}\n"
                f"<b>Stop Loss:</b> ${stop:.2f}\n"
                f"<b>Take Profit:</b> ${target:.2f}\n\n"
                f"Risk: ${risk:.2f}\n"
                f"Reward: ${reward:.2f}\n"
                f"Risk/Reward: 1:{ratio:.2f}"
            )
    
    else:
        text = "Command not found"
    
    send_message(chat_id, text)

def main():
    log_message("Bot started successfully")
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
                
                log_message(f"Message: {text}")
                
                if text.startswith("/"):
                    handle_command(chat_id, text)
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            log_message(f"Error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
