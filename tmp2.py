import numpy as np


# 初始化井字棋棋盘，0表示空位，1表示玩家1（智能体），-1表示玩家2（人）
board_size = 3
board = np.zeros((board_size, board_size), dtype=int)


def get_state_number(board):
    state_num = 0
    multiplier = 1
    for row in board.flatten():
        state_num += (row + 1) * multiplier
        multiplier *= 3
        #print("当前状态编号计算:", state_num)
    return state_num


board[0][0]=1
num = get_state_number(board)
print(num)
board[0][1]=1
num = get_state_number(board)
print(num)
board[1][1]=-1
num = get_state_number(board)
print(num)


