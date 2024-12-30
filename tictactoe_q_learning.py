import numpy as np
import random


# 初始化井字棋棋盘，0表示空位，1表示玩家1（智能体），-1表示玩家2（人）
board_size = 3
board = np.zeros((board_size, board_size), dtype=int)

# 初始化Q表，所有值初始化为0，状态数量根据棋盘可能情况计算，动作数量为9（9个格子可落子）
num_states = 3 ** (board_size * board_size)
num_actions = board_size * board_size
Q_table = np.zeros((num_states, num_actions))

# 学习率
learning_rate = 0.1
# 折扣因子
discount_factor = 0.9
# 探索率
epsilon = 0.1


# 根据棋盘状态获取对应的状态编号（简单将棋盘状态转换为一个整数表示）
def get_state_number(board):
    state_num = 0
    multiplier = 1
    for row in board.flatten():
        state_num += (row + 1) * multiplier
        multiplier *= 3
        #print("当前状态编号计算:", state_num)
    return state_num


def get_empty_positions(board):
    empty_positions = []
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == 0:
                empty_positions.append(row * board_size + col)
    return empty_positions

def choose_action(state, epsilon, board):
    empty_positions = get_empty_positions(board)
    if not empty_positions:
        return None
    action = None
    while True:
        if random.random() < epsilon:
            action_idx = random.randint(0, len(empty_positions) - 1)
            action = empty_positions[action_idx]
        else:
            action_idx = np.argmax([Q_table[state, pos] for pos in empty_positions])
            action = empty_positions[action_idx]
        return action


# 执行动作，更新棋盘状态
def take_action(board, action):
    row = action // board_size
    col = action % board_size
    if board[row][col] == 0:
        board[row][col] = 1
    return board


# 检查游戏是否结束，返回结果（1表示玩家1赢，-1表示玩家2赢，0表示未结束或平局）
def check_game_over(board):
    # 检查行
    for row in board:
        if np.sum(row) == 3:
            return 1
        elif np.sum(row) == -3:
            return -1
    # 检查列
    for col in range(board_size):
        if np.sum(board[:, col]) == 3:
            return 1
        elif np.sum(board[:, col]) == -3:
            return -1
    # 检查对角线
    if np.sum(board.diagonal()) == 3 or np.sum(np.fliplr(board).diagonal()) == 3:
        return 1
    elif np.sum(board.diagonal()) == -3 or np.sum(np.fliplr(board).diagonal()) == -3:
        return -1
    # 检查是否平局（棋盘已满）
    if np.count_nonzero(board) == board_size * board_size:
        return 0
    return None

def human_random_action(board):
    available_actions = []
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == 0:
                available_actions.append(row * board_size + col)
    return random.choice(available_actions)

def statistic_qtable(tbl):
    n = 0
    for i in range(num_states):
        for j in range(num_actions): 
            if tbl[i][j]!=0:
                n += 1
    print('non zeros elem=', n)

num_episodes = 1000
agent_win=0
human_win=0
draw=0
for episode in range(num_episodes):
    #global agent_win
    #global human_win
    #global draw
    #print('---------------episode=',episode, '-----------------')        
    board = np.zeros((board_size, board_size), dtype=int)
    game_over = False
    while not game_over:
        # 智能体选择动作并落子
        current_state = get_state_number(board)
        action = choose_action(current_state, epsilon, board)
        board = take_action(board, action).copy()
        result = check_game_over(board)
        # add by mjohh
        agent_reward = 0
        human_reward = 0
        if result is not None:
            game_over = True
            if result == 1:
                agent_reward = 1
                human_reward = -1
                agent_win += 1
            elif result == -1:
                agent_reward = -1
                human_reward = 1
                human_win += 1
            else:
                # let agent learn draw
                agent_reward = 0.5
                human_reward = 0
                draw += 1
            #print('agent_reward=',agent_reward)        
            # 更新智能体的Q表
            #print(board)
            new_state = get_state_number(board)
            #print(new_state)
            v = learning_rate * (agent_reward + discount_factor * np.max(Q_table[new_state, :]) - Q_table[current_state, action])
            Q_table[current_state, action] += v 
            #print('Q_table[{}][{}]={}'.format(current_state, action, v) )
            break
        #print(board)
        # 模拟人类玩家选择动作并落子
        human_action = human_random_action(board)  # 这里可以替换成更复杂的人类策略函数
        board[human_action // board_size][human_action % board_size] = -1
        result = check_game_over(board)
        if result is not None:
            game_over = True
            # same as above, mjohh
            if result == 1:
                agent_reward = 1
                human_reward = -1
                agent_win += 1
            elif result == -1:
                agent_reward = -1
                human_reward = 1
                human_win += 1
            else:
                # let agent learn draw
                agent_reward = 0.5
                human_reward = 0
                draw += 1
            #print('agent_reward=',agent_reward)        
        #print('')
        #print(board)
        #print('agent_reward=',agent_reward)
        #print('human_win=',human_win, 'agent_win=',agent_win, 'draw=',draw)

        # 更新智能体的Q表
        #print(board)
        new_state = get_state_number(board)
        #print(new_state)
        v = learning_rate * (agent_reward + discount_factor * np.max(Q_table[new_state, :]) - Q_table[current_state, action])
        Q_table[current_state, action] += v 
        #print('Q_table[{}][{}]={}'.format(current_state, action, v) )

print('human_win=',human_win, 'agent_win=',agent_win, 'draw=',draw)
print(Q_table)
statistic_qtable(Q_table)

while True:

    # 人与训练后智能体对局
    print("欢迎来和训练后的智能体玩井字棋游戏！")
    board = np.zeros((board_size, board_size), dtype=int)
    game_over = False
    while not game_over:
        # 智能体下棋
        current_state = get_state_number(board)
        action = choose_action(current_state, 0, board)  # 利用为主，探索率设为0
        board = take_action(board, action).copy()
        print("智能体下棋后的棋盘：")
        print(board)
        result = check_game_over(board)
        if result is not None:
            game_over = True
            if result == 1:
                print("智能体获胜！")
            elif result == -1:
                print("你获胜！")
            else:
                print("平局！")
            break

        # 玩家下棋
        print("请输入你要落子的位置（行 列，从0开始计数）：")
        player_row, player_col = map(int, input().split())
        while board[player_row][player_col]!= 0:
            print("该位置已有棋子，请重新输入你要落子的位置（行 列，从0开始计数）：")
            player_row, player_col = map(int, input().split())
        board[player_row][player_col] = -1
        print("你下棋后的棋盘：")
        print(board)
        result = check_game_over(board)
        if result is not None:
            game_over = True
            if result == 1:
                print("智能体获胜！")
            elif result == -1:
                print("你获胜！")
            else:
                print("平局！")
