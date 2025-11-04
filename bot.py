import telebot

BOT_TOKEN = "8587007298:AAFkoi5ovkasDTHYRLw4oCVTOc0XDssi92w"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salut! ✅ Botul funcționează!")

bot.polling()

