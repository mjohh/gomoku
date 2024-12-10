# -*- coding: utf-8 -*-
import numpy as np
import time
FIVE = 0
LIVE_FOUR = 1
SLEEP_FOUR = 2
LIVE_THREE = 3
SLEEP_THREE = 4
LIVE_TWO = 5
SLEEP_TWO = 6

PLAYER = 1
OPPONENT = -1
EMPTY = 0
BOARD_SIZE = 15 

shapes = ['five','live_four','sleep_four','live_three','sleep_three','live_two','sleep_two']
shape_scores = {'five':100000,'live_four':10000,'sleep_four':1000,'live_three':1000,'sleep_three':100,'live_two':100,'sleep_two':10}


def save_shape_cnts(cnt_dict, cnt, start_blocken, end_blocken):
    if cnt==5:
        cnt_dict['five'] += 1
    if start_blocken and end_blocken:
        return
    elif start_blocken or end_blocken:
        if cnt==2:
            cnt_dict['sleep_two'] += 1
        elif cnt==3:
            cnt_dict['sleep_three'] += 1
        elif cnt==4:
            cnt_dict['sleep_four'] += 1
    else:
        if cnt==2:
            cnt_dict['live_two'] += 1
        elif cnt==3:
            cnt_dict['live_three'] += 1
        elif cnt==4:
            cnt_dict['live_four'] += 1

'''
def match_shapes_in_line(line):
    l = len(line)
    i = 0
    player_cnts = {shape:0 for shape in shapes}
    opponent_cnts = {shape:0 for shape in shapes}

    while i<l:
        # 
        cnt = 1 
        player = 0
        start = i
        start_blocken = False
        end_blocken = False

        while i+1<l and line[i]==line[i+1] and cnt<5:
            player = line[i]
            cnt += 1
            i += 1
        #at least 2 in line
        if cnt>1:
            if player!=0:
                # check ends
                end=start+cnt-1
                if start-1<0 or line[start-1]==-player:
                    start_blocken = True
                if end+1>l-1 or line[end+1]==-player:
                    end_blocken = True

                # save cnt for shape of player
                if player==PLAYER:
                    save_shape_cnts(player_cnts, cnt, start_blocken, end_blocken)    
                else:
                    save_shape_cnts(opponent_cnts, cnt, start_blocken, end_blocken)
        else:
            i += 1
    return player_cnts, opponent_cnts
'''
def match_shapes_in_line(line):
    l = len(line)
    i = 0
    player_cnts = {shape:0 for shape in shapes}
    opponent_cnts = {shape:0 for shape in shapes}

    while i<l:
        # 
        cnt = 1 
        player = 0
        start = i
        start_blocken = False
        end_blocken = False

        #while i+1<l and line[i]==line[i+1] and cnt<5:
        #    player = line[i]
        #    cnt += 1 
        #    i += 1
        while True:
            if i+1<l and line[i]!=0 and line[i]==line[i+1] and cnt<5:
                player = line[i]
                cnt += 1
                i += 1
                end = i
            #skipping
            elif i+2<l and line[i]!=0 and line[i+1]==0 and line[i]==line[i+2] and cnt<4:
                player = line[i]
                cnt += 1 
                i += 2
                end = i
            else:
                i += 1
                break
            
        #at least 2 in line
        if cnt>1:
            if player!=0:
                # check ends
                #end=start+cnt-1
                if start-1<0 or line[start-1]==-player:
                    start_blocken = True
                if end+1>l-1 or line[end+1]==-player:
                    end_blocken = True

                # save cnt for shape of player
                if player==PLAYER:
                    save_shape_cnts(player_cnts, cnt, start_blocken, end_blocken)    
                else:
                    save_shape_cnts(opponent_cnts, cnt, start_blocken, end_blocken)

    return player_cnts, opponent_cnts

def count_scores_in_line(line):
    player_score=0
    opponent_score=0
    a,b = match_shapes_in_line(line)

    for k in a.keys():
        player_score += a[k]*shape_scores[k]
    for k in b.keys():
        opponent_score += b[k]*shape_scores[k]
    return player_score-opponent_score

# 扫描所有方向上的棋线（横向、纵向、对角线）
def evaluate_board(board):
    """
    扫描棋盘上的所有线段（横向、纵向、对角线）。
    :param board: 当前棋盘状态
    :return: 返回总score
    """
    score = 0
    t1 = time.time()
    # 1. 横向扫描（逐行扫描每一列）
    for i in range(BOARD_SIZE):
        line = [board[i][j] for j in range(BOARD_SIZE)]
        if len(line)>=5:
            all_zero = all(v==0 for v in line)
            if not all_zero:
                score += count_scores_in_line(line)

    # 2. 纵向扫描（逐列扫描每一行）
    for j in range(BOARD_SIZE):
        line = [board[i][j] for i in range(BOARD_SIZE)]
        if len(line)>=5:
            all_zero = all(v==0 for v in line)
            if not all_zero:
                score += count_scores_in_line(line)

    # 3. 右下对角线扫描
    for start in range(BOARD_SIZE):  # 从左上到右下的每条对角线
        line = []
        x, y = start, 0
        all_zero = True
        while x < BOARD_SIZE and y < BOARD_SIZE:
            line.append(board[x][y])
            if board[x][y]!=EMPTY:
                all_zero = False 
            x += 1
            y += 1
        if len(line)>=5 and not all_zero:
            score += count_scores_in_line(line)

    for start in range(1, BOARD_SIZE):  # 从左下到右上的每条对角线
        line = []
        x, y = 0, start
        all_zero = True
        while x < BOARD_SIZE and y < BOARD_SIZE:
            line.append(board[x][y])
            if board[x][y]!=EMPTY:
                all_zero = False 
            x += 1
            y += 1
        if len(line)>=5 and not all_zero:
            score += count_scores_in_line(line)

    # 4. 左下对角线扫描
    for start in range(BOARD_SIZE):  # 从右上到左下的每条对角线
        line = []
        all_zero = True
        x, y = start, BOARD_SIZE - 1
        while x < BOARD_SIZE and y >= 0:
            line.append(board[x][y])
            if board[x][y]!=EMPTY:
                all_zero = False 
            x += 1
            y -= 1
        if len(line)>=5 and not all_zero:
            score += count_scores_in_line(line)

    for start in range(1, BOARD_SIZE):  # 从右下到左上的每条对角线
        line = []
        x, y = 0, BOARD_SIZE - 1 - start
        all_zero = True
        while x < BOARD_SIZE and y >= 0:
            line.append(board[x][y])
            if board[x][y]!=EMPTY:
                all_zero = False 
            x += 1
            y -= 1
        if len(line)>=5 and not all_zero:
            score += count_scores_in_line(line)
    t2 = time.time()
    #print('evaluate cost t={}ms'.format(t2-t1))
    return score


# 初始化棋盘
def init_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# 打印棋盘
def print_board(board):
    print("\n" + "  ".join([str(i).rjust(2) for i in range(BOARD_SIZE)]))  # 打印列号
    for r in range(BOARD_SIZE):
        row = [str(board[r][c]) for c in range(BOARD_SIZE)]
        print("{:2}".format(r) + "  ".join(row))  # 打印行号

# 判断是否胜利
def check_winner(board, player):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == player:
                if check_line(board, r, c, 1, 0, player) or check_line(board, r, c, 0, 1, player) or \
                   check_line(board, r, c, 1, 1, player) or check_line(board, r, c, 1, -1, player):
                    return True
    return False

def check_line(board, r, c, dr, dc, player):
    for i in range(5):
        nr, nc = r + dr * i, c + dc * i
        if not (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE) or board[nr][nc] != player:
            return False
    return True

# Minimax算法
eval_cnt=0
def minimax(board, depth, maximizing_player):
    if depth == 0 or check_winner(board, PLAYER) or check_winner(board, OPPONENT):
        global eval_cnt
        eval_cnt += 1
        #print('eval_cnt={}'.format(eval_cnt))
        return evaluate_board(board)

    if maximizing_player:  # AI玩家
        max_eval = -float('inf')
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == EMPTY:  # 空位
                    board[r][c] = PLAYER
                    eval = minimax(board, depth-1, False)
                    max_eval = max(max_eval, eval)
                    board[r][c] = EMPTY
        return max_eval
    else:  # 玩家1
        min_eval = float('inf')
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == EMPTY:  # 空位
                    board[r][c] = OPPONENT 
                    eval = minimax(board, depth-1, True)
                    min_eval = min(min_eval, eval)
                    board[r][c] = EMPTY
        return min_eval

# 找到AI的最佳落子
def find_best_move(board):
    best_move = None
    best_value = -float('inf')
    t1 = time.time()
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == EMPTY:  # 空位
                board[r][c] = PLAYER
                move_value = minimax(board, 1, False)  # 深度设置为3
                if move_value > best_value:
                    best_value = move_value
                    best_move = (r, c)
                board[r][c] = EMPTY
    t2 = time.time()
    print('one move cost:{}ms'.format(t2-t1))
    return best_move

# 玩家1（你）输入落子位置
def player_move(board):
    while True:
        try:
            #python2.0
            #move = raw_input("请输入你的落子位置（格式：行 列）：")
            #python3.0
            move = input("请输入你的落子位置（格式：行 列）：")
            r, c = map(int, move.split())
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == EMPTY:
                return r, c
            else:
                print("无效的落子位置，请重新输入！")
        except ValueError:
            print("输入无效，请按格式输入：行 列")

# 游戏主函数
def play_game():
    board = init_board()
    print_board(board)

    while True:
        # 玩家1（你）的回合
        print("\n你的回合（X）:")
        r, c = player_move(board)
        board[r][c] = OPPONENT 
        print_board(board)

        if check_winner(board, OPPONENT):
            print("\n恭喜你！你赢了！")
            break

        # AI玩家（玩家2）的回合
        print("\nAI的回合（O）:")
        ai_move = find_best_move(board)
        r, c = ai_move
        board[r][c] = PLAYER
        print_board(board)

        if check_winner(board, PLAYER):
            print("\nAI赢了！")
            break

if __name__ == "__main__":
    play_game()
#################################################################
'''
#all empty
l = [0,0,0,0,0,0,0,0]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
#only one
l = [1,0,0,0,0,0,0,0]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==0
#only one
l = [0,0,0,0,0,0,0,1]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==0
#muti ones
l = [0,0,1,0,1,0,0,1]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==100
#one sleep two
l = [1,1,0,0,0,0,0,0]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==10
#one sleep two
l = [0,0,0,0,0,0,1,1]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==10
#muti sleep two
l = [1,1,0,-1,1,1,0,1]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==10
#sleep two+live two
l = [0,0,1,1,0,0,1,1]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==110
#two live two
l = [0,1,1,0,0,1,1,0]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==200
#sleep two + oppo sleep two
l = [1,1,0,0,0,0,-1,-1]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==0
#sleep two + oppo sleep two
l = [-1,-1,0,0,0,0,1,1]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==0
#oppo five + sleep two
l = [-1,-1,-1,-1,-1,0,1,1]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==(-100000+10)
#one sleep two
l = [0,-1,1,1,0,0,0,0]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==10
#none
l = [0,-1,1,1,-1,0,0,0]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==0
#one oppo sleep two
l = [0,-1,1,1,-1,-1,0,0]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==-10
#one live four
l = [0,1,1,1,1,0,0,0]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==10000
#one live three
l = [0,1,1,0,1,0,0,0]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==1000
#one sleep four
l = [1,1,1,0,1,0,0,0]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==1000
#one sleep three 
l = [0,0,0,0,1,0,1,1]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==100
#one live three 
l = [0,0,0,0,1,0,1,0]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==100
#one live three 
l = [0,1,0,1,1,0,1,0]
a,b=match_shapes_in_line(l)
print(l)
print(a)
print(b)
s=count_scores_in_line(l)
print(s)
assert s==10000

####
# 初始化一个棋盘
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

# 设置一些棋子，假设玩家1为1，玩家2为-1
board[7][7] = 1  # 玩家1的棋子
board[7][8] = -1  # 玩家2的棋子
board[7][9] = 1  # 玩家1的棋子
board[8][7] = 1  # 玩家1的棋子
board[9][7] = 1  # 玩家1的棋子

# 扫描所有方向上的棋线
score = evaluate_board(board)
print(score)
assert score==1100

####
# 初始化一个棋盘
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

# 设置一些棋子，假设玩家1为1，玩家2为-1
board[7][7] = 1  # 玩家1的棋子
board[7][8] = -1  # 玩家2的棋子
board[7][9] = 1  # 玩家1的棋子
board[7][10] = 1  # 玩家1的棋子
board[8][7] = 1  # 玩家1的棋子
board[9][7] = 1  # 玩家1的棋子

# 扫描所有方向上的棋线
score = evaluate_board(board)
print(score)
assert score==1110

####
# 初始化一个棋盘
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

# 设置一些棋子，假设玩家1为1，玩家2为-1

board[5][5] = 1  # 玩家1的棋子
board[6][6] = 1  # 玩家1的棋子
board[6][7] = 1  # 玩家1的棋子
board[7][7] = 1  # 玩家1的棋子
board[7][8] = -1  # 玩家2的棋子
board[8][8] = -1  # 玩家2的棋子
board[9][9] = -1  # 玩家2的棋子
board[7][9] = 1  # 玩家1的棋子
board[7][10] = 1  # 玩家1的棋子
board[8][7] = 1  # 玩家1的棋子
board[9][7] = 1  # 玩家1的棋子

# 扫描所有方向上的棋线
score = evaluate_board(board)
#print(board)
print(score)
assert score==10100
'''
