#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bot to display food of the TH Rosenheim canteen
"""

import json
import logging
import os
from pathlib import Path
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue

data_file = Path('gifs.json')
last_modified = 0
gif_data = {}

# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def populate_gif_data():
    gif_data.clear()
    gif_data.update(json.loads(data_file.open().read()))
    last_modified = data_file.stat().st_mtime

def find_word(text):
    for w in text.lower().split():
        if w in gif_data:
            return gif_data[w]

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Bischd du dumm?')

def read(update, context):
    if last_modified < data_file.stat().st_mtime:
        populate_gif_data()
    match = find_word(update.message.text)
    if match:
        update.message.reply_animation(match)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # init
    populate_gif_data()
    updater = Updater("", use_context=True)
    dp = updater.dispatcher

    # commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("hilfe", help))

    dp.add_handler(MessageHandler(Filters.text, read))

    # logging
    dp.add_error_handler(error)

    # start
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

