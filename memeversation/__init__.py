#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .tracking import Tracking

import json
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

    def find_word(self, text):
        for w in text.lower().split():
            if w in self.gif_data:
                return w, self.gif_data[w]

    def write_data_file(self):
        json.dump(self.gif_data, self.data_file.open('w'))

