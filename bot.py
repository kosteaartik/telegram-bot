import telebot
import os
import time
import schedule
from database import init_db, add_user, get_users

TOKEN = os.getenv("8587007298:AAFkoi5ovkasDTHYRLw4oCVTOc0XDssi92w")
bot = telebot.TeleBot(TOKEN)

init_db()

@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.chat.id)
    bot.send_message(message.chat.id, "✅ Te-ai abonat la notificări!\nVei primi informații automat.")

def send_daily_message():
    users = get_users()
    for user in users:
        try:
            bot.send_message(user, "📢 Salut! Mesaj automat zilnic.\nSecuritate & Protecție ✅")
        except:
            pass

schedule.every().day.at("09:00").do(send_daily_message)  # zilnic la 09:00
schedule.every().monday.at("09:00").do(send_daily_message) # săptămânal luni

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

import threading
t = threading.Thread(target=run_schedule)
t.start()

bot.polling(non_stop=True)
