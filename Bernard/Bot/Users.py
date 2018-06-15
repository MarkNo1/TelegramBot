from tabulate import tabulate
import time
import os
import re


LOG = './Log_Users.pkl'
W = 'wb'
R = 'rb'
ID = 'id'


class Users:
    def __init__(self):
        self.U = dict()

    def add(self, chat):
        return False if chat[ID] in self.U else self.U.update({chat[ID]: chat})

    def __eq__(self, chat):
        return True if chat[ID] in self.U else False

    def __call__(self, id):
        return self.U[id] if id in self.U else None

    def __str__(self):
        pass

    def save(self):
        with open(LOG, W) as fd:
            pickle.dump(items, fd)

    def load(self):
        with open(LOG, R) as fd:
            return pickle.load(fd)
