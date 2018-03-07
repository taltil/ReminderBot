import csv
import os


class DBManger(object):
    def __init__(self):
        self.filename = "reminderDB.csv"
        if self.is_empty():
            self.id = 1
        else:
            self.id = self.last_id()

    def is_empty(self):
        return self.lines_num() == 0

    def add_line(self, chat_id, key_list, reminder_list):
        line = [str(self.id)]
        self.id += 1
        line.append(chat_id)
        for i in key_list:
            line.append(i)
        line.append(";")
        for i in reminder_list:
            line.append(i)
        with open(self.filename, "a") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(line)

    def find_line(self, chat_id, word):
        flag = False
        return_line = []
        with open(self.filename, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line in csv_reader:
                if (len(line) > 0) and int(line[1]) == chat_id:
                    reminder = line[2:]
                    for i in reminder:
                        if i == word and reminder.index(";") > reminder.index(word):
                            flag = True
                            return_line = line
                            break
                    if flag:
                        break
        return return_line

    def lines_num(self):
        line_count = 0
        with open(self.filename, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line in csv_reader:
                if len(line) > 0:
                    line_count += 1
        return line_count

    def last_id(self):
        with open(self.filename, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line in csv_reader:
                if len(line) > 0:
                    return_id = line[0]
        return int(return_id) + 1

    def return_reminder(self, line):
        # return only the reminder part of the line
        reminders = []
        index = line.index(";")
        for i in range(index + 1, len(line)):
            reminders.append(line[i])
        return reminders

    def return_table(self, chat_id):
        table = "Reminders table:\n"
        with open(self.filename, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line in csv_reader:
                if (len(line) > 0) and int(line[1]) == chat_id:
                    table += "id: " + line[0] + ' '
                    reminder = line[2:]
                    table += "for: "
                    for i in reminder:
                        if i != ';':
                            table += i + ' '
                        if i == ';':
                            table += " reminder are: "
                    table += '\n'
        return table

    def delete_line(self, chat_id, line_id):
        try:
            line_id = int(line_id)
        except:
            return False

        id_found = False
        with open(self.filename, "r") as input, open('temp.csv', "w") as output:
            csv_reader = csv.reader(input, delimiter=',')
            csv_writer = csv.writer(output, delimiter=',')
            for line in csv_reader:
                if len(line) > 0:
                    if int(line[0]) == line_id and int(line[1]) == chat_id:
                        id_found = True
                    else:
                        csv_writer.writerow(line)
        if id_found:
            os.remove(self.filename)
            os.rename('temp.csv', self.filename)
        return id_found
