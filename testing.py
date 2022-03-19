import os
from sympy import N
import telebot
import logging
from telebot import types

sticker = {}


bot = telebot.TeleBot('5247497288:AAHkz-1-1RVVKCshTxqZ1UPpTvUg9scQZpQ')

i = 0
k = 0
j = ['♦️', '♣️', '♥️', '♠️']
list = {}

@bot.message_handler(content_types="sticker")
def get(message):
    global i
    global k
    global list
    list[f'{k}{j[i]}'] = message.sticker.file_id
    print(list)
    if(i == 3):
        k += 1
    i = (i+1)%4

@bot.message_handler(commands=["end"])
def end(message):
    with open('abc.txt', 'w') as f:
        for i in list:
            f.write(i)
    
bot.polling()

