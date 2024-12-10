import numpy as np

# 定义棋盘大小
BOARD_SIZE = 15

# 定义棋形评分
SCORES = {
    "five": 10000,  # 五连
    "alive_four": 800,  # 活四
    "dead_four": 200,  # 死四
    "alive_three": 150,  # 活三
    "dead_three": 50,  # 死三
    "alive_two": 20,    # 活二
    "dead_two": 0,      # 死二
}

# 检查一个位置是否越界
def is_valid(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

# 计算棋盘状态的评估分数
def evaluate_board(board, player):
    """
    根据棋盘状态评估当前局面。
    :param board: 当前棋盘的状态，二维数组
    :param player: 当前评估的玩家（1 或 -1）
    :return: 局面得分
    """
    score = 0
    visited = np.zeros_like(board, dtype=bool)  # 用于标记已经评估过的位置
    
    # 扫描所有方向：水平、垂直、两个对角线
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    # 遍历棋盘每个位置
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # 如果当前位置为空或者已经扫描过，跳过
            if board[i][j] != 0 or visited[i][j]:
                continue
            
            for direction in directions:
                # 对每个方向进行棋形检测
                line_score, positions = evaluate_line(board, i, j, direction, player)
                if line_score > 0:
                    # 如果这条线得分大于0，标记这些位置已经被评估过
                    for pos in positions:
                        if pos is not None:  # 确保pos不是None
                            visited[pos[0], pos[1]] = True
                score += line_score
    
    return score

# 评估一条线上的棋形
def evaluate_line(board, x, y, direction, player):
    """
    评估从(x, y)开始，在指定方向上可能的棋形。
    :param board: 当前棋盘的状态
    :param x: 起始位置的x坐标
    :param y: 起始位置的y坐标
    :param direction: 方向元组（dx, dy）
    :param player: 当前评估的玩家（1 或 -1）
    :return: 此方向上的得分和涉及的位置
    """
    # 扫描出一条长度为5的棋线
    line = []
    positions = []
    for i in range(-4, 5):
        nx, ny = x + direction[0] * i, y + direction[1] * i
        if is_valid(nx, ny):
            line.append(board[nx][ny])
            positions.append((nx, ny))
        else:
            line.append(None)  # 越界的位置用None表示
            positions.append(None)  # 对应的位置为None

    return calculate_score_for_line(line, player, positions)

# 根据一条棋线计算得分，并返回涉及的位置
def calculate_score_for_line(line, player, positions):
    """
    根据一条线（5个位置）上的棋形计算得分。
    :param line: 5个位置上的棋子状态（1、-1 或 0 或 None）
    :param player: 当前评估的玩家（1 或 -1）
    :param positions: 该线上的位置（用于标记已评估）
    :return: 该线的得分以及涉及的位置
    """
    filtered_line = [c for c in line if c is not None]
    
    # 如果该线已经有五个棋子，直接返回对应的得分
    if len(filtered_line) == 5 and all(c == player for c in filtered_line):
        return SCORES["five"], positions
    
    # 检查棋形
    score = 0
    player_count = filtered_line.count(player)
    opponent_count = filtered_line.count(-player)
    
    # 判断棋形种类
    if player_count == 4 and opponent_count == 0:
        score += SCORES["alive_four"]
        print('alive_four')
    elif player_count == 4 and opponent_count == 1:
        score += SCORES["dead_four"]
        print('dead_four')
    elif player_count == 3 and opponent_count == 0:
        score += SCORES["alive_three"]
        print('alive_treee')
    elif player_count == 3 and opponent_count == 1:
        score += SCORES["dead_three"]
        print('dead_three')
    elif player_count == 2 and opponent_count == 0:
        score += SCORES["alive_two"]
        print('alive_two')
    elif player_count == 2 and opponent_count == 1:
        score += SCORES["dead_two"]
        print('dead_two')

    return score, positions

# 示例用法
if __name__ == "__main__":
    # 初始化一个空棋盘
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    
    # 设置玩家1和玩家2的一些棋子
    board[7][7] = 1  # 玩家1的棋子
    board[7][8] = -1  # 玩家2的棋子
    board[7][9] = 1  # 玩家1的棋子
    board[8][7] = 1  # 玩家1的棋子
    board[9][7] = 1  # 玩家1的棋子
    
    # 评估棋盘，假设评估玩家1
    score = evaluate_board(board, 1)
    print(board)
    print(f"当前局面的评分: {score}")

