import random

# 棋盘大小
BOARD_SIZE = 15

# 玩家标记
PLAYER_X = 1  # 玩家1（你）用 X
PLAYER_O = -1  # AI（玩家2）用 O
EMPTY = 0  # 空位

# 初始化棋盘
def init_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# 打印棋盘
def print_board(board):
    print("\n" + "  ".join([str(i).rjust(2) for i in range(BOARD_SIZE)]))  # 打印列号
    for r in range(BOARD_SIZE):
        row = [str(board[r][c]) for c in range(BOARD_SIZE)]
        print(f"{r:2} " + "  ".join(row))  # 打印行号

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

# 评估当前棋局的得分
def evaluate_board(board):
    score = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == PLAYER_X:
                score += 1
            elif board[r][c] == PLAYER_O:
                score -= 1
    return score

# Minimax算法
def minimax(board, depth, maximizing_player):
    if depth == 0 or check_winner(board, PLAYER_X) or check_winner(board, PLAYER_O):
        return evaluate_board(board)
    
    if maximizing_player:  # AI玩家
        max_eval = -float('inf')
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == EMPTY:  # 空位
                    board[r][c] = PLAYER_O
                    eval = minimax(board, depth-1, False)
                    max_eval = max(max_eval, eval)
                    board[r][c] = EMPTY
        return max_eval
    else:  # 玩家1
        min_eval = float('inf')
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == EMPTY:  # 空位
                    board[r][c] = PLAYER_X
                    eval = minimax(board, depth-1, True)
                    min_eval = min(min_eval, eval)
                    board[r][c] = EMPTY
        return min_eval

# 找到AI的最佳落子
max_depth = 1
def find_best_move(board):
    best_move = None
    best_value = -float('inf')
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == EMPTY:  # 空位
                board[r][c] = PLAYER_O
                move_value = minimax(board, max_depth, False)  # 深度设置为3
                if move_value > best_value:
                    best_value = move_value
                    best_move = (r, c)
                board[r][c] = EMPTY
    return best_move

# 玩家1（你）输入落子位置
def player_move(board):
    while True:
        try:
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
        board[r][c] = PLAYER_X
        print_board(board)

        if check_winner(board, PLAYER_X):
            print("\n恭喜你！你赢了！")
            break

        # AI玩家（玩家2）的回合
        print("\nAI的回合（O）:")
        ai_move = find_best_move(board)
        r, c = ai_move
        board[r][c] = PLAYER_O
        print_board(board)

        if check_winner(board, PLAYER_O):
            print("\nAI赢了！")
            break

if __name__ == "__main__":
    play_game()
