import math

def validate(game):
    # check format of dataframe
    if list(game.columns) == ['coalition', 'value']:
        print('The passed dataframe has the correct columns\n')
    # check if indices are correct type
    if game.index.dtype == 'int64':
        print('The indices have the correct type (int)\n')
    # check if coalitions are correct type
    check = [isinstance(coal,list) for coal in game['coalition']]
    if all(item is True for item in check):
        print('The coalitions have the correct type (list)\n')
    # check if value is correct type
    check = [isinstance(coal, float) for coal in game['value']]
    if all(item is True for item in check):
        print('The coalitions have the correct type (float)\n')
    # number of players according to number of coalitions
    num = math.log2(len(game))
    # number of individual players passed in the dataframe
    ind = len(set([element for sublist in [i for i in game['coalition']] for element in sublist]))
    if num == ind:
        print('The amount of coalitions (' + str(len(game)) + ') correctly matches the number of individual players in the game (' + str(ind) + ')\n')
    # check empty and grand coalition
    for coal in game.index:
        if game['coalition'][coal] == []:
            if game['value'][coal] == 0:
                print('The value of the empty coalition is 0\n')
        if len(game['coalition'][coal]) == num:
            if game['value'][coal] == max(game['value']):
                print('The value of the grand coalition is the maximum\n')
