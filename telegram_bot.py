#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bot to enrich your conversation with beautiful gifs
"""

import logging
from memeversation import Memeversation
from memeversation import Tracking
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue

m = Memeversation()
stats = Tracking()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Bischd du dumm?')

def usage(update, context):
    """send usage of requested phrase"""
    phrase = " ".join(context.args).lower()
    used = "{0} was used {1} times".format(phrase, stats.evaluate_word(phrase))
    update.message.reply_text(used)

def read(update, context):
    m.update_gif_data()
    word, media = m.get_gif(update.message.text.lower())
    if media:
        update.message.reply_animation(media)

        # collect stats
        stats.update(update.message.from_user.username, word,
            update.message.chat.title)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater("", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("hilfe", help))
    dp.add_handler(CommandHandler("nutzung", usage))

    dp.add_handler(MessageHandler(Filters.text, read))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

