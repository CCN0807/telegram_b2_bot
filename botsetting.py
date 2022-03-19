import os
import telebot
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

api = os.environ['big_two_bot_api']

bot = telebot.TeleBot(api)
