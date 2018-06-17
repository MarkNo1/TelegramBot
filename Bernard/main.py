from Bot.Bot import Bot
import signal
import sys


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
print('Bot Activated - Press Ctr+C for quit')


bot = Bot()
bot.activateReciveLoop()

signal.pause()
