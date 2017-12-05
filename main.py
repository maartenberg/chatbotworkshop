import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space
import time
import commands

commanddict = {
    "/start": commands.start,
    "/help": commands.help,
    "/setup": commands.setup,
}

class BattleshipBot(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(BattleshipBot, self).__init__(*args, **kwargs)

        # Initialiseer hier je state
        self.game_state = commands.GamePhase.NONE

    def on_chat_message(self, msg):
        cmd = self.get_command(msg)
        res = cmd(self, msg)

        if res:
            self.sender.sendMessage(res, parse_mode='Markdown')


    def get_command(self, msg):
        firstword = msg['text'].split()[0]
        return commanddict.get(firstword, commands.catchall)

if __name__ == '__main__':
    TOKEN = "326577114:AAGTzxrk9awgd_xpxL07xQji_wkRSJgnV24"
    bot = telepot.DelegatorBot( TOKEN, [
        pave_event_space()(
        per_chat_id(), create_open, BattleshipBot, timeout=1000006),
        ])
    bot.message_loop(run_forever=True)
