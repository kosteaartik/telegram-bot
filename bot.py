import telebot

BOT_TOKEN = "8587007298:AAEz9ALOEFUni74uc2tfucTsVqssu3osbs0"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salut! ✅ Botul funcționează!")

bot.polling()
