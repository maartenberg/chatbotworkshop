import telepot
import time
import commands

commands = {"/start": commands.start}


def on_msg(msg):
    command = msg["text"]

    if command in commands.keys():
        commands[command](msg, bot)



if __name__ == '__main__':
    bot = telepot.Bot("238085180:AAEkpdj6JceHn2fjn8f4jCxbFiUCyvTMaLE")

    print('Online...')
    bot.message_loop({'chat': on_msg,
                      })

    while 1:
        time.sleep(10)
