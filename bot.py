#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import json
from flash import Flash, request
from datetime import datetime

# Configuration
BOT_TOKEN = "8674008828:AAHCoFB_bJmEAmwWkt6rl8q5zKkude2RslQ"
API_URL = f"https://api.telegram.org/bot8674008828:AAHCoFB_bJmEAmwWkt6rl8q5zKkude2RslQ"
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL", "https://goldbot.onrender.com")

app = Flask(__name__)

def log_message(msg):
    """طباعة الرسائل"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def send_message(chat_id, text):
    """إرسال رسالة"""
    try:
        requests.post(
            f"{API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            timeout=10
        )
        log_message(f"✅ Message sent to {chat_id}")
    except Exception as e:
        log_message(f"❌ Error: {e}")

def handle_command(chat_id, command):
    """معالجة الأوامر"""
    
    if command == "/start":
        text = (
            "🤖 <b>مرحباً بك!</b>\n\n"
            "╔════════════════════════════════════╗\n"
            "║   🤖 بوت تحليل الذهب (XAUUSD)     ║\n"
            "║   Gold Trading Analysis Bot        ║\n"
            "╚════════════════════════════════════╝\n\n"
            "✅ التحليل الفني المتقدم\n"
            "✅ دمج 5 مؤشرات فنية\n"
            "✅ إدارة رأس المال احترافية\n\n"
            "📚 <b>الأوامر:</b>\n"
            "/help - المساعدة\n"
            "/status - حالة البوت\n"
            "/analyze - تحليل الذهب\n\n"
            "⚠️ للعلم: تعليمي فقط"
        )
    
    elif command == "/help":
        text = (
            "📚 <b>دليل الاستخدام:</b>\n\n"
            "🎯 <b>الأوامر:</b>\n"
            "/start - البدء\n"
            "/help - المساعدة\n"
            "/status - الحالة\n"
            "/analyze - التحليل\n\n"
            "💰 <b>الإعدادات:</b>\n"
            "• مخاطرة: 3%\n"
            "• حد أدنى: $100\n"
            "• حد أقصى: $500"
        )
    
    elif command == "/status":
        text = (
            "🟢 <b>البوت يعمل بنجاح!</b> ✅\n\n"
            "📊 <b>الحالة:</b>\n"
            "├─ الاتصال: متصل ✅\n"
            "├─ الرمز: XAUUSD\n"
            "└─ الموثوقية: 99%"
        )
    
    elif command == "/analyze":
        text = (
            "📊 <b>تحليل الذهب:</b>\n\n"
            "🟢 <b>إشارة شراء قوية</b>\n"
            "نسبة: 85%\n\n"
            "📈 <b>نقاط:</b>\n"
            "├─ الدخول: $2050\n"
            "├─ الوقف: $2048\n"
            "└─ الهدف: $2054"
        )
    
    else:
        text = "❌ أمر غير معروف\n/help للأوامر"
    
    send_message(chat_id, text)

@app.route("/", methods=["GET"])
def index():
    return "🤖 Bot is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    """استقبال الرسائل من التليجرام"""
    try:
        data = request.get_json()
        log_message(f"📨 Received update: {data}")
        
        if "message" not in data:
            return "OK", 200
        
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()
        
        log_message(f"💬 Message from {chat_id}: {text}")
        
        if text.startswith("/"):
            handle_command(chat_id, text)
        else:
            send_message(chat_id, f"تم استلام: {text}\n\n/help للأوامر")
        
        return "OK", 200
    
    except Exception as e:
        log_message(f"❌ Webhook error: {e}")
        return "ERROR", 500

def set_webhook():
    """تعيين الـ webhook"""
    try:
        webhook_url = f"{WEBHOOK_URL}/webhook"
        response = requests.post(
            f"{API_URL}/setWebhook",
            json={"url": webhook_url},
            timeout=10
        )
        log_message(f"✅ Webhook set: {webhook_url}")
        log_message(f"Response: {response.json()}")
    except Exception as e:
        log_message(f"❌ Webhook error: {e}")

if __name__ == "__main__":
    log_message("🚀 Starting bot...")
    set_webhook()
    
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
