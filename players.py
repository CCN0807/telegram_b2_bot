from numpy import choose
from telebot.types import InlineKeyboardButton , InlineKeyboardMarkup, InlineQueryResultCachedSticker, InlineQueryResultArticle
from poker_algorithm import card_value
import os

from botsetting import bot
import logging 
from card_list import value_id

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def key(e):
    return (e[0]+1)*10+e[1]
def fkey(e):
    return (e[1]+1)*100 + e[0]
class players:
    previous_player = ''
    previous_result = []
    all_info = {}
    all_id = []
    order = []
    chat_id = ''
    def __init__(self, name, id, index, cards = [], tmp = []):
       
            self.name = name
            self.id = id
            self.cards = cards
            self.tmp = tmp
            self.index = index
            players.all_id.append(self.id)
            players.all_info[self.id] = name
            
            for pid in players.all_id:
                bot.send_message(players.chat_id, f"player{pid}: \n {players.all_info[pid]}")

    def __repr__(self):
        return f'Name : {self.name}, Id : {self.id}, cards : {self.cards}'
    def distribute(self, list):
        self.cards = list

    def choose(self, inline_query, k = 0, num = 0):
        i = 0
        choose_list = []
        for c in self.cards:

            x = card_value(c)
            choose_list.append(InlineQueryResultCachedSticker(f'{c}', value_id[x]))
            i+=1
        bot.answer_inline_query(inline_query.id, choose_list, is_personal=True, cache_time=2)

    def asscending(self):
        self.cards = sorted(self.cards, key=key)
     
    def descending(self):
        self.cards = sorted(self.cards,key=key, reverse = True)
 
    def flower(self):
        self.cards = sorted(self.cards, key=fkey) 
    
    def remove_cards(self, x):
        p = self.cards.index(x)
        self.tmp.append(self.cards.pop(p))
        print(self.name + ': ')
        print(self.tmp)

    def regret(self):
        for i in range(len(self.tmp)):
            self.cards.append(self.tmp.pop(0))



