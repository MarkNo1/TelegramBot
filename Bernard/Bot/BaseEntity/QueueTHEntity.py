from threading import Thread
from mark_utils.time import now, delta
from mark_utils.color import Color as c
from queue import Queue
from enum import Enum
import abc

# Queue Enum


class TypeQ(Enum):
    MSG_SENDER = 0
    MSG_RECEIVER = 1
    SWITCH_CONVERSATION = 2


class QueueTHEntity(Thread):
    __metaclass__ = abc.ABCMeta

    def __del__(self):
        self.timeEnd = now()
        time = '[' + str(self.timeEnd) + ']'
        print(c.orange(time), ' End ', self.info(), '| DT: ',
              delta(self.timeStart, self.timeEnd))

    def __init__(self, user, queue):
        Thread.__init__(self)
        self.user = user
        self.entityName = self.__class__.__name__
        self.daemon = True
        self.timeStart = now()
        time = '[' + str(self.timeStart) + ']'
        print(c.green(time), ' Start ', self.info())
        if queue:
            self.queue = queue
        else:
            self.queue = {TypeQ.MSG_SENDER: Queue(),
                          TypeQ.MSG_RECEIVER: Queue(),
                          TypeQ.SWITCH_CONVERSATION: Queue()}

    def info(self):
        return '| ' + str(self.entityName) + '| ' + c.blue(str(self.user['username']))

    def shareQueue(self):
        return self.queue

    def addMessageToSenderQ(self, message):
        self.queue[TypeQ.MSG_SENDER].put(message)

    def addMessageToReceiverQ(self, message):
        self.queue[TypeQ.MSG_RECEIVER].put(message)

    def addNextConversationQ(self, conversation):
        self.queue[TypeQ.SWITCH_CONVERSATION].put(conversation)

    def getMessageFromSenderQ(self):
        return self.queue[TypeQ.MSG_SENDER].get(block=True)

    def getMessageFromReceiverQ(self):
        return self.queue[TypeQ.MSG_RECEIVER].get(block=True)

    def getNextConversationQ(self):
        return self.queue[TypeQ.SWITCH_CONVERSATION].get(block=True)

    def run(self):
        try:
            self.task()
        except Exception as e:
            print(c.red(str(e)))

    @abc.abstractmethod
    def task(self):
        raise NotImplemented
