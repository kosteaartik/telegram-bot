# bot.py
import os
import telebot
from telebot import types
from db import SessionLocal, init_db
from models import User, Lead
from sqlalchemy.orm import Session

TOKEN = os.environ.get("8587007298:AAFkoi5ovkasDTHYRLw4oCVTOc0XDssi92w")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))

bot = telebot.TeleBot(TOKEN)
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def user_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row("🛡 О компании", "📦 Услуги")
    menu.row("📞 Контакты", "📟 Вызов экспертизы")
    return menu

@bot.message_handler(commands=['start'])
def start(message):
    db = SessionLocal()
    try:
        existing = db.query(User).filter_by(tg_id=message.chat.id).first()
        if not existing:
            u = User(tg_id=message.chat.id, name=message.from_user.first_name,
                     username=message.from_user.username)
            db.add(u); db.commit()
        bot.send_message(message.chat.id,
                         "👋 Добро пожаловать! Вы подписаны на оповещения.",
                         reply_markup=user_menu())
    finally:
        db.close()

@bot.message_handler(func=lambda m: m.text == "📟 Вызов экспертизы")
def request_expert(message):
    bot.send_message(message.chat.id,
        "🧾 Опишите запрос: кратко укажите что нужно, адрес или местоположение.\n\n"
        "Например:\n— Обследование объекта, улица Ленина 10\n— Установка видеонаблюдения")
    bot.register_next_step_handler(message, forward_expert_to_admin)

def forward_expert_to_admin(message):
    db = SessionLocal()
    try:
        # optional: save as lead
        lead = Lead(tg_id=message.chat.id, name=message.from_user.first_name,
                    message=message.text)
        db.add(lead); db.commit()
    finally:
        db.close()

    admin_text = (
        f"📟 Запрос на экспертизу\n"
        f"👤 {message.from_user.first_name} @{message.from_user.username}\n"
        f"ID: {message.chat.id}\n"
        f"💬 {message.text}"
    )
    bot.send_message(ADMIN_ID, admin_text)
    bot.send_message(message.chat.id, "✅ Ваш запрос отправлен. Мы свяжемся с вами в ближайшее время.")

# Unsubscribe via text STOP / СТОП
@bot.message_handler(func=lambda m: m.text and m.text.strip().upper() in ("СТОП","STOP"))
def handle_stop(message):
    db = SessionLocal()
    try:
        u = db.query(User).filter_by(tg_id=message.chat.id).first()
        if u:
            u.subscribed = False
            db.commit()
        bot.send_message(message.chat.id, "Вы отписаны. Спасибо.")
    finally:
        db.close()

# Admin commands via private chat
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if str(message.chat.id) != str(ADMIN_ID):
        bot.send_message(message.chat.id, "⛔ Доступ запрещён")
        return
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📢 Сделать рассылку", "📊 Подписчики")
    kb.row("⬅️ В меню")
    bot.send_message(message.chat.id, "Панель администратора", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "📊 Подписчики")
def count_subs(message):
    if str(message.chat.id) != str(ADMIN_ID): return
    db = SessionLocal()
    try:
        cnt = db.query(User).filter_by(subscribed=True).count()
        bot.send_message(message.chat.id, f"📊 Подписчиков: {cnt}")
    finally:
        db.close()

@bot.message_handler(func=lambda m: m.text == "📢 Сделать рассылку")
def ask_broadcast(message):
    if str(message.chat.id) != str(ADMIN_ID): return
    bot.send_message(message.chat.id, "Введите текст рассылки:")
    bot.register_next_step_handler(message, do_broadcast)

def do_broadcast(message):
    if str(message.chat.id) != str(ADMIN_ID): return
    text = message.text
    db = SessionLocal()
    try:
        users = db.query(User).filter_by(subscribed=True).all()
        sent = 0
        for u in users:
            try:
                bot.send_message(u.tg_id, text)
                sent += 1
            except Exception:
                pass
        bot.send_message(message.chat.id, f"✅ Разослано: {sent}")
    finally:
        db.close()

if __name__ == "__main__":
    bot.infinity_polling()
