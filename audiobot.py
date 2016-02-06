# set encoding: utf-8
import json
import logging
import os
import random
import re

import telebot
from tinytag.tinytag import TinyTag
from config import BOT_TOKEN, DESCRIPTION_FILE, MENTION_WORDS

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('bot.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(fh)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


class Dataset:
    def __init__(self, description_file):
        with open(description_file, encoding="utf-8") as fp:
            description = json.load(fp)
        self.path = description['path']
        self.data = description['data']
        self.data_keys = sorted(list(self.data.keys()))
        self.last_random = None

        for key in self.data_keys:
            self.data[key]['keywords'] = set(self.data[key]['keywords'].split())

        logger.info("Dataset loaded with %d audio files" % len(self.data_keys))

    def _audio_candidates(self, words):
        """
        Get audio files with matching keywords
        :param words:
        :return:
        """
        if not words:
            return []
        logger.debug("Searching candidates")
        candidates = []
        for key in self.data_keys:
            word_intersection = words.intersection(self.data[key]['keywords'])
            if words.intersection(self.data[key]['keywords']):
                logger.debug("Matching words: %s" % word_intersection)
                candidates.append(key)
        return candidates

    def get_audio_by_key(self, key):
        path = os.path.join(self.path, key)
        audio = open(path, 'rb')
        tag = TinyTag.get(path)
        return audio, tag.duration

    def get_audio(self, audio_id):
        return self.get_audio_by_key(self.data_keys[audio_id])

    def random_audio(self, words=None):
        audio_candidates = self._audio_candidates(words)
        if audio_candidates:
            key = random.choice(audio_candidates)
        else:
            key = random.choice(self.data_keys)
            # Don't repeat audio file
            while key == self.last_random:
                key = random.choice(self.data_keys)
        return self.get_audio_by_key(key)

    def list_files(self):
        text = []
        for i, key in enumerate(self.data_keys):
            text.append("%2d > %s" % (i, self.data[key]['title']))
        return "\n".join(text)


def user_log_string(msg):
    return "%s:%s (%s %s)" % (
        msg.from_user.id, msg.from_user.username, msg.from_user.first_name, msg.from_user.last_name)


def sanitize_string(text):
    chars_to_remove = "[¡¿!?,.]"
    msg_plain = re.sub(chars_to_remove, "", text.lower())
    replacements = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}
    for old, new in replacements.items():
        msg_plain = msg_plain.replace(old, new)
    return msg_plain


dataset = Dataset(DESCRIPTION_FILE)
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["list"])
def audio_list(msg):
    bot.reply_to(msg, dataset.list_files())


@bot.message_handler(commands=['frase'])
def frase(msg):
    try:
        audio_id = int(msg.text.split()[1])
    except (IndexError, ValueError):
        audio_id = -1
    if 0 <= audio_id < len(dataset.data_keys):
        audio, duration = dataset.get_audio(audio_id)
    else:
        audio, duration = dataset.random_audio()
    logger.info("/frase: responding to user %s" % user_log_string(msg))

    bot.send_audio(msg.chat.id, audio, duration)


@bot.message_handler()
def search_mentions(msg):
    msg_plain = sanitize_string(msg.text)
    msg_words = set(msg_plain.split())
    if not MENTION_WORDS.intersection(msg_words):
        return
    logger.info("mention: responding to user %s" % user_log_string(msg))
    audio, duration = dataset.random_audio(msg_words)
    bot.send_audio(msg.chat.id, audio, duration)


bot.polling(none_stop=True)
