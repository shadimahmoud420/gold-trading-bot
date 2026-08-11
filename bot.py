#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
from datetime import datetime

# Configuration
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
        log_message(f"OK Sent to {chat_id}")
    except Exception as e:
        log_message(f"ERROR: {e}")

def get_live_gold_price():
    """Get live gold price"""
    try:
        # Source 1: CoinGecko
        try:
            response = requests.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=gold&vs_currencies=usd",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if "gold" in data and "usd" in data["gold"]:
                    price = float(data["gold"]["usd"])
                    if price > 0:
                        log_message(f"OK Price: ${price}")
                        return round(price, 2)
        except Exception as e:
            log_message(f"Source 1 failed: {e}")
        
        # Source 2: Cryptonator
        try:
            response = requests.get(
                "https://api.cryptonator.com/api/ticker/xau-usd",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    price = float(data["ticker"]["price
