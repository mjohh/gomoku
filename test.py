
EMPTY = 0
BOARD_SIZE = 10
board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def get(board):
    bb = board
    bb[0][0] = 1
    return board


bbb = get(board)
bbb[2][2]=1
print('bbb:',bbb)
print('board:',board)

