import math

def dif_gain(name, n, game):
    # returns the difference between the gains of n players coalitions including
    # the player "name" and those of n-1 players coalitions not containing this player

    # Initialization
    sum_in = 0
    # Sum of the gains of n players coalitions including the player "name"
    sum_ex = 0
    # Sum of the gains of n-1 players coalitions not containing this player

    # Checks the size of the strings that correspond to the number of players
    # in the coalition and whether the name of the player is included or not
    for ind in game.index:
        if len(game['coalition'][ind]) == n - 1 and not name in game['coalition'][ind]:
            sum_ex += game['value'][ind]
        elif len(game['coalition'][ind]) == n and name in game['coalition'][ind]:
            sum_in += game['value'][ind]
    dif = sum_in - sum_ex
    return (dif)

def Shapley(game):
    # Return the Shapley value of the problem
    # Number of players
    players = set([element for sublist in [i for i in game['coalition']] for element in sublist])
    Shapley={player: 0 for player in players}
    for player in Shapley:
        n = len(Shapley)
        for j in range (1,n+1):
            Shapley[player]+=math.factorial(n-j)*math.factorial(j-1)*dif_gain(player,j,game)/math.factorial(n)

    print('Shapley value properly calculated\n')
    return (Shapley)

