#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
from datetime import datetime
import pytz

BOT_TOKEN = "8674008828:AAHCoFB_bJmEAmwWkt6rl8q5zKkude2RslQ"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# توقيت فلسطين
PALESTINE_TZ = pytz.timezone('Asia/Jerusalem')

def get_current_time():
    """الحصول على الوقت الحالي بتوقيت فلسطين"""
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

def get_live_gold_price():
    """محاولة جلب السعر الحقيقي من API موثوقة"""
    
    try:
        # المحاولة الأولى: metals.live
        response = requests.get(
            "https://api.metals.live/v1/spot/gold",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if "price" in data:
                price = float(data["price"])
                if 4000 < price < 5000:  # تحقق من أن السعر معقول
                    return round(price, 2)
    except:
        pass
    
    try:
        # المحاولة الثانية: exchangerate-api
        response = requests.get(
            "https://api.exchangerate-api.com/v4/latest/XAU",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if "rates" in data and "USD" in data["rates"]:
                rate = float(data["rates"]["USD"])
                if rate > 0:
                    price = 1 / rate
                    if 4000 < price < 5000:
                        return round(price, 2)
    except:
        pass
    
    try:
        # المحاولة الثالثة: apilayer
        response = requests.get(
            "https://api.apilayer.com/exchangerates_data/latest?base=XAU&symbols=USD",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "rates" in data:
                rate = float(data["rates"]["USD"])
                if rate > 0:
                    price = 1 / rate
                    if 4000 < price < 5000:
                        return round(price, 2)
    except:
        pass
    
    return None

def handle_command(chat_id, command):
    current_time = get_current_time()
    
    if command == "/start":
        text = (
            "🤖 <b>مرحباً بك!
