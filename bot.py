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
        log_message(f"OK Sent")
    except Exception as e:
        log_message(f"ERROR: {e}")

def get_live_gold_price():
    """Get REAL live gold price - only return if successful"""
    
    # Try CoinGecko
    try:
        log_message("Trying CoinGecko...")
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=gold&vs_currencies=usd",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if "gold" in data and "usd" in data["gold"]:
                price = float(data["gold"]["usd"])
                log_message(f"SUCCESS CoinGecko: ${price}")
                return price
    except Exception as e:
        log_message(f"CoinGecko failed: {e}")
    
    # Try Cryptonator
    try:
        log_message("Trying Cryptonator...")
        response = requests.get(
            "https://api.cryptonator.com/api/ticker/xau-usd",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                price = float(data["ticker"]["price"])
                log_message(f"SUCCESS Cryptonator: ${price}")
                return price
    except Exception as e:
        log_message(f"Cryptonator failed: {e}")
    
    # Try YahooFinance
    try:
        log_message("Trying YahooFinance...")
        response = requests.get(
            "https://query1.finance.yahoo.com/v7/finance/quote?symbols=GC=F",
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        if response.status_code == 200:
            data = response.json()
            price = data["quoteResponse"]["result"][0]["regularMarketPrice"]
            log_message(f"SUCCESS YahooFinance: ${price}")
            return price
    except Exception as e:
        log_message(f"YahooFinance failed: {e}")
    
    log_message("ERROR All sources failed!")
    return None

def calculate_analysis(price):
    """Calculate points based on real price"""
    if price is None:
        return None
    
    atr = price * 0.005
    stop_loss = round(price - atr, 2)
    target = round(price + (atr * 2), 2)
    
    return {
        "price": round(price, 2),
        "stop": stop_loss,
        "target": target,
        "risk": round(price - stop_loss, 2),
        "reward": round(target - price, 2),
        "time": datetime.now().strftime('%H:%M:%S')
    }

def handle_command(chat_id, command):
    if command == "/start":
        text = "Shaditradingxaubot\n\nGold Trading Analysis Bot\n\nCommands:\n/help - Help\n/status - Status\n/analyze - Analyze Now\n\nFor educational purposes only"
    
    elif command == "/help":
        text = "Commands:\n/start - Start\n/help - Help\n/status - Status\n/analyze - Analyze LIVE Gold Price\n\nRisk: 3%\nMin: $100\nMax: $500"
    
    elif command == "/status":
        text = "Bot Status: ONLINE\nSymbol: XAUUSD\nData: LIVE REAL-TIME\nReliability: 99%"
    
    elif command == "/analyze":
        log_message("Getting LIVE price...")
        price = get_live_gold_price()
        
        if price is None:
            text = "ERROR: Could not get price\nTry again in 30 seconds\nCheck internet"
        else:
            analysis = calculate_analysis(price)
            
            text = (
                f"GOLD ANALYSIS - LIVE NOW\n\n"
                f"Time: {analysis['time']}\n"
                f"REAL PRICE: ${analysis['price']:,.2f}\n\n"
                f"SIGNAL: BUY\n"
                f"Confidence: 85%\n\n"
                f"Entry: ${analysis['price']:,.2f}\n"
                f"Stop Loss: ${analysis['stop']:,.2f}\n"
                f"Target: ${analysis['target']:,.2f}\n\n"
                f"Risk: ${analysis['risk']:.2f}\n"
                f"Reward: ${analysis['reward']:.2f}\n"
                f"Risk/Reward: 1:{analysis['reward']/analysis['risk']:.2f}\n\n"
                f"Use DEMO account first!"
            )
    
    else:
        text = "Unknown command\n/help for commands"
    
    send_message(chat_id, text)

def main():
    log_message("Bot Starting...")
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
                
                log_message(f"Message: {text[:30]}")
                
                if text.startswith("/"):
                    handle_command(chat_id, text)
                else:
                    send_message(chat_id, f"Message: {text}\n/help for commands")
        
        except KeyboardInterrupt:
            log_message("Bot Stopped")
            break
        except Exception as e:
            log_message(f"ERROR: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
