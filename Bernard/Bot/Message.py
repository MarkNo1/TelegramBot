from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from tabulate import tabulate
import datetime as dt


class Message:
    @staticmethod
    def createTextMessage(id, text):
        return {'chat_id': id, 'text': text}

    @staticmethod
    def createKeyboardMessage(id, text, keyboardConent):
        buttons = [[KeyboardButton(text=button)]
                   for button in keyboardConent]
        keyboard = ReplyKeyboardMarkup(
            keyboard=buttons, one_time_keyboard=True, resize_keyboard=True)
        return {'chat_id': id, 'text': text, 'reply_markup': keyboard}

    @staticmethod
    def readID(message):
        return message['chat']['id']

    @staticmethod
    def readText(message):
        return message['text']
