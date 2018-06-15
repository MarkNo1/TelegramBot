from threading import Thread
from queue import Queue

from Bot.Conversation import Intro


class Session(Thread):
    def __init__(self, id, intro=True):
        Thread.__init__(self)
        print('Session created')
        self.id = id
        self.q_snd = Queue()
        self.q_rcv = Queue()
        self.q_conv = Queue()
        self.daemon = True
        if intro:
            self.q_conv.put(Intro(self.id, self.q_snd, self.q_rcv, self.q_conv))
        else:
            # welcome
            pass

    def run(self):
        # Init session with conversation 1
        while(True):
            if not self.q_conv.empty():
                conversation = self.q_conv.get()
                conversation.start()
                print('Conversation: {}  started. '.format(conversation.name))
                conversation.join()
