import random
from itertools import combinations
import pandas as pd

def create_game(n=1, s=None):
    '''
    Function that creates a (random) n-player TU game
    :param n: number of players in the game
    :return: A fully specified game in the form of a DataFrame
    '''
    # Set seed if applicable
    if s is not None:
        random.seed(s)
    players = range(0,n)
    # Generate all coalitions for the n-player game
    coalitions = [[comb for comb in combinations(players,i)] for i in players]
    coalitions.append([comb for comb in combinations(players,n)])
    # Generate benefits for all coalitions
    k = 0
    values = {():0.0}
    game = {k: [[],0.0]}
    for level in coalitions:
        if level != [()]:
            for coal in level:
                k+=1
                incr = random.random()
                pre = max([values[Si] for Si in [tuple([x for x in coal if x != player]) for player in coal]])
                if len(coal) == 1:
                    values[coal] = 0
                    game[k] = [list(coal), 0]
                else:
                    values[coal] = pre + incr
                    game[k] = [list(coal), pre + incr]
    game = pd.DataFrame(game, index=['coalition', 'value']).transpose()
    print('\n###############')
    print('The ' + str(n) + '-player game has been created')
    print('###############\n')
    return game