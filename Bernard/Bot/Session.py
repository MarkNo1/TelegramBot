from Bot.Conversations import Intro, WelcomeBack
from Bot.BaseEntity.QueueTHEntity import QueueTHEntity, TypeQ


class Session(QueueTHEntity):
    def __init__(self, user, queue=None, welcomeBack=False):
        super().__init__(user, queue)
        if welcomeBack:
            self.addNextConversationQ(WelcomeBack(self))
        else:
            self.addNextConversationQ(Intro(self))

    def getSenderQ(self):
        return self.queue[TypeQ.MSG_SENDER]

    def task(self):
        while(True):
            conversation = self.getNextConversationQ()
            conversation.start()
            conversation.join()
