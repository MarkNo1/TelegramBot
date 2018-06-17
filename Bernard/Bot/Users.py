from tabulate import tabulate
import time
import os
import re
import pickle

LOG = './Bot/log/Users.pkl'
W = 'wb'
R = 'rb'
ID = 'id'


class Users:
    def __init__(self):
        self.U = dict()

    def add(self, user):
        return False if user[ID] in self.U else self.U.update({user[ID]: user})

    def __eq__(self, user):
        return True if user[ID] in self.U else False

    def __call__(self, user):
        return self.U[user[ID]] if user[ID] in self.U else None

    def __str__(self):
        pass

    def save(self):
        with open(LOG, W) as fd:
            pickle.dump(self.U, fd)

    def load(self):
        if os.path.exists(LOG):
            with open(LOG, R) as fd:
                self.U = pickle.load(fd)
