import sys
from Create_game import create_game
from Validate_game import validate
from Shapley import Shapley
from CostGap import tauvalue
from Core import core_exists, is_in_core, least_core, minmax_core
from Nucleolus import nucleolus, nucl_screen

GAMS_PATH=r'C:\GAMS\37\apifiles\Python'
sys.path.append(GAMS_PATH + r'\api_39')
sys.path.append(GAMS_PATH + r'\gams')
game = create_game(5)
validate(game)
core_exists(game, GAMS=True)
tau = tauvalue(game)
print(is_in_core(game,tau))
print()
nucl = nucleolus(game, GAMS=True, delta=0.3)
print(is_in_core(game,nucl))
print()
print('\n:::::::INTERESTING STUF ::::::::\n')
lcore = least_core(game)
print(lcore)
mncore = least_core(game)
print(mncore)
'''
shapley = Shapley(game)
print('Shapley:')
print(shapley)
print('\nNucleolus:')
print(nucl)
'''
