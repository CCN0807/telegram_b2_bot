from ast import While
import random
import os
import telebot
import time
import logging

#logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

#bot setting
api = os.environ['big_two_bot_api']

bot = telebot.TeleBot(api)

#assign var
players = ["","","",""]
player_id = []
cards = []
player_c = [[],[],[],[]]


@bot.message_handler(commands=["start_b2"])

def start_b2(message):
    global start
    bot.send_message(message.chat.id, "/join_b2 to join game")
    start = True


@bot.message_handler(commands=['join_b2'])

def join_b2(message):
    global players
    global player_id

    p = 0

    if message.from_user.id in player_id:
        bot.reply_to(message, f"bruh {message.from_user.first_name} u already in game bun 7")
    else:
        while(players[p] != ""):
            p+=1
        players[p] = message.from_user.first_name
        player_id.append(message.from_user.id)
        bot.send_message(message.chat.id, f"player: \n player 1: {players[0]} \n player 2: {players[1]} \n player 3: {players[2]} \n player 4: {players[3]}")

    if p == 0:
        bot.send_message(message.chat.id, "4 players joined \n Game start!!!")
        time.sleep(1)
        bot.send_message(message.chat.id, f"this is your poker cards: {show_cards(cards)} \n No Cheating")
        bot.send_message(message.chat.id, "/shuffle to shuffle the card")

def show_cards(cards):
    for i in range(52):
        cards.append([i%13, int((i)/13)])

    return cards


@bot.message_handler(commands=['shuffle'])

def shuffle(message):
    global cards
    random.shuffle(cards)
    print(cards)
    bot.send_message(message.chat.id, "keep /shuffle or /distribute card")

@bot.message_handler(commands=['distribute'])



def distribute(message):
    global player_c

    for i in range(0,52):
        player_c[int(i/13)].append(cards[i])

    print(player_c[0])

    for i in range(4):
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        for c in player_c[i]:
            print(c)
            x = ''
            if(c[1] == 0):
                x = '♦️'
            
            elif(c[1] == 1):
                x = '♣️'
            elif(c[1] ==2):
                x = '♥️'
            else:
                x = '♠️'
            
            item = telebot.types.KeyboardButton(x + str(c[0]+1))
            markup.add(item)

        bot.send_message(message.chat.id, f"Check you card {players[i]}", reply_markup=markup)


bot.polling()