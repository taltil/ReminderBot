import telegram
import telegram.ext
from Actions import *
from time import time
import logging


class BotHandler(object):
    def __init__(self, message_queue):
        self.filename = "token.txt"
        self.token = self.get_token()
        self.action = Actions.NOT_SET
        self.bot = telegram.Bot(self.token)
        self.updater = telegram.ext.Updater(token=self.token)
        self.dispatcher = self.updater.dispatcher
        self.start_handler = telegram.ext.CommandHandler('start', self.start)
        self.dispatcher.add_handler(self.start_handler)
        self.updater.start_polling()
        self.insert_handler = telegram.ext.CommandHandler('insert', self.insert_reminder)
        self.dispatcher.add_handler(self.insert_handler)
        self.show_table_handler = telegram.ext.CommandHandler('show', self.show_table)
        self.dispatcher.add_handler(self.show_table_handler)
        self.delete_reminder_handler = telegram.ext.CommandHandler('delete', self.delete_reminder)
        self.dispatcher.add_handler(self.delete_reminder_handler)
        self.help_handler = telegram.ext.CommandHandler('help', self.help_info)
        self.dispatcher.add_handler(self.help_handler)
        self.message_handler = telegram.ext.MessageHandler(telegram.ext.Filters.text, self.get_message)
        self.dispatcher.add_handler(self.message_handler)
        self.message_queue = message_queue
        self.log_bot()

    def log_bot(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()

    def get_token(self):
        with open(self.filename, "r") as tokenfile:
            token = tokenfile.read()
        return token

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="I'm a reminder bot!")

    def get_message(self, bot, update):
        text = update.message.text
        chat_id = update.message.chat_id
        print("message: ", text, "  chat_id:  ", chat_id)
        if self.action == Actions.NOT_SET:
            self.action = Actions.CHECK_FOR_REMINDER
        self.insert_to_queue(time(), chat_id, text, self.action)
        self.action = Actions.NOT_SET

    def insert_reminder(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Please insert the two lists with ; to separate them.")
        bot.send_message(chat_id=update.message.chat_id, text="Example: key1, key2, key3 ; reminder1, reminder2")
        self.action = Actions.INSERT_TO_DB

    def show_table(self, bot, update):
        self.insert_to_queue(time(), update.message.chat_id, "show_table", Actions.GET_ALL_REMINDERS)

    def delete_reminder(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="To delete a reminder, please enter ID.")
        self.action = Actions.DELETE_REMINDER

    def help_info(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text="This is a reminder bot.\nTo insert to reminder please enter /insert and press enter.\n")
        bot.send_message(chat_id=update.message.chat_id,
                         text="Next message should be a list of words to initiate reminder (keys), then ; (to sperate the lists) followed by list of words to reminde off (reminders).")
        bot.send_message(chat_id=update.message.chat_id,
                         text="To see all the reminders inserted to bot, please enter /show and press enter.\n")
        bot.send_message(chat_id=update.message.chat_id,
                         text="To Delete reminder by ID, please enter /delete and press enter.\n")

    def insert_to_queue(self, message_time, chat_id, text, flag):
        print('insert in queue: ' + text)
        self.message_queue.put([message_time, chat_id, text, flag])

    def output_message(self, task):
        task_message = task[0]
        task_id = task[1]
        if len(task_message) > 0:
            try:
                self.bot.send_message(chat_id=task_id, text=task_message)
            except:
                print("error in sending ", task_message, " to chat id ", task_id)
