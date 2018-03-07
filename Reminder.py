# Reminder main
import threading
from queue import Queue
from BotHandler import *
from MessageProcessor import *


class Reminder():
    def __init__(self):
        self.messageQueue = Queue()
        self.outputQueue = Queue()
        self.botHandler = None
        self.threads()

    def threads(self):

        bot_thread = threading.Thread(target=self.bot_init(), args=())
        db_thread = threading.Thread(target=self.message_init(), args=())
        bot_thread.daemon = True
        db_thread.daemon = True
        bot_thread.start()
        db_thread.start()
        bot_thread.join()
        db_thread.join()

    def bot_init(self):
        print('starting bot handler')
        self.botHandler = BotHandler(self.messageQueue)

    def message_init(self):
        print('starting message processor')
        while True:
            if not self.messageQueue.empty():
                message = self.messageQueue.get()
                print("message: ",message)
                message_processor = MessageProcessor(message, self.outputQueue)
            if not self.outputQueue.empty():
                output = self.outputQueue.get()
                self.botHandler.output_message(output)

ReminderBot = Reminder()
