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
    bot.sender.sendMessage("Ready to play!")

def help(bot, msg):
    helptekst = '''/help - Read this wonderful text again.
/setup - Begin placing your ships.
/playgame - Finish placing ships and get shot at.
'''

    bot.sender.sendMessage(helptekst)

def setup(bot, msg):
    bot.game_state = GamePhase.SETUP
    bot.ships = []
    bot.sender.sendMessage(
        'Now give me 10 messages formatted like `(A1, H, 3)`.'
    )

def playgame(bot, msg):
    bot.game_state = GamePhase.GAME
    can_start = bot.game.start_game()
    if not can_start:
        bot.sender.sendMessage('Somehow the game broke')
        return
    bot.sender.sendMessage('Good, now what do you want to shoot at?')

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
                    bot.sender.sendMessage(
                        'Board accepted, start game with /playgame'
                    )
                    bot_behaviour.initialize(bot)
                    b2 = bot_behaviour.generate_board(bot)
                    bot.game = Game("player", "bot")
                    bot.game.register_board("player", b)
                    bot.game.register_board("bot", b2)
                    bot.sender.sendMessage(
                        "`{}`".format(b.prettyprint(blind=False))
                    )

                except ValueError:
                    bot.ships = []
                    bot.sender.sendMessage(
                        'One or more of your ships are placed incorrectly, '\
                        'unable to generate a board.\n' \
                        'ships reset'
                    )

        except ValueError:
            bot.sender.sendMessage(
                'Could not parse your notation, please try again.'
            )

    elif bot.game_state == GamePhase.GAME:
        try:
            px, py = Ship.parse_shot_notation(msg['text'])
            res = bot.game.process_fire(px, py)
            bot.sender.sendMessage('Your shot was a {}'.format(res.name))

            if res == 3:
                bot.game_state = GamePhase.ENDED
                bot.sender.sendMessage(
                    "{} Wins!".format(bot.game.current_opponent())
                )
                return

            bot.sender.sendMessage(
                "`{}`".format(
                    bot.game.print_board('bot', True)
                ), parse_mode='Markdown'
            )

            #process bot logic
            bx, by = bot_behaviour.generate_hit(bot)
            bres = bot.game.process_fire(bx, by)
            bot.results.append((bx, by, bres))
            bot.sender.sendMessage(
                'Bot shot at {}, it was a {}'.format(
                    to_ledgible(bx, by), bres.name
                )
            )

            if res == 3:
                bot.game_state = GamePhase.ENDED
                bot.sender.sendMessage(
                    "{} Wins!".format(bot.game.current_opponent())
                )
                return

            bot.sender.sendMessage(
                "`{}`".format(bot.game.print_board('player', False))
            )

        except ValueError:
            return

    elif bot.game_state == GamePhase.ENDED:
        bot.sender.sendMessage(
            'Game has already ended. Use /setup to restart at the setup phase.'
        )
    else:
        bot.sender.sendMessage('I do not understand what you want me to do')

def debug_ships() -> [pybattleships.ship.Ship]:
    ''' Create hardcoded board for the computer to use. '''
    s1  = Ship.parse_notation('(A1, H, 2)')
    s2  = Ship.parse_notation('(D1, V, 3)')
    s3  = Ship.parse_notation('(G1, H, 4)')
    s4  = Ship.parse_notation('(A3, V, 4)')
    s5  = Ship.parse_notation('(F3, H, 3)')
    s6  = Ship.parse_notation('(J3, V, 2)')
    s7  = Ship.parse_notation('(F6, V, 2)')
    s8  = Ship.parse_notation('(J6, V, 3)')
    s9  = Ship.parse_notation('(E10, H, 5)')
    s10 = Ship.parse_notation('(A8, H, 2)')

    return [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]

def to_ledgible(x: int, y:int) -> str:
    a = chr(ord('A') + x)
    b = y+1
    return "{}{}".format(a, b)
