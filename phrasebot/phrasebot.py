import json

import telebot
from config import BOT_TOKEN, DESCRIPTION_FILE
from dataset import Dataset
from utils import logger, user_log_string, sanitize_string


class AudioBot(telebot.TeleBot):
    def __init__(self, token, description_file):
        super(AudioBot, self).__init__(token, threaded=False)
        with open(description_file, encoding="utf-8") as fp:
            description = json.load(fp)
        self.mention_words = set(description['mention_words'])
        self.dataset = Dataset(description_file)

    def audio_list(self, msg):
        logger.info("%s: sending phrase list to user %s" % (msg.text, user_log_string(msg)))
        text = ["Phrase list (use '/say ID' to choose phrase):"]
        for i, title in self.dataset.list_files():
            text.append("*[%2d]*  _%s_" % (i, title))
        self.reply_to(msg, "\n".join(text), parse_mode="Markdown")

    def top_phrases(self, msg):
        logger.info("%s: sending top phrases to user %s" % (msg.text, user_log_string(msg)))
        lines = ["Top phrases (use '/say ID' to choose phrase):"]
        for audio_id, count in self.dataset.top_phrases.most_common(5):
            lines.append(
                "*[%2d]*  _%s_ (%d reproductions)" % (audio_id, self.dataset.get_audio_data(audio_id)['title'], count))
        self.reply_to(msg, "\n".join(lines), parse_mode="Markdown")

    def send_phrase(self, msg, audio_id):
        if 0 <= audio_id < len(self.dataset.data_keys):
            audio, duration = self.dataset.get_phrase(audio_id)
            logger.info("%s: sending phrase #%d to user %s" % (msg.text, audio_id, user_log_string(msg)))
            self.send_audio(msg.chat.id, audio, duration)
        else:
            bot.send_random_phrase(msg)

    def send_random_phrase(self, msg):
        logger.info("%s: sending random phrase to user %s" % (msg.text, user_log_string(msg)))
        audio, duration = self.dataset.random_phrase()
        self.send_audio(msg.chat.id, audio, duration)

    def search_mentions(self, msg):
        msg_plain = sanitize_string(msg.text)
        msg_words = set(msg_plain.split())
        if not self.mention_words.intersection(msg_words):
            return
        logger.info("mention: responding to user %s" % user_log_string(msg))
        audio, duration = self.dataset.random_phrase(msg_words)
        self.send_audio(msg.chat.id, audio, duration)


bot = AudioBot(BOT_TOKEN, DESCRIPTION_FILE)


@bot.message_handler(commands=["list"])
def phrase_list(msg):
    bot.audio_list(msg)


@bot.message_handler(commands=['top'])
def top_phrases(msg):
    bot.top_phrases(msg)


@bot.message_handler(commands=['frase', 'say'])
def send_phrase(msg):
    try:
        audio_id = int(msg.text.split()[1])
        bot.send_phrase(msg, audio_id)
    except (IndexError, ValueError):
        bot.send_random_phrase(msg)


@bot.message_handler()
def search_mentions(msg):
    bot.search_mentions(msg)


bot.polling(none_stop=True)
