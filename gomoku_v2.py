
# 初始化棋盘
def init_board():
    return [[0 for _ in range(15)] for _ in range(15)]

# 打印棋盘
def print_board(board):
    for row in board:
        print(" ".join(["X" if cell == 1 else "O" if cell == -1 else "-" for cell in row]))
    print()


# 判断游戏是否结束
def evaluate(board):
    # 检查行
    for row in board:
        for i in range(11):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == row[i+4] and row[i] != 0:
                return row[i]*100000
    
    # 检查列
    for col in range(15):
        for i in range(11):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == board[i+4][col] and board[i][col] != 0:
                return board[i][col]*100000
    
    # 检查对角线（从左上到右下）
    for i in range(11):
        for j in range(11):
            if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == board[i+4][j+4] and board[i][j] != 0:
                return board[i][j]*100000
    
    # 检查对角线（从右上到左下）
    for i in range(11):
        for j in range(4, 15):
            if board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] == board[i+4][j-4] and board[i][j] != 0:
                return board[i][j]*100000
    
    # 检查是否平局
    if all(cell != 0 for row in board for cell in row):
        return 0
    
    # 游戏未结束
    return None

# 检查连五、活四、冲四、活三、眠三、活二、眠二
def count_patterns(line):
    patterns = {
        "XXXXX": 100000,  # 连五
        ".XXXX.": 10000,  # 活四
        ".XXXX|": 1000,   # 冲四
        "|XXXX.": 1000,   # 冲四
        ".XXX.": 1000,    # 活三
        ".XXX|": 100,     # 眠三
        "|XXX.": 100,     # 眠三
        ".XX.": 100,      # 活二
        ".XX|": 10,       # 眠二
        "|XX.": 10        # 眠二
    }
    total_score = 0
    for pattern, value in patterns.items():
        total_score += line.count(pattern) * value
    return total_score

def count_patterns_by_rows(board, player):
    opponent = -player
    score = 0
    for row in board:
        s = "".join(["X" if cell == player else "|" if cell == opponent else "." for cell in row])
        score += count_patterns(s)
        #print(s)
    return score


def count_patterns_by_columns(board, player):
    score = 0
    opponent = -player
    for col in range(len(board[0])):
        column = [board[row][col] for row in range(len(board))]
        s = "".join(["X" if cell == player else "|" if cell == opponent else "." for cell in column])
        score += count_patterns(s)
    return score

def count_patterns_by_main_diagonals(board, player):
    # 获取棋盘的行数和列数
    rows = len(board)
    cols = len(board[0])
    score = 0
    opponent = -player

    # 逐行打印主对角线方向的棋盘
    for start_row in range(rows):
        diagonal = []
        x, y = start_row, 0
        while x < rows and y < cols:
            diagonal.append(board[x][y])
            x += 1
            y += 1
        s = "".join(["X" if cell == player else "|" if cell == opponent else "." for cell in diagonal])
        score += count_patterns(s)
        #print(s, score)

    for start_col in range(1, cols):
        diagonal = []
        x, y = 0, start_col
        while x < rows and y < cols:
            diagonal.append(board[x][y])
            x += 1
            y += 1
        s = "".join(["X" if cell == player else "|" if cell == opponent else "." for cell in diagonal])
        score += count_patterns(s)
        #print(s, score)
    return score

def count_patterns_by_anti_diagonals(board, player):
    # 获取棋盘的行数和列数
    rows = len(board)
    cols = len(board[0])
    score = 0
    opponent = -player

    # 逐行打印副对角线方向的棋盘
    for start_row in range(rows):
        diagonal = []
        x, y = start_row, 0
        while x >= 0 and y < cols:
            diagonal.append(board[x][y])
            x -= 1
            y += 1
        s = "".join(["X" if cell == player else "|" if cell == opponent else "." for cell in diagonal])
        score += count_patterns(s)

    for start_col in range(1, cols):
        diagonal = []
        x, y = rows - 1, start_col
        while x >= 0 and y < cols:
            diagonal.append(board[x][y])
            x -= 1
            y += 1
        s = "".join(["X" if cell == player else "|" if cell == opponent else "." for cell in diagonal])
        score += count_patterns(s)
    return score


def heuristic_evaluate(board, player):
    opponent = -player
    score = 0

    # 检查所有方向
    score += count_patterns_by_rows(board, player)
    score += count_patterns_by_columns(board, player)
    score += count_patterns_by_main_diagonals(board, player)
    score += count_patterns_by_anti_diagonals(board, player)

    score -= count_patterns_by_rows(board, opponent)
    score -= count_patterns_by_columns(board, opponent)
    score -= count_patterns_by_main_diagonals(board, opponent)
    score -= count_patterns_by_anti_diagonals(board, opponent)

    return score
    

# Minimax 算法 + Alpha-Beta 剪枝 + 最大搜索深度
def minimax(board, depth, max_depth, alpha, beta, is_maximizing, player):
    result = evaluate(board)
    if result is not None:
        return result
    
    if depth >= max_depth:
        return heuristic_evaluate(board, player)
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(15):
            for j in range(15):
                if board[i][j] == 0:
                    board[i][j] = player
                    score = minimax(board, depth + 1, max_depth, alpha, beta, False, -player)
                    board[i][j] = 0
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for i in range(15):
            for j in range(15):
                if board[i][j] == 0:
                    board[i][j] = -player
                    score = minimax(board, depth + 1, max_depth, alpha, beta, True, player)
                    board[i][j] = 0
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score

# 找到最佳走法
def find_best_move(board, max_depth):
    best_move = None
    best_score = -float('inf')
    for i in range(15):
        for j in range(15):
            if board[i][j] == 0:
                board[i][j] = 1
                score = minimax(board, 0, max_depth, -float('inf'), float('inf'), False, -1)
                board[i][j] = 0
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

# 主函数
def main():
    board = init_board()
    current_player = 1  # 1 表示玩家 X，-1 表示玩家 O
    max_depth = 1  # 设置最大搜索深度
    
    while True:
        print_board(board)
        result = evaluate(board)
        if result is not None:
            if result == 1:
                print("玩家 X 赢了！")
            elif result == -1:
                print("玩家 O 赢了！")
            else:
                print("平局！")
            break
        
        if current_player == 1:
            # 玩家 X 的回合
            move = find_best_move(board, max_depth)
            if move:
                board[move[0]][move[1]] = 1
            current_player = -1
        else:
            # 玩家 O 的回合
            print("请输入你的走法 (行 列): ")
            row, col = map(int, input().split())
            if board[row][col] == 0:
                board[row][col] = -1
                current_player = 1
            else:
                print("非法走法，请重试！")

if __name__ == "__main__":
    main()
