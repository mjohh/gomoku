## -*- coding: utf-8 -*-
import numpy as np
import time
import copy
import random

# import mcts tree
from mcts import TreeNode
from mcts import C
from mcts import print_node
from mcts import uct_val
#from mcts import select 
#from mcts import expand
#from mcts import simulate
#from mcts import backpropagate
#from mcts import monte_carlo_search
from mcts import print_mcts_tree
 
TIMES = 1000 


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
BOARD_SIZE = 8 

WIN = 1
DRAW = 0
GOON = -1

#node_cnt=0
#sim_cnt=0

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

def in_board(i,j):
    return i>-1 and i<BOARD_SIZE and j>-1 and j<BOARD_SIZE


def is_empty_line(board, x0, y0, dr, dc):
    noempty = False
    i = x0
    j = y0
    while(in_board(i,j)):
        if(board[i][j]!=EMPTY):
            return False 
        i+=dr
        j+=dc
    return True
    
def is_short_line(board, x0, y0, dr, dc):
    return not in_board(x0+4*dr, y0+4*dc)    

def illegal_line(board, x0, y0, dr, dc):
    i = x0
    j = y0
    # too short
    if not in_board(x0+4*dr, y0+4*dc):
        return True    
    # not empty
    while(in_board(i,j)):
        if(board[i][j]!=EMPTY):
            return False 
        i+=dr
        j+=dc
    # empty
    return True
    
def count_scores_in_line(line):
    player_score=0
    opponent_score=0
    a,b = match_shapes_in_line(line)

    for k in a.keys():
        player_score += a[k]*shape_scores[k]
    for k in b.keys():
        opponent_score += b[k]*shape_scores[k]
    return player_score-opponent_score

# for opponent live_trhee, blocking it has hihger priority
# than form self's live_three 
def count_scores_in_line_v2(line, player):
    player_score=0
    opponent_score=0
    a,b = match_shapes_in_line(line)

    if player==PLAYER:
        for k in a.keys():
            player_score += a[k]*shape_scores[k]
        for k in b.keys():
            if k=='live_three':#danger!, kill it rightly
                opponent_score += b[k]*shape_scores[k]*10
            else:
                opponent_score += b[k]*shape_scores[k]
    else: #OPPONENT:
        for k in a.keys():
            if k=='live_three':#danger!, kill it rightly
                player_score += a[k]*shape_scores[k]*10
            else: 
                player_score += a[k]*shape_scores[k]
        for k in b.keys():
            opponent_score += b[k]*shape_scores[k]
    return player_score - opponent_score

# 扫描所有方向上的棋线（横向、纵向、对角线）
def evaluate_board(board, player):
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
        if len(line)>=5 and any(v != 0 for v in line):
            score += count_scores_in_line_v2(line, player)

    # 2. 纵向扫描（逐列扫描每一行）
    for j in range(BOARD_SIZE):
        line = [board[i][j] for i in range(BOARD_SIZE)]
        if len(line)>=5 and any(v != 0 for v in line):
            score += count_scores_in_line_v2(line, player)

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
            score += count_scores_in_line_v2(line, player)

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
            score += count_scores_in_line_v2(line, player)

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
            score += count_scores_in_line_v2(line, player)

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
            score += count_scores_in_line_v2(line, player)
    t2 = time.time()
    #print('v1 evaluate cost t={}ms'.format(t2-t1))
    return score


# 初始化棋盘
def init_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    #board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    #return board

# 打印棋盘
def print_board(board):
    show_board=[['-' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c]==-1:
                show_board[r][c]='0'
            elif board[r][c]==1:
                show_board[r][c]='1'
    print("\n " + " ".join([str(i).rjust(2) for i in range(BOARD_SIZE)]))  # 打印列号
    for r in range(BOARD_SIZE):
        #row = [str(board[r][c]) for c in range(BOARD_SIZE)]
        row=show_board[r]
        print("{:2}".format(r) + "  ".join(row))  # 打印行号
    #print(board)

# 判断是否胜利
def check_winner(board, player):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == player:
                if check_line(board, r, c, 1, 0, player) or check_line(board, r, c, 0, 1, player) or \
                   check_line(board, r, c, 1, 1, player) or check_line(board, r, c, 1, -1, player):
                    return WIN 

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == EMPTY:
                return GOON
    return DRAW


def check_line(board, r, c, dr, dc, player):
    for i in range(5):
        nr, nc = r + dr * i, c + dc * i
        if not (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE) or board[nr][nc] != player:
            return False
    return True

# 三步以内无子，剪枝
def is_isolated(board, x, y, steps):
    for step in range(1,steps+1):
        if in_board(x,y-step) and board[x][y-step]!=EMPTY:
            return False
        if in_board(x-step,y-step) and board[x-step][y-step]!=EMPTY:
            return False
        if in_board(x-step,y) and board[x-step][y]!=EMPTY:
            return False
        if in_board(x-step,y+step) and board[x-step][y+step]!=EMPTY:
            return False
        if in_board(x,y+step) and board[x][y+step]!=EMPTY:
            return False
        if in_board(x+step,y+step) and board[x+step][y+step]!=EMPTY:
            return False
        if in_board(x+step,y) and board[x+step][y]!=EMPTY:
            return False
        if in_board(x+step,y-step) and board[x+step][y-step ]!=EMPTY:
            return False
    return True

def empty_board(state):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
           if state[r][c]!=EMPTY:
                return False
    return True

#def get_possible_moves(node):
def get_possible_moves(state):
    if empty_board(state):
    # first step, just place on the center
        return [(BOARD_SIZE//2,BOARD_SIZE//2)]
    board = state
    moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # have neibor chess within 3 steps
            if board[row][col]==0 and not is_isolated(board, row, col, 2):
                moves.append((row, col))
    return moves

def make_move(state, move, player):
    #new_state = [row.copy() for row in state]
    #if deepcopy:
    #    new_state = [copy.deepcopy(row) for row in state]
    #else:
        #new_state = state
    #    new_state = [copy.deepcopy(row) for row in state]
    row, col = move
    state[row][col] = player
    #return state


# attention:no consider draw temply
def is_game_over(state, player):
    r = check_winner(state, player)
    if r==WIN:
        return True, player
    elif r==DRAW:
        return True, None
    return False, None

def choose_move_by_score(state, player):
    possible_moves = get_possible_moves(state)
    if len(possible_moves)<=0:
        return None
    mv = None
    if player==PLAYER:
        maxscore = float('-inf') 
        for move in possible_moves:
            make_move(state, move, player)
            score = evaluate_board(state, player)
            if maxscore < score:
                maxscore = score
                mv = move
            make_move(state, move, EMPTY)
        return mv
    else:#opponent
        minscore = float('inf')
        for move in possible_moves:
            make_move(state, move, player)
            score = evaluate_board(state, player)
            if minscore > score:
                minscore = score
                mv = move
            make_move(state, move, EMPTY)
        return mv

def choose_high_score_child(children):
    sel=None
    player = children[0].player
    if player==PLAYER:
        maxscore = float('-inf')
        for child in children:
            score = evaluate_board(child.state, player)
            if maxscore < score:
                maxscore = score
                sel = child
        return sel
    else:#opponent
        minscore = float('inf')
        for child in children:
            score = evaluate_board(child.state, player)
            if minscore > score:
                minscore = score
                sel = child
        return sel

'''
def select(node):
    while node.children:
        # node never visited will be selected for it's uct val 'inf'
        #for node in node.children:
        #    print_node(node)
        node = max(node.children, key=uct_val)
        #print('----select----')
        #for node in node.children:
        #    print_node(node)
        #print('selected:')
        #print_node(node)
    return node
'''
def select(node):
    while node.children:
        # node never visited will be selected for it's uct val 'inf'
        node = max(node.children, key=uct_val)
    return node

def expand(node):
    global node_cnt
    possible_moves = get_possible_moves(node.state)
    for move in possible_moves:
        new_state = [copy.deepcopy(row) for row in node.state]
        make_move(new_state, move, -node.player)
        child = TreeNode(new_state, -node.player, parent=node)
        child.move=move #record the move, we could return it rightly if choosed 
        node.children.append(child)
    return node.children

'''
def simulate(state):
    while True:
        game_over,winner = is_game_over(state)
        if game_over:
            return winner
        possible_moves = get_possible_moves(state)
        move = random.choice(possible_moves) 
        state = make_move(state, move
'''

def simulate(node):
    player = node.player
    state = node.state
    cnt = 0
    while True:
        cnt += 1
        t1 = time.time()
        game_over,winner = is_game_over(state, player)
        if game_over:
            print('---------game over!----------')
            if winner==PLAYER:
                print_board(state)
            return winner
        #possible_moves = get_possible_moves(state)
        # TODO:my could add evalution, not randomly
        # evalution only in simsulation?
        #print('possible_moves len:',len(possible_moves))
        #move = random.choice(possible_moves)
        player = -player
        move = choose_move_by_score(state, player)
        make_move(state, move, player)
        print_board(state)
        #print('move:',move)
        t2 = time.time()
        #print('cnt=',cnt,',one move=',t2-t1)
    
def backpropagate(node, result):
    while node:
        node.visits += 1
        if result==PLAYER:
            node.wins += 1
        # learn draw, better than loss
        #elif result== None:
        #    node.wins += 0.5
        node = node.parent
 

def monte_carlo_search(board, player):
    #game begin,asume no.0 step is -1, then the no.1 step will be 1
    sim_cnt = 0
    node_cnt = 0
    selected_couldnot_expand_cnt = 0
    player_win_cnt = 0
    opponent_win_cnt = 0
    draw_cnt = 0
    select_cnt = 0
    root = TreeNode(board, -player)
    for _ in range(TIMES):
        t1 = time.time()
        selected = select(root)
        select_cnt += 1
        #print_node(selected)
        children = expand(selected)
        node_cnt += len(children)
        if len(children)==0:
            selected_couldnot_expand_cnt += 1
        if children:
            #simulated_state = random.choice(children).state
            #result = simulate(simulated_state)
            # TODO:here may could add evalution besides simulate
            #child = random.choice(children)
            child = choose_high_score_child(children)
            ts1 = time.time()
            result = simulate(child)
            sim_cnt += 1
            ts2 = time.time()
            #print('one sim cost:', ts2-ts1)
            #backpropagate(selected, resul)
            backpropagate(child, result)#backpropagate from the bottom node
            if result==PLAYER:
                player_win_cnt += 1
            elif result==OPPONENT:
                opponent_win_cnt += 1
            elif result==None:
                draw_cnt += 1
            else:
                print('impossible!!!!')
        t2 = time.time()
        #print('one mcts search time cost:',t2-t1)
    print_mcts_tree(root,depth=2)
    best_child = max(root.children, key=lambda x:x.wins)
    print('node_cnt=',node_cnt)
    print('TIMES=',TIMES)
    print('selected_couldnot_expand_cnt=',selected_couldnot_expand_cnt)
    print('sim_cnt=',sim_cnt)
    print('player_win_cnt:',player_win_cnt)
    print('opponent_win_cnt:',opponent_win_cnt)
    print('draw_cnt:',draw_cnt)
    print('select_cnt:',select_cnt)
    return best_child.move

def find_best_move(board, current_player):
     move = monte_carlo_search(board, current_player)
     return move
    

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

        if WIN==check_winner(board, OPPONENT):
            print("\n恭喜你！你赢了！")
            break
        if DRAW==check_winner(board, OPPONENT):
            print("\n平局！")
            break
        # AI玩家（玩家2）的回合
        print("\nAI的回合（O）:")
        t1 = time.time()
        ai_move = find_best_move(board, PLAYER)
        t2 = time.time()
        print('find best move cost:',t2-t1)
        r, c = ai_move
        board[r][c] = PLAYER
        print_board(board)

        if WIN==check_winner(board, PLAYER):
            print("\nAI赢了！")
            break
if __name__ == "__main__":
    play_game()

'''
#################################################################
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
############################
# 初始化一个棋盘
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
a,b = match_shapes_in_line_v2(board, 1, 1, 0, 1)
#print(board)
print(a)
print(b)

# 初始化一个棋盘
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
board[0][0]=1
board[0][1]=1
a,b = match_shapes_in_line_v2(board, 0, 0, 0, 1)
#print(board)
print(a)
print(b)

# 初始化一个棋盘
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
board[0][0]=1
board[1][1]=1
a,b = match_shapes_in_line_v2(board, 0, 0, 1, 1)
#print(board)
print(a)
print(b)

# 初始化一个棋盘
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
board[0][0]=1
board[1][0]=1
a,b = match_shapes_in_line_v2(board, 0, 0, 1, 0)
#print(board)
print(a)
print(b)

# 初始化一个棋盘
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
board[0][1]=1
board[0][2]=1
a,b = match_shapes_in_line_v2(board, 0, 1, 0, 1)
#print(board)
print(a)
print(b)

# 初始化一个棋盘
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
board[1][1]=1
board[2][2]=1
a,b = match_shapes_in_line_v2(board, 1, 1, 1, 1)
#print(board)
print(a)
print(b)

# 初始化一个棋盘
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
board[1][0]=1
board[2][0]=1
a,b = match_shapes_in_line_v2(board, 1, 0, 1, 0)
#print(board)
print(a)
print(b)

# 初始化一个棋盘
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
board[1][0]=1
board[2][0]=0
board[3][0]=1
a,b = match_shapes_in_line_v2(board, 1, 0, 1, 0)
#print(board)
print(a)
print(b)
# 初始化一个棋盘
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
board[1][0]=1
board[2][0]=0
board[3][0]=0
board[4][0]=1
a,b = match_shapes_in_line_v2(board, 1, 0, 1, 0)
#print(board)
print(a)
print(b)

# 初始化一个棋盘
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
# 设置一些棋子，假设玩家1为1，玩家2为-1
board[7][7] = 1  # 玩家1的棋子
board[7][8] = -1  # 玩家2的棋子
board[7][9] = 1  # 玩家1的棋子
board[8][7] = 1  # 玩家1的棋子
board[9][7] = 1  # 玩家1的棋子
a,b = match_shapes_in_line_v2(board, 0, 7, 1, 0)
#print(board)
print(a)
print(b)

####
# 初始化一个棋盘

####
'''
'''
# 初始化一个棋盘
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

# 设置一些棋子，假设玩家1为1，玩家2为-1
board[7][7] = 1  # 玩家1的棋子
board[7][8] = -1  # 玩家2的棋子
board[7][9] = 1  # 玩家1的棋子
board[8][7] = 1  # 玩家1的棋子
board[9][7] = 1  # 玩家1的棋子
#print(board)
# 扫描所有方向上的棋线
score = evaluate_board_v2(board)
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
score = evaluate_board_v2(board)
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
score = evaluate_board_v2(board)
#print(board)
print(score)
assert score==10100
'''
