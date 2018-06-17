from Bot.Bot import Bot
import signal
import sys
import os


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
print('Bot Activated - Press Ctr+C for quit')

print('Bot 0.4 Started with PID: ', os.getpid())

bot = Bot()
bot.activateReciveLoop()

signal.pause()
