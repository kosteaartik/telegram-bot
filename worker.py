import time
import telebot
import sqlite3
from datetime import datetime

BOT_TOKEN = "8587007298:AAFkoi5ovkasDTHYRLw4oCVTOc0XDssi92w"

bot = telebot.TeleBot(BOT_TOKEN)

def trimite_mesaje_programate():
    while True:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM users")
        users = cursor.fetchall()

        for user in users:
            try:
                bot.send_message(user[0], "🔔 Mesaj automat de test")
            except:
                pass

        conn.close()
        time.sleep(3600) # trimite la 1 oră

if __name__ == "__main__":
    trimite_mesaje_programate()
