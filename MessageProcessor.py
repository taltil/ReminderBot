
from Actions import *


class MessageProcessor():
    def __init__(self, db, message_list, outputQueue):
        self.db=db
        self.outputQueue = outputQueue
        print('starting message processor')
        self.preform_action(message_list)
        self.message=""
        self.chat_id = None

    def preform_action(self, message_list):
        if message_list[3] == Actions.CHECK_FOR_REMINDER:
            self.message = message_list[2].split()
            self.chat_id = message_list[1]
            reminder_dic = self.find_reminders()
            reminder_text = self.create_reminder_text(reminder_dic)
            self.outputQueue.put([reminder_text, self.chat_id])
        elif message_list[3] == Actions.INSERT_TO_DB:
            self.add_reminder_to_db(message_list[1], message_list[2])
        elif message_list[3] == Actions.GET_ALL_REMINDERS:
            table = self.return_table(message_list[1])
            self.outputQueue.put([table, message_list[1]])
        elif message_list[3] == Actions.DELETE_REMINDER:
            self.delete_reminder(message_list[1], message_list[2])

    def find_reminders(self):
        reminder_dic = {}
        # find the reminder of each word in the sentence
        for word in self.message:
            reminder = self.find_word(word)
            if len(reminder) > 0:
                reminder_dic[word] = reminder
        return reminder_dic

    def find_word(self, word):
        # find word in the db
        reminders = []
        reminder_line = self.db.find_line( self.chat_id, word)
        if len(reminder_line) > 0:
            reminders = self.return_reminder(reminder_line)
        return reminders

    def return_reminder(self, line):
        # return only the reminder part of the line
        reminders = []
        index = line.index(";")
        for i in range(index + 1, len(line)):
            reminders.append(line[i])
        return reminders

    def add_reminder_to_db(self, chat_id, message):
        if len(message) == 0:
            self.outputQueue.put(['Error: no message insert!', chat_id])
            return
        message = message.split(';')
        if len(message) != 2:
            self.outputQueue.put(['Error: exactly one ; should be insert!', chat_id])
            return
        if len(message[0]) == 0 or len(message[1]) == 0:
            self.outputQueue.put(['Error: keys or reminders are missing!'.chat_id])
            return
        key_list = message[0].split(',')
        reminder_list = message[1].split(',')
        self.db.add_line(chat_id, key_list, reminder_list)
        self.outputQueue.put(['New reminder was successfully added.', chat_id])

    def create_reminder_text(self, reminder_dic):
        text = ''
        for key, value_list in reminder_dic.items():
            text += 'Reminders For ' + key + ':\n'
            for value in value_list:
                text += value + '\n'
        return text

    def return_table(self, chat_id):
        return  self.db.return_table( chat_id)

    def delete_reminder(self, chat_id, line_id):
        if  self.db.delete_line( chat_id, line_id):
            self.outputQueue.put(['Reminder was successfully deleted.', chat_id])
        else:
            self.outputQueue.put(['Error: id is not valid or not exist.\nPlease try again.', chat_id])
