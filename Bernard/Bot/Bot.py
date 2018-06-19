from threading import Thread
import os

from telepot.loop import MessageLoop
import telepot

from Bot.Users import Users
from Bot.Message import Message as msg
from Bot.Session import Session
from Bot.Plex import read
from Plex import mPlex


def readKey():
    with open('Key', 'r')as fd:
        return fd.read().split()[0]


class Bot():
    def __init__(self):
        self.bot = telepot.Bot(readKey())
        self.myPlex = mPlex()
        self.users = Users()
        self.currentSession = dict()
        self.users.load()
        for user in self.users.U.values():
            self.initSession(user, True)

    def initSession(self, user, welcomeBack=False):
        self.currentSession[user['id']] = Session(
            user, welcomeBack=welcomeBack)
        self.currentSession[user['id']].start()
        self.activateSenderThread(self.currentSession[user['id']].getSenderQ())

    def activateReciveLoop(self):
        MessageLoop(self.bot, self.messagesDispachter).run_as_thread()

    def messagesDispachter(self, message):
        user = msg.readUser(message)
        if not user == self.users:
            self.addNewUser(user)
            self.initSession(user)

        print(self.currentSession[user['id']])
        self.currentSession[user['id']].addMessageToReceiverQ(message)

    def addNewUser(self, user_info):
        print('Adding new user : ', user_info['id'])
        self.users.add(user_info)
        self.users.save()

    def activateSenderThread(self, q_snd):
        self.thSender = Thread(target=self.senderThread,
                               kwargs={'q_snd': q_snd})
        self.thSender.daemon = True
        self.thSender.start()

    def senderThread(self, q_snd):
        while True:
            message = q_snd.get(block=True)
            self.bot.sendMessage(**message)
