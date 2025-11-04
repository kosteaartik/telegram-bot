# worker.py
import os
import time
import telebot
import schedule
from db import SessionLocal, init_db
from models import User
from sqlalchemy.orm import Session

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

init_db()

def send_daily():
    db = SessionLocal()
    try:
        users = db.query(User).filter_by(subscribed=True).all()
        for u in users:
            try:
                bot.send_message(u.tg_id, "📢 Ежедневная рассылка: советы по безопасности.")
            except Exception:
                pass
    finally:
        db.close()

# schedule: daily at env DAILY_HOUR (format "09:00")
DAILY_HOUR = os.environ.get("DAILY_HOUR", "09:00")
schedule.every().day.at(DAILY_HOUR).do(send_daily)
schedule.every().monday.at(DAILY_HOUR).do(send_daily)  # example

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
