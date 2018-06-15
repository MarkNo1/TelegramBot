from threading import Thread

from telepot.loop import MessageLoop
import telepot

from Bot.Users import Users
from Bot.Message import Message as msg
from Bot.Conversation import Conversation
from Bot.Session import Session


def readKey():
    with open('Key', 'r')as fd:
        return fd.read().split()[0]


class Bot():
    def __init__(self):
        self.bot = telepot.Bot(readKey())
        self.users = Users()
        self.sessions = dict()
        # self.users.load()

    def activateReciveLoop(self):
        MessageLoop(self.bot, self.messagesDispacher).run_as_thread()

    def messagesDispacher(self, message):
        id = msg.readID(message)
        if id in self.sessions:
            ses = self.sessions[id]
            ses.q_rcv.put(message)
        else:
            self.sessions[id] = Session(id)
            self.sessions[id].start()
            self.sessions[id].q_rcv.put(message)
            self.activateSenderThread(self.sessions[id].q_snd)

    def activateSenderThread(self, q_snd):
        self.thSender = Thread(target=self.senderThread, kwargs={'q_snd': q_snd})
        self.thSender.daemon = True
        self.thSender.start()

    def senderThread(self, q_snd):
        while True:
            message = q_snd.get(block=True)
            self.bot.sendMessage(**message)
