# ============================================================
# 3 Jugs problem (or n jugs) definition
# Authors: S. El Alaoui and ChatGPT 5
# ============================================================


class SearchProblem:
    def start_state(self):
        raise NotImplementedError()

    def actions(self, state):
        raise NotImplementedError()

    def cost(self, state, action):
        raise NotImplementedError()

    def succ(self, state, action):
        raise NotImplementedError()

    def is_end(self, state):
        raise NotImplementedError()


# Action = of type Tuple[str, int, Optional[int]]  # ('fill', i, None) | ('empty', i, None) | ('pour', i, j)
# State = of type Tuple[int, ...]


class NJugsProblem(SearchProblem):
    """
    N-jugs problem with the standard operations:
      - fill(i): fill jug i to its capacity from an infinite source
      - empty(i): empty jug i to drain
      - pour(i, j): pour from jug i into jug j until i is empty or j is full

    State is an N-tuple of amounts (non-negative ints).
    Cost per action defaults to 1 (can be changed with cost_per_move).
    """

    def __init__(self, capacities, goal):
        caps = tuple(int(c) for c in capacities)
        if any(c <= 0 for c in caps):
            raise ValueError("All capacities must be positive integers.")

        if not goal:
            raise ValueError("Goal must be provided.")

        goal = tuple(int(x) for x in goal)
        if len(goal) != len(capacities):
            raise ValueError(
                "Goal length must match number of capacities (", len(capacities), ")."
            )

        self.capacities = caps
        self.n = len(caps)
        self._goal = tuple(goal)

    # ---- SearchProblem API ----
    def start_state(self):
        return tuple(0 for _ in range(self.n))

    def is_end(self, state):
        return state == self._goal

    def cost(self, state, action) -> int:
        # Unit cost per move by default 1.
        return 1

    """
    Returns the set of all possible actions available on the current state of the jugs.

    The actions function should return a list of all the possible actions that can be taken given a state.

    Each action should be represented as a tuple (action_kind, i, j) 
    action_kind is one of: "fill", "empty" and "pour"
    i corresponds to the jug affected by the action
    j is a valid number only if the action is "pour" (i.e. pour from jug i into jug j). Otherwise it should be set to None
    """

    def actions(self, state):
        if len(state) != self.n:
            raise ValueError("Lenght of 'state' doesn't match length of capacities")
        actions = []
        index = 0
        for jug in state:
            if state[jug] < self.capacities[jug] and state[index] > 0 and index != jug:
                actions.append(("pour", index, jug))
                if index < self.n:
                    index += 1
                else:
                    index = 0
            if state[jug] < self.capacities[jug]:
                actions.append(("fill", jug))
            if state[jug] > 0:
                actions.append(("empty", jug))
        return tuple(actions)

    """
    Returns the state of the jugs after taking action (kind, i, j), without modifying the original state.

    If `action` is not a valid action for the current state, you  should raise an exception.

    The returned state should be: tuple([j1, j2, j3]) 
    where j1, j2 and j3 represent the amount of water in each jug, respectively. 

    Importantly, the original state should be left unmodified. This 
    means that simply updating the input state itself is not a correct 
    implementation of this function. You’ll likely want to make a 
    copy of the state first before making any changes.
    """

    def succ(self, state, action):
        if len(state) != self.n:
            raise ValueError("Lenght of 'state' doesn't match legnth of 'capacities")
        if action[0] == "fill":
            jug = action[1]
            state = list(state)
            state[jug] = self.capacities[jug]
            return tuple(state)
        elif action[0] == "empty":
            jug = action[1]
            state = list(state)
            state[jug] = 0
            return tuple(state)
        elif action[0] == "pour":
            sourceJug = action[1]
            targetJug = action[2]
            state = list(state)
            while (
                state[sourceJug] > 0 and state[targetJug] < self.capacities[targetJug]
            ):
                state[sourceJug] = state[sourceJug] - 1
                state[targetJug] = state[targetJug] + 1
            return tuple(state)
        else:
            raise ValueError(f"unknown action: {action}")

    # ---- Helpers ----

    @property
    def goal(self):
        return self._goal

    @property
    def capacities_tuple(self):
        return self.capacities
