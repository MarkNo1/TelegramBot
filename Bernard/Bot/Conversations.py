from Bot.BaseEntity.ConversationTHEntity import Conversation
from Bot.Message import Message as msg
from Bot.Plex import read
import subprocess


class WelcomeBack(Conversation):
    def task(self):
        self.sendText('Bernard 0.1 is back online!')
        self.addNextConversationQ(Menu(self))


class Intro(Conversation):
    def task(self):
        self.waitAnswer()
        self.sendText('Welcome to Bernard 0.1')
        self.addNextConversationQ(Menu(self))


class Menu(Conversation):
    def task(self):
        answ = self.sendTextWithKeyboard("Menu'", [
                                         'Download', 'List Contents',
                                         'Credits'])
        cmd = msg.readText(answ)
        if 'Download' in cmd:
            self.addNextConversationQ(Download(self))
        elif 'List Contents' in cmd:
            self.addNextConversationQ(List(self))
        elif 'Credits' in cmd:
            self.addNextConversationQ(Credits(self))
        elif 'Root':
            self.addNextConversationQ(Root(self))
        else:
            self.addNextConversationQ(Menu(self))


class Download(Conversation):
    def task(self):
        self.sendText('Welcome to the download section!')
        self.addNextConversationQ(Menu(self))


class List(Conversation):
    def task(self):
        self.sendText('List of Conentents')
        movies = read('Movies.txt')
        self.sendText(movies)
        self.addNextConversationQ(Menu(self))


class Credits(Conversation):
    def task(self):
        self.sendText('Credits Markno1 (TM)')
        self.addNextConversationQ(Menu(self))


class Root(Conversation):
    def task(self):
        carryOn = True
        resp = self.sendTextWaitAnswer('Insert the password!')
        cmd = msg.readText(resp)
        if cmd == 'Super':
            self.sendText('Password Accepted - Type "quit" to exit')
            while(carryOn):
                try:
                    response = self.sendTextWaitAnswer('>')

                    if msg.readText(response) == 'quit':
                        carryOn = False
                    else:
                        commands = msg.readText(response).split()
                        self.sendText(commands)
                        p = subprocess.Popen(
                            commands,  stdout=subprocess.PIPE, shell=True)
                        (output, err) = p.communicate()
                        out = output.decode('utf-8').split('\n')
                        out = "\n".join(out)
                        self.sendText(out)
                except Exception as e:
                    errorLog = 'Error processing: ' + str(commands)
                    print(errorLog)
                    self.sendText(errorLog)
                    print(e)
        else:
            print('Error! credential non valid')
            self.sendText('Error! credential non valid')
        self.addNextConversationQ(Menu(self))
