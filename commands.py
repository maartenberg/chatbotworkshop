import enum
import bot_behaviour
import pybattleships
from pybattleships.ship import Ship
from pybattleships.board import Board
from pybattleships.game import Game
import pybattleships.game

class GamePhase(enum.IntEnum):
    NONE = 0
    SETUP = 1
    GAME = 2
    ENDED = 3

def start(bot, msg):
    return "kom vegte dan"

def help(bot, msg):
    helptekst = '''/help - Read this wonderful text again.
/setup - Begin placing your ships.
/playgame - Finish placing ships and get shot at.
'''

    return helptekst

def setup(bot, msg):
    bot.game_state = GamePhase.SETUP
    bot.ships = []
    return 'Now give me 10 messages formatted like `(A1, H, 3)`.'
# hoeveel schippa's van welke lengte
# wat de fuck is een horizontal todo

def playgame(bot, msg):
    bot.game_state = GamePhase.GAME
    can_start = bot.game.start_game()
    if not can_start:
        return 'Somehow the game broke'
    return 'Good now what do you want to shoot at?'

def catchall(bot, msg):
    if bot.game_state == GamePhase.SETUP:
        try:
            if msg['text'].lower() == 'default':
                bot.ships = debug_ships()
            else:
                s = Ship.parse_notation(msg['text'])
                bot.ships.append(s)

            if len(bot.ships) == 10:
                try:
                    b = pybattleships.board.Board(bot.ships)
                    bot.sender.sendMessage( 'Board accepted, start game with /playgame')
                    bot_behaviour.initialize(bot)
                    b2 = bot_behaviour.generate_board(bot)
                    bot.game = Game("player", "bot")
                    bot.game.register_board("player", b)
                    bot.game.register_board("bot", b2)
                    return "`{}`".format(b.prettyprint(blind=False))
                except ValueError:
                    bot.ships = []
                    return 'One or more of your ships are placed incorrectly, unable to generate a board.\n\
                        ships reset'

        except ValueError:
            return 'Could not parse your notation, please try again.'
    elif bot.game_state == GamePhase.GAME:
        try:
            px, py = Ship.parse_shot_notation(msg['text'])
            res = bot.game.process_fire(px, py)
            bot.sender.sendMessage('Your shot was a {}'.format(res.name))

            if res == 3:
                bot.game_state = GamePhase.ENDED
                bot.sender.sendMessage("{} Wins!".format(bot.game.current_opponent())
                return

            bot.sender.sendMessage("`{}`".format(bot.game.print_board('bot', True)), parse_mode='Markdown')

            #process bot logic
            bx, by = bot_behaviour.generate_hit(bot)
            bres = bot.game.process_fire(bx, by)
            bot.results.append((bx, by, bres))
            bot.sender.sendMessage('Bot shot at {}, it was a {}'.format(to_ledgible(bx, by), bres.name))

            if res == 3:
                bot.game_state = GamePhase.ENDED
                bot.sender.sendMessage("{} Wins!".format(bot.game.current_opponent())
                return

            return "`{}`".format(bot.game.print_board('player', False))

        except ValueError:
            return ''
    elif bot.game_state == GamePhase.ENDED:
        return 'Game has already ended. Use /setup to restart at the setup phase.'
    else:
        return 'I do not understand what you want me to do'

def to_ledgible(x: int, y:int) -> str:
    a = chr(ord('A') + x)
    b = y+1
    return "{}{}".format(a, b)
