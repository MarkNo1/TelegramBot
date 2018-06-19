from Bot.Message import Message as msg
from Bot.BaseEntity.QueueTHEntity import QueueTHEntity, TypeQ
from mark_utils.time import now
from mark_utils.color import Color as c


class Conversation(QueueTHEntity):
    def __init__(self, convEntity):
        super().__init__(convEntity.user, convEntity.queue)

    def task(self):
        raise NotImplemented

    def waitAnswer(self):
        time = '[' + str(now()) + ']'
        print(c.green(time), self.info(), '| waiting answer')
        response = self.queue[TypeQ.MSG_RECEIVER].get(block=True)
        print(c.green(time), self.info(), '| response: ',
              c.orange(msg.readText(response)))
        return response

    def sendText(self, text):
        self.addMessageToSenderQ(msg.createTextMessage(self.user['id'], text))
        time = '[' + str(now()) + ']'
        print(c.green(time), self.info(), '| sent: ', c.light_blue(text))

    def sendTextWaitAnswer(self, text):
        self.sendText(text)
        return self.waitAnswer()

    def sendTextWithKeyboard(self, text, buttonList):
        self.addMessageToSenderQ(
            msg.createKeyboardMessage(self.user['id'], text, buttonList))
        time = '[' + str(now()) + ']'
        print(c.green(time), self.info(), '| sent: ', c.light_blue(text))
        return self.waitAnswer()
