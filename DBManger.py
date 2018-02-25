import csv


class DBManger(object):
    def __init__(self):
        self.filename = "reminderDB.csv"
        if self.isEmpty():
            self.id = 1
        else:
            self.id = self.last_id()

    def isEmpty(self):
        return self.lines_num() == 0

    def add_line(self, key_list, reminder_list):
        line = [str(self.id)]
        self.id += 1
        for i in key_list:
            line.append(i)
        line.append(";")
        for i in reminder_list:
            line.append(i)
        with open(self.filename, "a") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(line)

    def find_line(self, word):
        flag = False
        return_line = []
        with open(self.filename, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line in csv_reader:
                for i in line:
                    if i == word and line.index(";") > line.index(word):
                        flag = True
                        return_line = line
                        break
                if flag:
                    break
        return return_line

    def lines_num(self):
        row_count = 0
        with open(self.filename, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if (len(row) > 0):
                    row_count += 1
        return row_count

    def last_id(self):
        with open(self.filename, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if (len(row) > 0):
                    id = row[0]
        return int(id) + 1

    def return_reminder(self, line):
        # return only the reminder part of the line
        reminders = []
        index = line.index(";")
        for i in range(index + 1, len(line)):
            reminders.append(line[i])
        return reminders
