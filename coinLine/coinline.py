# coinline.py


class State:
    def __init__(self, coins, pScore=0, aiScore=0, turn="player"):
        self.coins = tuple(coins)
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
    return state.turn


"""
Returns the set of all possible actions available on the line of coins.

The actions function should return a list of all the possible actions that can be taken given a state.

Each action should be represented as a tuple (i, j) where i corresponds to the side of the line ('L', 'R')
and j corresponds to the number of coins to be picked (1, 2).

Possible moves depend on the numner of coins left.

Any return value is acceptable if there are no coins left.
"""


def actions(state):
    coins_left = len(state.coins)

    if coins_left == 0:
        return []

    possible = []

    if coins_left >= 1:
        possible.append(("L", 1))
        possible.append(("R", 1))

    if coins_left >= 2:
        possible.append(("L", 2))
        possible.append(("R", 2))

    return possible


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
    side, num = action

    if side not in ("L", "R") or num not in (1, 2):
        raise ValueError("Error: bad action format")

    coins_left = len(state.coins)

    if num > coins_left:
        raise ValueError("Cant take more coins than available")

    new_coins = list(state.coins)

    if side == "L":
        taken = new_coins[:num]
        new_coins = new_coins[num:]
    else:
        taken = new_coins[-num:]
        new_coins = new_coins[:-num]

    points = sum(taken)

    if state.turn == "player":
        new_pScore = state.pScore + points
        new_aiScore = state.aiScore
        new_turn = "ai"
    else:
        new_pScore = state.pScore
        new_aiScore = state.aiScore + points
        new_turn = "player"

    return State(
        coins=new_coins,
        pScore=new_pScore,
        aiScore=new_aiScore,
        turn=new_turn,
    )


"""
Returns True if game is over, False otherwise.

If the game is over when there are no coins left.

Otherwise, the function should return False if the game is still in progress.
"""


def terminal(state):
    return len(state.coins) == 0


"""
Returns the scores of the two players.

You may assume utility will only be called on a state if terminal(state) is True.
"""


def utility(state):
    return (state.pScore, state.aiScore)


"""
Returns the winner of the game, if there is one.

- If the player has won the game, the function should return 'player'.
- If your AI program has won the game, the function should return AI.
- If there is no winner of the game (either because the game is in progress, or because it ended in a tie), the
  function should return None.
"""


def winner(state):
    if not terminal(state):
        return None

    if state.pScore > state.aiScore:
        return "player"
    elif state.aiScore > state.pScore:
        return "ai"
    else:
        return None


"""
Returns the best achivable value and the optimal action for the current player.

The move returned should be the optimal action (i, j) that is one of the allowable 
actions given a line of coins.

If multiple moves are equally optimal, any of those moves is acceptable.

If the board is a terminal board, the minimax function should return None.
"""


def minimax(state, is_maximizing=True):
    if not hasattr(minimax, "_cache"):
        minimax._cache = {}
    cache = minimax._cache

    def solve(s, alpha, beta):
        if terminal(s):
            return (s.pScore - s.aiScore, None)

        maximizing = s.turn == "player"

        key = (s.coins, s.pScore, s.aiScore, s.turn)
        hit = cache.get(key)
        if hit is not None:
            return hit

        acts = actions(s)
        if not acts:
            res = (s.pScore - s.aiScore, None)
            cache[key] = res
            return res

        if maximizing:
            best_val = -float("inf")
            best_action = None
            for a in acts:
                val, _ = solve(succ(s, a), alpha, beta)
                if val > best_val:
                    best_val, best_action = val, a
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break
            res = (best_val, best_action)
        else:
            best_val = float("inf")
            best_action = None
            for a in acts:
                val, _ = solve(succ(s, a), alpha, beta)
                if val < best_val:
                    best_val, best_action = val, a
                beta = min(beta, best_val)
                if beta <= alpha:
                    break
            res = (best_val, best_action)

        cache[key] = res
        return res

    return solve(state, -float("inf"), float("inf"))

