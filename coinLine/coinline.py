# coinline.py

class State:
    def __init__(self, coins, pScore=0, aiScore=0, turn='player'): 
        self.coins = coins
        self.pScore = pScore
        self.aiScore = aiScore
        self.turn = turn


"""
Returns which player (either you or AI) who has the next turn.

In the initial game state, you (i.e. 'player') gets to pick first. 
Subsequently, the players alternate with each additional move.

If there no coins left, any return value is acceptable.
"""
def player(state):
    raise NotImplementedError


"""
Returns the set of all possible actions available on the line of coins.

The actions function should return a list of all the possible actions that can be taken given a state.

Each action should be represented as a tuple (i, j) where i corresponds to the side of the line ('L', 'R')
and j corresponds to the number of coins to be picked (1, 2).

Possible moves depend on the numner of coins left.

Any return value is acceptable if there are no coins left.
"""
def actions(state):
    raise NotImplementedError

"""
Returns the line of coins that results from taking action (i, j), without modifying the 
original coins' lineup.

If `action` is not a valid action for the board, you  should raise an exception.

The returned state should be the line of coins and scores that would result from taking the 
original input state, and letting the player whose turn it is pick the coin(s) indicated by the 
input action.

Importantly, the original state should be left unmodified. This means that simply updating the 
input state itself is not a correct implementation of this function. You’ll likely want to make a 
deep copy of the state first before making any changes.
"""
def succ(state, action):
    raise NotImplementedError

"""
Returns True if game is over, False otherwise.

If the game is over when there are no coins left.

Otherwise, the function should return False if the game is still in progress.
"""
def terminal(state):
    raise NotImplementedError

"""
Returns the scores of the two players.

You may assume utility will only be called on a state if terminal(state) is True.
"""
def utility(state):
    raise NotImplementedError

"""
Returns the winner of the game, if there is one.

- If the player has won the game, the function should return 'player'.
- If your AI program has won the game, the function should return AI.
- If there is no winner of the game (either because the game is in progress, or because it ended in a tie), the
  function should return None.
"""
def winner(state):
    raise NotImplementedError
    


"""
Returns the best achivable value and the optimal action for the current player.

The move returned should be the optimal action (i, j) that is one of the allowable 
actions given a line of coins.

If multiple moves are equally optimal, any of those moves is acceptable.

If the board is a terminal board, the minimax function should return None.
"""
def minimax(state, is_maximizing):
    raise NotImplementedError


    