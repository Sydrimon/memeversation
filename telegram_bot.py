#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bot to enrich your conversation with beautiful gifs
"""

import logging
from memeversation import Memeversation
from memeversation import Tracking
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

m = Memeversation()
stats = Tracking()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hi!')

async def help(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text('Bischd du dumm?')

async def usage(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """send usage of requested phrase"""
    phrase = " ".join(context.args).lower()
    used = "{0} was used {1} times".format(phrase, stats.evaluate_word(phrase))
    await update.message.reply_text(used)

async def read(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    m.update_gif_data()
    word, media = m.get_gif(update.message.text.lower())
    if media:
        # collect stats
        stats.update(update.message.from_user.username, word,
            update.message.chat.title)

        await update.message.reply_animation(media)

def error(update, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    application = Application.builder().token("").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hilfe", help))
    application.add_handler(CommandHandler("nutzung", usage))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, read))

    application.add_error_handler(error)

    application.run_polling(allowed_updates=Update.MESSAGE)

if __name__ == '__main__':
    main()

