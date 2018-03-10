import sqlite3


class SQLManger(object):
    def __init__(self):
        self.conn, self.cur= self.open_connection()
        if self.is_empty():
            self.id = 1
        else:
            self.id = self.__last_id()

    def open_connection(self):
        conn = sqlite3.connect('reminderDB')
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS reminders(id INT, chat_id INT,key_list TEXT, reminder_list TEXT)")
        return conn, cur

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def is_empty(self):
        self.cur.execute("SELECT * FROM reminders")
        if len(self.cur.fetchall()) > 0:
            return False
        else:
            return True

    def convert_list_to_string(self,l):
        s=''
        for i in l:
            s+=i+','
        return s

    def convert_string_to_list(self,s):
        return s.split(',')


    def add_line(self, chat_id, key_list, reminder_list):
        key_str=self.convert_list_to_string(key_list)
        reminder_str=self.convert_list_to_string(reminder_list)
        self.cur.execute("INSERT INTO  reminders (id, chat_id, key_list, reminder_list) VALUES (?, ? , ? , ?)",
                    (self.id, chat_id, key_str, reminder_str))
        self.conn.commit()
        self.id += 1

    def find_line(self, chat_id, word):
        line=[]
        self.cur.execute("SELECT * FROM reminders WHERE chat_id = ?", (chat_id,))
        data = self.cur.fetchall()
        for row in data:
            for i in self.convert_string_to_list(row[2]):
                if i==word:
                    line.append(str(row[0]))
                    line.append(str(row[1]))
                    for j in self.convert_string_to_list(row[2][:-1]):
                        line.append(j)
                    line.append(";")
                    for j in self.convert_string_to_list(row[3][:-1]):
                        line.append(j)
                    break
        return line


    def __last_id(self):
        self.cur.execute("SELECT * FROM reminders WHERE id=(SELECT MAX(id) FROM reminders)")
        row=self.cur.fetchall()
        if len(row)==0:
            return 1
        return row[0][0]+1

    def return_table(self, chat_id):
        table = "Reminders table:\n"
        self.cur.execute("SELECT * FROM reminders WHERE chat_id = ?", (chat_id,))
        for row in self.cur.fetchall():
            table += "id: " + str(row[0]) + ' '
            table += "for: "+ row[2][:-1]+' '
            table += "reminders are: "+ row[3][:-1]
            table +="\n"
        return table

    def delete_line(self, chat_id, id):
        flag=False
        self.cur.execute("SELECT * FROM reminders WHERE chat_id=? AND id=?", (chat_id, id))
        if len(self.cur.fetchall())>0:
            flag=True
        self.cur.execute("DELETE FROM reminders WHERE chat_id=? AND id=?",(chat_id, id))
        self.conn.commit()
        return flag
