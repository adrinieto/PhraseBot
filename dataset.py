import collections
import json
import os
import random

from tinytag import TinyTag
from utils import logger

TOP_PHRASES_FILE = "top_phrases.json"


class Dataset:
    def __init__(self, description_file):
        with open(description_file, encoding="utf-8") as fp:
            description = json.load(fp)
        self.path = description['path']
        self.data = description['data']

        self.data_keys = sorted(list(self.data.keys()))
        self.top_phrases = self.load_top_phrases(TOP_PHRASES_FILE)
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

    def get_audio_data(self, audio_id):
        return self.data[self.data_keys[audio_id]]

    def get_phrase_by_key(self, key):
        path = os.path.join(self.path, key)
        audio = open(path, 'rb')
        tag = TinyTag.get(path)
        return audio, tag.duration

    def get_phrase(self, audio_id):
        self.increase_top_phrases(audio_id)
        return self.get_phrase_by_key(self.data_keys[audio_id])

    def random_phrase(self, words=None):
        audio_candidates = self._audio_candidates(words)
        if audio_candidates:
            key = random.choice(audio_candidates)
            index = self.data_keys.index(key)
            self.increase_top_phrases(index)
        else:
            key = random.choice(self.data_keys)
            # Don't repeat audio file
            while key == self.last_random:
                key = random.choice(self.data_keys)
        return self.get_phrase_by_key(key)

    def list_files(self):
        files_by_id = [(i, self.data[key]['title']) for i, key in enumerate(self.data_keys)]
        return files_by_id

    def increase_top_phrases(self, audio_id):
        self.top_phrases.update([audio_id])
        self.save_top_phrases()

    def save_top_phrases(self):
        with open(TOP_PHRASES_FILE, 'w') as fp:
            json.dump(self.top_phrases, fp)

    def load_top_phrases(self, top_phrases_file):
        if not os.path.exists(top_phrases_file):
            return collections.Counter()
        with open(top_phrases_file) as fp:
            json_top = json.load(fp)
            json_top_converted = {int(key): int(val) for key, val in json_top.items()}
            for i in range(len(self.data_keys)):
                if i not in json_top_converted:
                    json_top_converted.update({i: 0})
            return collections.Counter(json_top_converted)
