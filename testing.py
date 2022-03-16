import os
import telebot

API_KEY = os.environ['tkt_api']

bot = telebot.TeleBot(API_KEY)


@bot.inline_handler(lambda query: query.query == 'gif')
def query_text(inline_query):
    bot.reply_to(inline_query, "hi")

bot.polling()
