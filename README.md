# ReminderBot

This Telegram bot allowing the users the set a list of keys (A words using to initiate reminders) and corresponding reminders.
If the bot detects one or more keywords in the chat, it'll send back the corresponding reminders.

The users can take several actions to communicate with the bot:
/start: the bot will return a hello message.
/help: the bot will return a message with all the actions the users can perform.
/insert: the bot will return a message instructing the user how to insert new keys and reminder. If the following message is matching
         the format, the keys and reminders will be added to the database.
/show: the bot will return a table contains keys and reminders currently in the database.
/delete: the bot instruct the user to enter the id of a reminder. If the id is in the database the keys and reminders will be deleted. 

The bot is using the python-telegram-bot library to interact with Telegram Bot API.


