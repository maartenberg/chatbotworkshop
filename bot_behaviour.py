import random
import enum
import pybattleships
from pybattleships.ship import Ship
from pybattleships.board import Board
from pybattleships.game import Game
import pybattleships.game

def initialize(bot):
    '''
    This function will be called before any others,
    use this to define a starting state or taunt the player
    by typing:
    bot.sender.sendMessage("*YOUR AWESOME TAUNT*")
    somewhere before return
    '''
    # Make a list that keeps track of the squares we have already shot at
    bot.fired_at_list = []
    # Make a list to keep track of shot results, form of (x, y, ShotResult)
    bot.results = []
    return

def generate_hit(bot) -> (int, int):
    '''
    This function will be called any time your bot has to decide what to do.
    Remeber that a tuple of (x, y) values are expected and both x and y have
    to be an integer in the range 0-9
    '''
    x = random.randrange(10)
    y = random.randrange(10)

    #If we have fired at this sport before, just try again
    if (x, y) in bot.fired_at_list:
        return generate_hit(bot)
    else:
    #If we haven't fired at it before add it to the list and fire at it
        bot.fired_at_list.append((x, y))
        return (x, y)

def generate_board(bot) -> pybattleships.board.Board:
    '''
    This function will be called when it's the bot's turn to set up a board.
    You can keep it as is but that would be pretty boring to play against,
    so it's best to come up with a way to generate a board automatically.
    '''
    s1  = Ship.parse_notation('(A1, H, 2)')
    # You can also use another (easier) way to make a ship
    s2  = Ship(3, 0, False, 3)
    # this is the same ship as
    # Ship.parse_notation('(D1, V, 3)') would have made.
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


