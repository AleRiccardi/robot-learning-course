import numpy as np


def move_still_possible(S):
    return not (S[S==0].size == 0)


def move_at_random(S):
    xs, ys = np.where(S==0)

    i = np.random.permutation(np.arange(xs.size))[0]
    
    S[xs[i],ys[i]] = -1

    return S

def move_by_selection(S):
    xs, ys = np.where(S==0)
    valid = False
    while(not valid):
        print("Make a move: ", end="")
        i = int(input()) - 1
        x = i % 3
        y = i // 3

        if S[y, x] == 0:
            S[y, x] = 1
            valid = True
        else:
            print("Invalid move")

    return S, i
    

def move_was_winning_move(S, p):
    if np.max((np.sum(S, axis=0)) * p) == 3:
        return True

    if np.max((np.sum(S, axis=1)) * p) == 3:
        return True

    if (np.sum(np.diag(S)) * p) == 3:
        return True

    if (np.sum(np.diag(np.rot90(S))) * p) == 3:
        return True

    return False


# python dictionary to map integers (1, -1, 0) to characters ('x', 'o', ' ')
symbols = { 1:'x',
           -1:'o',
            0:' '}


# print game state matrix using characters
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print (B)


def updateVs(player, lastMove, vs):
    # Tracker length
    n_0 = len(tracker) - 1

    # Temporal V(s) for terminal state
    terminalVs = np.ones() * 0.1

    # Traverse tracker in reverse order
    for x in range(n_0, -1, -1):
        # Update terminal state V(s)
        if (x == n_0):
            vs[tracker[x]][lastMove] = 1 if player == 1 else 0
        
        # Update previous states V(s)
        vs[tracker[x]] = vs[tracker[x]] + 0.2 * (vs[tracker[x+1]] - vs[tracker[x]])


if __name__ == '__main__':
    # initialize an empty tic tac toe board
    gameState = np.zeros((3,3), dtype=int)

    # Last player before terminal state
    lastMove = None

    # initialize the player who moves first (either +1 or -1)
    player = 1

    # initialize a move counter
    mvcntr = 1

    # initialize a flag that indicates whetehr or not game has ended
    noWinnerYet = True

    # V(s) hash-table
    vs = dict()

    # State tracker
    tracker = []

    # Initialize vs with state0 V(s)
    vs[gameState] = np.ones(9) * 0.1
    tracker.append(gameState)
    
    while move_still_possible(gameState) and noWinnerYet:
        # turn current player number into player symbol
        name = symbols[player]
        print ('%s moves' % name)

        # let current player move at random
        if player == 1:
            gameState, lastMove = move_by_selection(S)
        else:
            gameState = move_at_random(S)

        # Add successor state to V(s)
        vs[gameState] = np.ones(9) * 0.1
        tracker.append(gameState)

        # print current game state
        print_game_state(gameState)
        
        # evaluate current game state
        if move_was_winning_move(gameState, player):
            print ('player %s wins after %d moves' % (name, mvcntr))
            noWinnerYet = False

        # switch current player and increase move counter
        player *= -1
        mvcntr +=  1
    
    # Update Vs
    updateVs(player, lastMove, vs)

    if noWinnerYet:
        print ('game ended in a draw' )
