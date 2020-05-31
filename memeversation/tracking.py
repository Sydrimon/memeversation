#!/usr/bin/env python
# -*- coding: utf-8 -*-

import atexit
import json
import logging
from pathlib import Path

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Tracking:
    """collect usage stats"""

    def __init__(self, data_path=Path('data/stats.json'), cache_size=30):
        self.__data_path = data_path
        self.__cache_size = cache_size
        self.__cache_counter = 0

        self.__user_stats = dict()
        self.__group_stats = dict()
        self.__word_stats = dict()

        self.__user_key = 'user'
        self.__group_key = 'group'
        self.__word_key = 'word'

        if self.__data_path.is_file():
            self.__load_data()

        # register exit handler
        atexit.register(self.__write_data)

    def __load_data(self):
        """load from the stats file"""
        logger.info("loading statistics")
        json_object = json.loads(self.__data_path.open().read()) 

        self.__user_stats.update(json_object[self.__user_key])
        self.__group_stats.update(json_object[self.__group_key])
        self.__word_stats.update(json_object[self.__word_key])
        

    def __write_data(self):
        """write to the stats file"""
        logger.info("writing statistics")
        stats = {}
        stats[self.__user_key] = self.__user_stats
        stats[self.__group_key] = self.__group_stats
        stats[self.__word_key] = self.__word_stats
        json.dump(stats, self.__data_path.open('w'))
    
    def __save(self):
        """cache up to cache limit, then call write_data"""
        logger.debug("checking cache")
        self.__cache_counter += 1
        if self.__cache_counter >= self.__cache_size:
            self.__write_data()    

    def __update_user(self, user):
        """update user count"""
        logger.debug("updating user %s", user)
        self.__user_stats[user] = self.__user_stats.get(user, 0) + 1

    def __update_group(self, group):
        """update group count"""
        logger.debug("updating group %s", group)
        self.__group_stats[group] = self.__group_stats.get(group, 0) + 1

    def __update_word(self, word):
        """update word count"""
        logger.debug("updating word %s", word)
        self.__word_stats[word] = self.__word_stats.get(word, 0) + 1

    def update(self, user, word, group=None):
        """update all stats"""
        self.__update_user(user)
        self.__update_word(word)
        if group:
            self.__update_group(group)
        self.__save()

    def evaluate_word(self, word):
        """return counter for given word"""
        return self.__word_stats.get(word, 0)

