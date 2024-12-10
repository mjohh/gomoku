def evaluate_board(board):
    score = 0

    # 遍历每一个位置，检查各个方向上的棋形
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            # 如果当前位置是玩家1的棋子
            if board[x, y] == 1:
                directions = [(-1, 0), (0, -1), (-1, -1), (-1, 1)]
                for direction in directions:
                    # 评估不同棋形
                    if is_active_four(board, x, y, direction[0], direction[1]):
                        score += ACTIVE_FOUR_SCORE
                    elif is_active_three(board, x, y, direction[0], direction[1]):
                        score += ACTIVE_THREE_SCORE
                    elif is_dead_three(board, x, y, direction[0], direction[1]):
                        score += DEAD_THREE_SCORE
                    elif is_active_two(board, x, y, direction[0], direction[1]):
                        score += ACTIVE_TWO_SCORE
    return score

def in_board(i,j)
    return i>-1 and i<BOARD_SIZE and j>-1 and j<BOARD_SIZE

def match_shapes_in_line_v2(board, x0, y0, dr, dc):
    l = BOARD_SIZE
    i=x0
    j=y0
    player_cnts = {shape:0 for shape in shapes}
    opponent_cnts = {shape:0 for shape in shapes}

    while i<l and j<l and i>-1 and j>-1:
        cnt = 1
        player=EMPTY
        starti = i
        startj = j
        start_blocken = False
        end_blocken = False

        while True:
            if in_board(i+dr,j+dc) and board[i][j]!=EMPTY  and board[i][j]==board[i+dc][j+dr] and cnt<5:
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
            if player!=EMPTY:
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
