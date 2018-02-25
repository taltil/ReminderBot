from DBManger import *


class MessageProcessor(DBManger):
    def __init__(self, message_list, outputQueue):
        DBManger.__init__(self)
        self.outputQueue = outputQueue
        print('starting message processor')
        if message_list[2]:
            self.add_reminder_to_db(message_list[1])
        else:
            self.message = message_list[1].split()
            reminder_dic = self.find_reminders()
            reminder_text = self.create_reminder_text(reminder_dic)
            self.outputQueue.put(reminder_text)

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
        reminder_line = DBManger.find_line(self, word)
        if len(reminder_line) > 0:
            reminders = self.return_reminder(reminder_line)
        return reminders

    def return_reminder(self, line):
        return DBManger.return_reminder(self, line)

    def add_reminder_to_db(self, message):
        if len(message) == 0:
            self.outputQueue.put('error: no message insert')
            return
        message = message.split(';')
        if (len(message) != 2):
            self.outputQueue.put('error: exactly one ; should be insert')
            return
        if (len(message[0]) == 0 or len(message[1]) == 0):
            self.outputQueue.put('error: keys or reminders are missing')
            return
        key_list = message[0].split(',')
        reminder_list = message[1].split(',')
        DBManger.add_line(self, key_list, reminder_list)

    def create_reminder_text(self, reminder_dic):
        text = ''
        for key, value_list in reminder_dic.items():
            text += 'Reminders For ' + key + ':\n'
            for value in value_list:
                text += value + '\n'
        return text
