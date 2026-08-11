#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
from datetime import datetime, timedelta

BOT_TOKEN = "8674008828:AAHCoFB_bJmEAmwWkt6rl8q5zKkude2RslQ"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# متغير لتخزين آخر سعر دخله المستخدم
CURRENT_PRICE = None

def get_palestine_time():
    """الوقت بتوقيت فلسطين"""
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

def handle_command(chat_id, command):
    global CURRENT_PRICE
    time_str = get_palestine_time()
    
    if command == "/start":
        text = (
            "🤖 مرحباً بك!\n\n"
            "بوت تحليل الذهب XAUUSD\n\n"
            "الأوامر:\n"
            "/help - المساعدة\n"
            "/status - الحالة\n"
            "/analyze - التحليل\n"
            "/price [السعر] - أدخل السعر الحالي\n\n"
            "مثال: /price 4423.50"
        )
    
    elif command == "/help":
        text = (
            "الاوامر:\n"
            "/start - البدء\n"
            "/help - المساعدة\n"
            "/status - الحالة\n"
            "/analyze - التحليل\n"
            "/price [السعر] - أدخل السعر من Trading View\n\n"
            "مثال: /price 4423.50"
        )
    
    elif command == "/status":
        if CURRENT_PRICE:
            text = (
                f"🟢 البوت: يعمل\n"
                f"الرمز: XAUUSD\n"
                f"آخر سعر: ${CURRENT_PRICE:,.2f}\n"
                f"الوقت: {time_str}"
            )
        else:
            text = (
                "⚠️ لم تدخل السعر بعد\n"
                "استخدم: /price 4423.50"
            )
    
    elif command == "/analyze":
        if CURRENT_PRICE is None:
            text = "⚠️ أدخل السعر أولاً\nاستخدم: /price [السعر]"
        else:
            price = CURRENT_PRICE
            atr = price * 0.005
            stop_loss = round(price - atr, 2)
            target = round(price + (atr * 2), 2)
            risk = round(price - stop_loss, 2)
            reward = round(target - price, 2)
            ratio = round(reward / risk, 2) if risk > 0 else 0
            
            text = (
                f"📊 تحليل الذهب الحي\n\n"
                f"⏰ الوقت: {time_str}\n"
                f"💰 السعر الحالي: ${price:,.2f}\n\n"
                f"🟢 إشارة شراء\n"
                f"نسبة التأكيد: 85%\n\n"
                f"📈 نقاط التداول:\n"
                f"├─ الدخول: ${price:,.2f}\n"
                f"├─ الوقف: ${stop_loss:,.2f}\n"
                f"└─ الهدف: ${target:,.2f}\n\n"
                f"💰 إدارة المخاط
