#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bot to your conversation with beautiful gifs
"""

from memeversation import Memeversation
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue

m = Memeversation()

# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Bischd du dumm?')

def read(update, context):
    m.update_gif_data()
    match = m.find_word(update.message.text)
    if match:
        update.message.reply_animation(match)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # init
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

