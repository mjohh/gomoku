def in_board(i,j):
    return i>-1 and i<BOARD_SIZE and j>-1 and j<BOARD_SIZE

def match_shapes_in_line_v2(board, x0, y0, dr, dc):
    l = BOARD_SIZE
    i=x0
    j=y0
    player_cnts = {shape:0 for shape in shapes}
    opponent_cnts = {shape:0 for shape in shapes}

    while in_board(i, j):
        cnt = 1
        player=EMPTY
        starti = i
        startj = j
        start_blocken = False
        end_blocken = False

        while True:
            if in_board(i+dr,j+dc) and board[i][j]!=EMPTY and board[i][j]==board[i+dc][j+dr] and cnt<5:
                player = board[i][j]
                cnt += 1
                i += dr
                j += dc
                endi = i
                endj = j
            #skipping
            elif in_board(i+2*dr, j+2*dc) and board[i][j]!=EMPTY and board[i+dr][j+dc]==EMPTY and board[i][j]==board[i+2*dr][j+2*dc] and cnt<4:
                player = board[i][j]
                cnt += 1
                i += 2*dr
                j += 2*dc
                endi = i
                endj = j
            else:
                i += dr
                j += dc 
                break

        #at least 2 in line
        if cnt>1:
            #check ends
            if (not in_board(starti-dr,startj-dc)) or board[starti-dr][startj-dc]==-player:
                start_blocken=True
            if (not in_board(endi+dr,endj+dc)) or board[endi+dr][endj+dc]==-player:
                end_blocken=True 
      
            # save cnt for shape of player
            if player==PLAYER:
                save_shape_cnts(player_cnts, cnt, start_blocken, end_blocken)
            else:
                save_shape_cnts(opponent_cnts, cnt, start_blocken, end_blocken)
    return player_cnts, opponent_cnts


import time
import numpy as np

BOARD_SIZE = 18  # 假设棋盘大小为8x8
EMPTY = 0  # 假设EMPTY为0

# 列表的遍历
a=[[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
b=np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

t1 = time.time()
for i in range(10000):
    for j in range(BOARD_SIZE):
        v = a[j][j]
t2 = time.time()
print('cost1=',t2-t1)
#####
t1 = time.time()
for i in range(10000):
    for j in range(BOARD_SIZE):
        v = b[j][j]
t2 = time.time()
print('cost2=',t2-t1)
#####
t1 = time.time()
a=[]
for i in range(10000):
    a.append(i)
print(len(a))
t2 = time.time()
print('cost3=',t2-t1)
#####
t1 = time.time()
a=[None]*19000
for i in range(10000):
    a[i]=i
print(len(a))
t2 = time.time()
print('cost4=',t2-t1)
