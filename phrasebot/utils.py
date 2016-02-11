import logging

import re

import telebot

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('bot.log', encoding="utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
telebot.logger.setLevel(logging.WARN)
telebot.logger.addHandler(fh)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)


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
