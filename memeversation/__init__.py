#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .tracking import Tracking

import json
import re
from pathlib import Path

class Memeversation:

    def __init__(self, data_file=Path('data/gifs.json')):
        self.data_file = data_file
        self.last_modified = 0
        self.gif_data = {}

        self.add_gif_data(self.data_file)

    def add_gif_data(self, gif_json):
        self.gif_data.update(json.loads(gif_json.open().read()))

    def empty_gif_data(self):
        self.gif_data.clear()
        
    def update_gif_data(self):
        if self.last_modified < self.data_file.stat().st_mtime:
            self.add_gif_data(self.data_file)
            self.last_modified = self.data_file.stat().st_mtime

    def write_data_file(self):
        json.dump(self.gif_data, self.data_file.open('w'))

    def find_word(self, text):
        for word in text.lower().split():
            if word in self.gif_data:
                return word, self.gif_data[word]

    def create_word_list(self, text):
        phrases = text.lower().split()
        for i, word in enumerate(text.lower().split()):
            if i < len(phrases) - 1:
                new = " ".join(phrases[i:i+1])
                phrases.append(new)
                if i < len(phrases) - 2:
                    new = " ".join(phrases[i:i+2])
                    phrases.append(new)
        return phrases

    def get_gif(self, text):
        phrases = self.create_word_list(text)
        for p in phrases:
            if p in self.gif_data:
                return p, self.gif_data[p]

