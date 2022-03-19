import random
from numpy import number
import telebot
import time
import logging

from card_list import key_list, val_list
from poker_algorithm import card_list_value, check_valid, card_value, display_value

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot import types
from players import players
from botsetting import bot

#logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

cards = []
players_list = {}
index_id = []
n = 0
p = 0
distributed = 0
start = 0
role = 0
round = 1

def show_cards(cards):
    for i in range(52):                
        cards.append([i%13, int((i)/13)])

@bot.message_handler(commands=['close'])
def close(message):
    global cards
    global players_list
    global n
    global p
    global distributed
    global start
    if(start):
        cards = []
        players_list = {}
        index_id = []
        n = 0
        p = 0
        distributed = 0
        start = 0
        players.all_id = []
        players.all_info = {}
        players.chat_id = ''
        bot.send_message(message.chat.id, "game was closed")
        
@bot.message_handler(commands=["start_b2"])

def start_b2(message):
    global start
    if (players.chat_id == message.chat.id):
        bot.send_message(players.chat_id, "One group cannot exist more than one game")
    else:
        show_cards(cards)
        start = 1
        players.chat_id = message.chat.id
        print(players.chat_id)
        markup = types.ForceReply(selective=True)
        msg = bot.send_message(players.chat_id, "number of player: ", reply_markup=markup)
        bot.register_next_step_handler(msg, number_player)


def number_player(message):
    global n
    try:
        n = int(message.text)        
        join_b2(message)
        bot.send_message(players.chat_id, "/join_b2 to join game")
    except ValueError:
        markup = types.ForceReply(selective=True)
        msg = bot.send_message(players.chat_id, "invalid input, type again", reply_markup=markup)
        bot.register_next_step_handler(msg, number_player)

@bot.message_handler(commands=['join_b2'], func=lambda m: start == 1)

def join_b2(message):
    global p
    if(message.from_user.id in players.all_id):
        bot.send_message(message.chat.id, "Bruh u joined already")
    else:
        players_list[message.from_user.id] = (players(message.from_user.first_name, message.from_user.id, p, message))
        print(message.from_user.id)
        p += 1
        if p == n:
            bot.send_message(players.chat_id, "4 players joined \n Game start!!!\nthis is your poker cards: https://t.me/addstickers/left_pokera \n No Cheating\n/shuffle to shuffle the card")



@bot.message_handler(commands=['shuffle'], func= lambda m: start == 1 and m.from_user.id == players.all_id[0])

def shuffle(message):
    global cards
    random.shuffle(cards)
    print(cards)
    
    for key in players_list.keys():
        list = []
        for i in range(13):
            list.append(cards.pop(0))
        players_list[key].distribute(list)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("13 cards check", switch_inline_query_current_chat='Checkf'))
    
    bot.send_animation(players.chat_id, 'https://i.kym-cdn.com/photos/images/original/000/931/227/eac.gif', )
    bot.send_message(players.chat_id, text= 
    """D'Arby the Gambler has shuffle the cards for us\n
    Player check your cards by clicking the "13 cards" button below\n

    <@LEFT_big_two_bot Checka> to arrange card in assending order
    <@LEFT_big_two_bot Checkd> to arrange descending order
    <@LEFT_big_two_bot Checkf> to arrange on flower (recommended)
     """, reply_markup=markup)

    find_3d(message)


@bot.inline_handler(lambda query: query.query[0:5] == 'Check' and  start == 1)

def reply_to_query(inline_query):
    print(inline_query.from_user.first_name)
    if(inline_query.from_user.id in players.all_id):
        
        if(len(inline_query.query) > 5):
                print("larger than 6")

                if(inline_query.query[5] == 'a'):
                    print("assending")              
                    players_list[inline_query.from_user.id].asscending()

                elif(inline_query.query[5] == 'd'):
                    print("decending")
                    players_list[inline_query.from_user.id].descending()

                elif(inline_query.query[5] == 'f'):
                    print("flower")
                    players_list[inline_query.from_user.id].flower()
                                    
        players_list[inline_query.from_user.id].choose(inline_query)
    else:
        bot.send_message(players.chat_id, f'{inline_query.from_user.first_name} don\'t touch')
@bot.message_handler(commands=['ok'], func=lambda m: start == 1)
def find_3d(message):
    global role
    global role_player
    for id in players.all_id:
        role = 0
        role_player = players_list[players.all_id[role]]

        if([2, 0] in players_list[id].cards):
            bot.send_message(players.chat_id, f'{players_list[id].name} get the diamond 3, he start first')
            role = players_list[id].index
            role_player = players_list[players.all_id[role]]
            print(role_player)
            #role = 0
    round_start()
number_getted = 0
def round_start():
    global number_getted
    number_getted = 0
    players.previous_result = []
    markup = types.ReplyKeyboardMarkup(selective=True)
    markup.add(types.KeyboardButton("x1"))
    markup.add(types.KeyboardButton("x2"))
    markup.add(types.KeyboardButton("x3"))
    markup.add(types.KeyboardButton("x4"))
    markup.add(types.KeyboardButton("x5"))

    bot.send_message(players.chat_id, 
    f"""Round {round}: \n
    {role_player.name}'s turn 
    ({len(role_player.cards)} cards left)\n
    {role_player.name} reply "x1/2/3/4/5"to decide how many cards to be place
    BEFORE u place any cards""",
    reply_markup= markup
    )
    bot.register_next_step_handler_by_chat_id(players.chat_id, check_num)
num = 0
def check_num(message):
    global number_getted
    if(message.from_user.id != players.all_id[role]):
        bot.register_next_step_handler(message, check_num)
    elif(message.content_type != 'text' or not message.text[1].isdigit() or int(message.text[1].isdigit()) < 1 or int(message.text[1].isdigit()) > 5):
        bot.send_message(players.chat_id, "Please reply by x1/2/3/4/5")
        bot.register_next_step_handler(message, check_num)
    else:
        global num
        print(message.text)
        num = message.text[1]
        number_getted = 1
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(f"Choose {num} cards", switch_inline_query_current_chat='Check'))
        bot.send_message(players.chat_id, f"Send {num} cards via the button below", reply_markup=markup)


@bot.chosen_inline_handler(func= lambda s: number_getted == 1 and num != 0 and num != None and start == 1 and  s.from_user.id == players.all_id[role])
def get_cards(chosen_result):
    global sending
    sending = True
    print ("I think role is ")
    print(role)
    x = eval(chosen_result.result_id)
    role_player.tmp.append(role_player.cards.pop(role_player.cards.index(x)))
    print(role_player.__dict__)
    print(len(role_player.tmp))
    print(num)

    if(len(role_player.tmp) == int(num)):
        print(f"player send {num} cards")
        valid = check_valid(role_player.tmp, players.previous_result)
        if(valid[0] == False):
            bot.send_message(players.chat_id, valid[1])
            role_player.regret()
            if(chosen_result.from_user.id == players.previous_player or not players.previous_player):
                round_start()
            else:
                next(back=True)
        else:
            if(len(role_player.cards) == 0):
                bot.send_message(players.chat_id, role_player.name + "win!!!")
            else:
                bot.send_message(players.chat_id, valid[1])
                players.previous_result = role_player.tmp
                players.previous_player = players.all_id[role]
                role_player.tmp = []
                print(role_player.tmp)
        
                next()
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(f"{int(num) - len(role_player.tmp)} cards left", switch_inline_query_current_chat="Check"))
        bot.send_message(players.chat_id, f'Cards passed: {display_value(role_player.tmp)}, /back to regret your choice', reply_markup=markup)
        

def next(back = False):
    global role
    global role_player
    global num
    if(back == False):
        role = (role+1)%n
        print(f"role: {role}")
        role_player = players_list[players.all_id[role]]
        role_player.tmp = []
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(f"Choose {num} cards", switch_inline_query_current_chat='Check'))
    bot.send_message(players.chat_id, 
    f"""Previous: {display_value(players.previous_result)}\n 
    {role_player.name}'s turn \n
    /pass to pass\n
    Place {num} cards by button below
    """, reply_markup=markup)

@bot.message_handler(commands=['pass'], func= lambda m: m.from_user.id == players.all_id[role])
def pass_round(message):
    global role
    if(players.previous_player == players.all_id[(role+1)%n]):
        global round
        global role_player
        role = (role+1)%n
        role_player = players_list[players.all_id[role]]
        round += 1
        round_start()
    else:
        next()


@bot.message_handler(commands=['back'], func= lambda m: m.from_user.id == players.all_id[role])
def back(message):
    global sending
    sending = False
    role_player.regret()
    if(message.from_user.id == players.previous_player):
        round_start()
    else:
        next(back = True)

bot.polling()