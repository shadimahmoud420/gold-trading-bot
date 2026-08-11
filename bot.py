#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
from datetime import datetime

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

def get_real_gold_price():
    """Get REAL gold price - no cache, no templates"""
    
    prices = []
    
    # Source 1: Direct metals API
    try:
        log_message("Fetching from metals.live...")
        response = requests.get(
            "https://api.metals.live/v1/spot/gold",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            price = float(data.get("price", 0))
            if price > 0:
                log_message(f"metals.live: ${price}")
                prices.append(price)
    except Exception as e:
        log_message(f"metals.live ERROR: {e}")
    
    # Source 2: Forex API
    try:
        log_message("Fetching from forexapi...")
        response = requests.get(
            "https://api.exchangerate-api.com/v4/latest/XAU",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if "rates" in data and "USD" in data["rates"]:
                rate = float(data["rates"]["USD"])
                price = 1 / rate if rate > 0 else 0
                if price > 1000:
                    log_message(f"forexapi: ${price}")
                    prices.append(price)
    except Exception as e:
        log_message(f"forexapi ERROR: {e}")
    
    # Source 3: Twelve Data
    try:
        log_message("Fetching from twelvedata...")
        response = requests.get(
            "https://api.twelvedata.com/quote?symbol=XAU/USD&apikey=demo",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if "price" in data:
                price = float(data["price"])
                if price > 1000:
                    log_message(f"twelvedata: ${price}")
                    prices.append(price)
    except Exception as e:
        log_message(f"twelvedata ERROR: {e}")
    
    # Source 4: Finnhub
    try:
        log_message("Fetching from finnhub...")
        response = requests.get(
            "https://finnhub.io/api/v1/quote?symbol=XAUUSD&token=cljf96qr01qh3oj01d7g",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if "c" in data:
                price = float(data["c"])
                if price > 1000:
                    log_message(f"finnhub: ${price}")
                    prices.append(price)
    except Exception as e:
        log_message(f"finnhub ERROR: {e}")
    
    # Return average if got multiple sources
    if prices:
        avg_price = sum(prices) / len(prices)
        log_message(f"FINAL PRICE: ${avg_price:.2f}")
        return round(avg_price, 2)
    
    log_message("ERROR: No sources available")
    return None

def handle_command(chat_id, command):
    if command == "/start":
        text = "Gold Trading Bot\n\n/help - Help\n/status - Status\n/analyze - Analyze"
    
    elif command == "/help":
        text = "Commands:\n/start\n/help\n/status\n/analyze\n\nEducational only"
    
    elif command == "/status":
        text = "Status: ONLINE\nSymbol: XAUUSD\nData: LIVE"
    
    elif command == "/analyze":
        log_message("===== GETTING LIVE PRICE =====")
        real_price = get_real_gold_price()
        log_message("===== PRICE RECEIVED =====")
        
        if real_price is None:
            text = "ERROR getting price\nTry again"
        else:
            stop_loss = real_price - (real_price * 0.005)
            target = real_price + (real_price * 0.01)
            
            text = (
                f"LIVE ANALYSIS\n\n"
                f"Time: {datetime.now().strftime('%H:%M:%S')}\n"
                f"PRICE: ${real_price}\n\n"
                f"Entry: ${real_price}\n"
                f"Stop: ${stop_loss:.2f}\n"
                f"Target: ${target:.2f}\n\n"
                f"Live data - no cache"
            )
    
    else:
        text = "Unknown command"
    
    send_message(chat_id, text)

def main():
    log_message("Bot started")
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
                    send_message(chat_id, "OK")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            time.sleep(2)

if __name__ == "__main__":
    main()
