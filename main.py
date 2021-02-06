"""Simple inline keyboard bot with multiple CallbackQueryHandlers.
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
import logging
import time
import os
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND = range(2)
# Callback data
ONE, TWO, THREE, FOUR, END = range(5)


def start(update: Update, context: CallbackContext) -> None:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("Info", callback_data=str(ONE)),
            InlineKeyboardButton("Features", callback_data=str(TWO)),
            ],
           [InlineKeyboardButton("Aggiungimi ad un gruppo", url=str("t.me/doggycheems_bot?startgroup=bot")),
            InlineKeyboardButton("Updates", url=str("t.me/doggybotupdates")),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("🇮🇹: Ciao questo è un bot siluppato da @doggy_cheems, per ora è inutile ma verrà aggiornato\n🇬🇧: Hey this is a bot developed by @doggy_cheems, for now it's useless but it will be updated soon", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


def start_over(update: Update, context: CallbackContext) -> None:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Info", callback_data=str(THREE)),
            InlineKeyboardButton("Features", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    query.edit_message_text(text="🇮🇹: Ciao questo è un bot siluppato da @doggy_cheems, per ora è inutile ma verrà aggiornato\n🇬🇧: Hey this is a bot developed by @doggy_cheems, for now it's useless but it will be updated soon", reply_markup=reply_markup)
    return FIRST


def one(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Info", callback_data=str(THREE)),
            InlineKeyboardButton("Features", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="🇮🇹: Ciao questo è un bot siluppato da @doggy_cheems.\n🇬🇧: Hey this is a bot developed by @doggy_cheems.", reply_markup=reply_markup)
    return FIRST


def two(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Indietro", callback_data=str(ONE)),
            InlineKeyboardButton("Opzioni", callback_data=str(FOUR)),
            ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="FEATURES:\n1)Mandare il benvenuto (per ora predefinito) nel gruppo\n2)Scaricare video da  youtube(comando /ytdl) RICORDA: il bot è ancora in fase di testing, le nuove feature arriveranno dopo", reply_markup=reply_markup
    )
    return FIRST


def three(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Indietro", callback_data=str(ONE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="VERSIONE BOT: 1.0.🥳\n bot scritto in python 3.9.1 e hostato su uno smartphone per vedere le prestazioni, per info chiedere a @doggy_cheems", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return SECOND


def four(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Indietro", callback_data=str(TWO)),
            InlineKeyboardButton("Menu principale", callback_data=str(ONE)),
        ],
            [InlineKeyboardButton("Richiedi feature", url=str("t.me/doggy_cheems_bot")),
            InlineKeyboardButton("Segnala bug", url=str("t.me/doggy_cheems")),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Ciao qui avrai la possibilità di richiedere feature o segnalare bug del bot, per qualsiasi altro problema che non sia richiesta di feature o bug puoi selezionare l'opzione per  segnalare bug", reply_markup=reply_markup
    )
    return FIRST


def end(update: Update, context: CallbackContext) -> None:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="yoooo un easter egg")
    return ConversationHandler.END

def five(update: Update, context: CallbackContext) -> None:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("info", callback_data=str(ONE)),
            InlineKeyboardButton("features", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    query.edit_message_text(text="🇮🇹: Ciao questo è un bot siluppato da @doggy_cheems, per ora è inutile ma verrà aggiornato\n🇬🇧: Hey this is a bot developed by @doggy_cheems, for now it's useless but it will be updated soon", reply_markup=reply_markup)
    return FIRST

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("1521937075:AAFzUp-yZEGpbrRxwlm3BMXFFY15hfV5oIw")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
                CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$'),
            ],
            SECOND: [
                CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------













if __name__ == '__main__':
    main()