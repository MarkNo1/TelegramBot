import abc
from threading import Thread
import signal

from Bot.Message import Message as msg


class Conversation(Thread):
    __metaclass__ = abc.ABCMeta

    def __init__(self, id, q_snd, q_rcv, q_conv):
        Thread.__init__(self)
        self.name = self.__class__.__name__
        self.id = id
        self.q_snd = q_snd
        self.q_rcv = q_rcv
        self.q_conv = q_conv
        self.daemon = True

    @abc.abstractmethod
    def loop(self):
        raise NotImplemented

    def run(self):
        try:
            self.loop()
        except Exception as e:
            print(e)

    def waitAnswer(self):
        return self.q_rcv.get(block=True)

    def sendText(self, text):
        self.q_snd.put(msg.createTextMessage(self.id, text))

    def sendQuestionKeyboard(self, text, buttonList):
        self.q_snd.put(msg.createKeyboardMessage(self.id, text, buttonList))
        return self.waitAnswer()


class Intro(Conversation):
    def loop(self):
        answ = self.waitAnswer()
        self.sendText('Welcome to Bernard 0.1')
        # self.sendText("D'abord we can have a small conversation")
        # answ = self.sendQuestionKeyboard("Are you interested to watch Movie/Series in FHD and for free?", ['Yes', 'No'])
        self.q_conv.put(Menu(self.id, self.q_snd, self.q_rcv, self.q_conv))


class Menu(Conversation):
    def loop(self):
        answ = self.sendQuestionKeyboard("What you want to do?", ['Download', 'List Movie', 'Credits'])
        cmd = msg.readText(answ)
        if 'Download' in cmd:
            self.q_conv.put(Download(self.id, self.q_snd, self.q_rcv, self.q_conv))
        elif 'List Movie' in cmd:
            self.q_conv.put(ListMovie(self.id, self.q_snd, self.q_rcv, self.q_conv))
        elif 'Credits' in cmd:
            self.q_conv.put(Credits(self.id, self.q_snd, self.q_rcv, self.q_conv))
        else:
            self.q_conv.put(Menu(self.id, self.q_snd, self.q_rcv, self.q_conv))


class Download(Conversation):
    def loop(self):
        self.sendText('Welcome to the download section!')
        self.q_conv.put(Menu(self.id, self.q_snd, self.q_rcv, self.q_conv))


class ListMovie(Conversation):
    def loop(self):
        self.sendText('Welcome to the list of movie section!')
        self.q_conv.put(Menu(self.id, self.q_snd, self.q_rcv, self.q_conv))


class Credits(Conversation):
    def loop(self):
        self.sendText('Credits Markno1 (TM)')
        self.q_conv.put(Menu(self.id, self.q_snd, self.q_rcv, self.q_conv))
