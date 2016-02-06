# set encoding: utf-8
import json
import logging
import os
import random

import telebot
from tinytag.tinytag import TinyTag

BOT_TOKEN = "YOUR_TOKEN"

DESCRIPTION_FILE = "dataset.json"
MENTION_WORD = "YOUR_WORD"

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('bot.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(fh)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)


class Dataset:
    def __init__(self, description_file):
        with open(description_file) as fp:
            description = json.load(fp)
        self.path = description['path']
        self.data = description['data']
        self.data_keys = list(self.data.keys())

    def random_key(self):
        return random.choice(self.data_keys)

    def random_audio(self):
        key = self.random_key()
        path = os.path.join(self.path, key)
        audio = open(path, 'rb')
        tag = TinyTag.get(path)
        return audio, tag.duration


dataset = Dataset(DESCRIPTION_FILE)
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['frase'])
def frase(msg):
    audio, duration = dataset.random_audio()
    bot.send_audio(msg.chat.id, audio, duration)


@bot.message_handler()
def search_mentions(msg):
    if MENTION_WORD not in msg.text.lower():
        return
    logger.info("Responding to user %s" % msg.chat.id)
    audio, duration = dataset.random_audio()
    bot.send_audio(msg.chat.id, audio, duration)


bot.polling(none_stop=True)
