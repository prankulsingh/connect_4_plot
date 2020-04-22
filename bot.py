import logging
import os
import connect_4_plot

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hey there!')
    update.message.reply_text('I am "Connect 4 Plot" bot and I organise world level gaming tournaments!')
    update.message.reply_text('Just kidding, but I do let you play the game of Connect 4 with your friends!')
    update.message.reply_text('Use the following commands to begin:\n'
                              '1. /new_game : Use this command to start a new game\n'
                              '2. /help : Don\'t know how to play or use this? Use this command to learn.')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def new_game(update, context):
    new_game_board = "🔵's turn!\n\n1⃣2⃣3⃣4⃣5⃣6⃣7⃣\n⚪⚪⚪⚪⚪⚪⚪\n⚪⚪⚪⚪⚪⚪⚪\n⚪⚪⚪⚪⚪⚪⚪\n⚪⚪⚪⚪⚪⚪⚪\n⚪⚪⚪⚪⚪⚪⚪\n⚪⚪⚪⚪⚪⚪⚪"
    update.message.reply_text(new_game_board)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help will be added soon. I am lazy.')


def make_move(update, context):
    if update.message.reply_to_message is None or update.message.reply_to_message == "":
        update.message.reply_text("Please reply to a game message that I sent, otherwise how will I know previous "
                                  "state of game?")
    else:
        try:
            update.message.reply_text(connect_4_plot.make_move(update.message.reply_to_message.text, update.message.text))
        except Exception as e:
            logger.error('Something went wrong: ' + str(e))
            update.message.reply_text("I don't understand this. 😅")
            update.message.reply_text('I asked gaming minion 👾, he said "' + str(e)+'"')
            update.message.reply_text("There could be two things which might have happened:\n1⃣. Either I am too "
                                      "stupid and made a boo boo\n2⃣. Or you are too stupid and made stupid move and "
                                      "made me crash.\nDon't do that, I don't like it")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    token = ""
    try:
        import credentials
        token = credentials.token
    except Exception as e:
        logger.error("Unable to get token from credentials file: " + str(e))
        try:
            token = os.getenv("TOKEN")
        except Exception as e:
            logger.error("Unable to get token from OS env vars: " + str(e))
            exit(1)

    if token is None or token == "":
        logger.error("Unable to get token!")
        exit(1)

    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("new_game", new_game))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, make_move))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
