import telegram
import telegram.ext
from time import time
from queue import Queue

class BotHandler(object):
    def __init__(self, messageQueue):
        self.filename = "token.txt"
        self.token = self.get_token()
        self.flag = False
        self.bot = telegram.Bot(self.token)
        self.updater = telegram.ext.Updater(token=self.token)
        self.job_queue = self.updater.job_queue
        self.output_queue = Queue()
        self.due = 5
        self.dispatcher = self.updater.dispatcher
        self.start_handler = telegram.ext.CommandHandler('start', self.start)
        self.dispatcher.add_handler(self.start_handler)
        self.updater.start_polling()
        self.insert_handler = telegram.ext.CommandHandler('insert', self.insert_reminder)
        self.dispatcher.add_handler(self.insert_handler)
        self.help_handler = telegram.ext.CommandHandler('help', self.help_info)
        self.dispatcher.add_handler(self.help_handler)
        self.message_handler = telegram.ext.MessageHandler(telegram.ext.Filters.text, self.get_message)
        self.dispatcher.add_handler(self.message_handler)
        self.message_queue = messageQueue

    def get_token(self):
        with open(self.filename, "r") as tokenfile:
            token = tokenfile.read()
        return token

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="I'm a reminder bot!")

    def get_message(self, bot, update):
        # if flag is true than text is lists for DB
        # if flag is false than need to check text for reminders
        text = update.message.text
        self.insert_to_queue(time(), text, self.flag)
        self.flag = False
        job = self.job_queue.run_once(self.sent_message, self.due, context=update.message.chat_id)

    def insert_reminder(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Please insert the two lists with ; to separate them")
        bot.send_message(chat_id=update.message.chat_id, text="Example: key1, key2, key3 ; reminder1, reminder2")
        self.flag = True

    def help_info(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text="This is a reminder bot.\nTo insert to reminder please enter /insert and press enter.\n")
        bot.send_message(chat_id=update.message.chat_id,
                         text="next message will be a list of words to initiate reminder, then ; and then list of words to reminde off")

    def insert_to_queue(self, message_time, text, flag):
        print('insert in queue: ' + text)
        self.message_queue.put([message_time, text, flag])

    def output_message(self, message_text):
        self.output_queue.put(message_text)
        print(self.output_queue.qsize())

    def sent_message(self, bot, job):
        if not self.output_queue.empty():
            message = self.output_queue.get()
            print(message)
            bot.send_message(job.context, text=message)
