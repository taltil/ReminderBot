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

        botThread = threading.Thread(target=self.botinit(), args=())
        dbThread = threading.Thread(target=self.messageinit(), args=())
        botThread.daemon = True
        dbThread.daemon = True
        botThread.start()
        dbThread.start()
        botThread.join()
        dbThread.join()

    def botinit(self):
        print('starting bot handler')
        self.botHandler = BotHandler(self.messageQueue)

    def messageinit(self):
        print('starting message processor')
        while True:
            while not self.messageQueue.empty():
                message = self.messageQueue.get()
                print(message)
                messageProcessor = MessageProcessor(message, self.outputQueue)
            while not self.outputQueue.empty():
                output = self.outputQueue.get()
                self.botHandler.output_message(output)


ReminderBot = Reminder()
