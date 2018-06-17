from Bot.Message import Message as msg
from Bot.BaseEntity.QueueTHEntity import QueueTHEntity, TypeQ

import subprocess


class Conversation(QueueTHEntity):
    def __init__(self, convEntity):
        super().__init__(convEntity.user, convEntity.queue)

    def task(self):
        raise NotImplemented

    def waitAnswer(self):
        return self.queue[TypeQ.MSG_RECEIVER].get(block=True)

    def sendText(self, text):
        self.addMessageToSenderQ(msg.createTextMessage(self.user['id'], text))

    def sendTextWaitAnswer(self, text):
        self.sendText(text)
        return self.waitAnswer()

    def sendTextWithKeyboard(self, text, buttonList):
        self.addMessageToSenderQ(
            msg.createKeyboardMessage(self.user['id'], text, buttonList))
        return self.waitAnswer()
