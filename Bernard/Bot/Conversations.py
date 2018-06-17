from Bot.BaseEntity.ConversationTHEntity import Conversation
from Bot.Message import Message as msg

import subprocess


class WelcomeBack(Conversation):
    def task(self):
        self.sendText('Bernard 0.1 is glad to be online again!')
        self.addNextConversationQ(Menu(self))


class Intro(Conversation):
    def task(self):
        self.waitAnswer()
        self.sendText('Welcome to Bernard 0.1')
        self.addNextConversationQ(Menu(self))


class Menu(Conversation):
    def task(self):
        answ = self.sendTextWithKeyboard("What you want to do?", [
                                         'Download', 'List Contents', 'Credits', 'Root'])
        cmd = msg.readText(answ)
        if 'Download' in cmd:
            self.addNextConversationQ(Download(self))
        elif 'List Contents' in cmd:
            self.addNextConversationQ(List(self))
        elif 'Credits' in cmd:
            self.addNextConversationQ(Credits(self))
        else:
            self.addNextConversationQ(Menu(self))


class Download(Conversation):
    def task(self):
        self.sendText('Welcome to the download section!')
        self.addNextConversationQ(Menu(self))


class List(Conversation):
    def task(self):
        self.sendText('List of Conentents')
        p = subprocess.Popen(["ls", '/mnt/Film'],  stdout=subprocess.PIPE)
        (output, err) = p.communicate()
        out = output.decode('utf-8').split('\n')
        out = "\n".join(out)
        self.sendText(out)
        self.addNextConversationQ(Menu(self))


class Credits(Conversation):
    def task(self):
        self.sendText('Credits Markno1 (TM)')
        self.addNextConversationQ(Menu(self))


class Root(Conversation):
    def task(self):
        response = None
        cmd = self.sendTextWaitAnswer('Insert Password!')
        if cmd == 'super':
            while(response != 'exit'):
                response = self.sendTextWaitAnswer('>')
                commands = response.split()
                p = subprocess.Popen(commands,  stdout=subprocess.PIPE)
                (output, err) = p.communicate()
                out = output.decode('utf-8').split('\n')
                out = "\n".join(out)
                self.sendText(out)
            self.addNextConversationQ(Menu(self))
