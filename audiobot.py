# set encoding: utf-8
import logging
import os
import random

import telebot
from tinytag.tinytag import TinyTag

BOT_TOKEN = "YOUR_TOKEN"

AUDIO_FOLDER = "data/"
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

audio_files = [file for file in os.listdir(AUDIO_FOLDER) if os.path.isfile(os.path.join(AUDIO_FOLDER, file))]
logger.info("Loaded with %d audio files" % len(audio_files))


def user_log_string(msg):
    return "%s:%s (%s %s)" % (
        msg.from_user.id, msg.from_user.username, msg.from_user.first_name, msg.from_user.last_name)


def random_audio(files):
    audio_file = random.choice(files)
    path = os.path.join(AUDIO_FOLDER, audio_file)
    audio = open(path, 'rb')
    tag = TinyTag.get(path)
    return audio, tag.duration


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['frase'])
def frase(msg):
    logger.info("/frase: responding to user %s" % user_log_string(msg))
    audio, duration = random_audio(audio_files)
    bot.send_audio(msg.chat.id, audio, duration)


@bot.message_handler()
def search_mentions(msg):
    if MENTION_WORD not in msg.text.lower():
        return
    logger.info("mention: responding to user %s" % user_log_string(msg))
    audio, duration = random_audio(audio_files)
    bot.send_audio(msg.chat.id, audio, duration)


bot.polling(none_stop=True)
