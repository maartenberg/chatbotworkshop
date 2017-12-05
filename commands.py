import enum
import pybattleships
from pybattleships.ship import Ship
from pybattleships.board import Board
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
/fire - Fire at the enemy.'''
    return helptekst

def setup(bot, msg):
    bot.game_state = GamePhase.SETUP
    bot.ships = []
    return 'Now give me 10 messages formatted like `(A1, H, 3)`.'
# hoeveel schippa's van welke lengte
# wat de fuck is een horizontal todo

def catchall(bot, msg):
    if bot.game_state == GamePhase.SETUP:
        try:
            s = Ship.parse_notation(msg['text'])
            bot.ships.append(s)

            if len(bot.ships) == 10:
                try:
                    b = pybattleships.board.Board(bot.ships)
                    b2 = generate_opponent_board()
                    bot.sender.sendMessage( 'ha ik heb je bord geaccepteerd supermooi pik')
                    return "`{}`".format(b.prettyprint(blind=False))
                except ValueError:
                    bot.ships = []
                    return 'get fukt en probeer het opnieuw al dan niet in die volgorde'

        except ValueError:
            return 'fuk u'
    else:
        return 'hee dat is geen commando'

def generate_opponent_board() -> pybattleships.board.Board:
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

    ships = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]

    board = Board(ships)
    return board
