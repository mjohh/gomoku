def evaluate_scan_line(line, player):
    """
    对扫描线进行棋形匹配
    :param line: 一维列表，表示棋盘的一行、一列或一条对角线
    :param player: 当前玩家（1 或 2）
    :return: 一个字典，记录每种棋形出现的次数
    """
    # 棋形计数
    pattern_count = {
        "five_in_a_row": 0,
        "live_four": 0,
        "blocked_four": 0,
        "live_three": 0,
        "sleep_three": 0,
        "live_two": 0,
        "sleep_two": 0
    }

    n = len(line)
    opponent = 3 - player  # 对手的棋子
    i = 0

    while i <= n - 5:  # 窗口长度为 5
        window = line[i:i + 5]  # 当前窗口
        player_count = 0  # 计数玩家棋子的数量
        opponent_count = 0  # 计数对手棋子的数量
        empty_count = 0  # 计数空位数量
        consecutive_player = True  # 追踪是否是连续玩家棋子
        consecutive_opponent = False  # 追踪是否是连续对手棋子

        # 检查窗口内的棋子，判断是否为连续的棋子
        for j in range(5):
            if window[j] == player:
                if consecutive_opponent:  # 如果遇到对手棋子，跳出循环
                    consecutive_player = False
                    break
                player_count += 1
            elif window[j] == opponent:
                if consecutive_player:  # 如果遇到玩家棋子，跳出循环
                    consecutive_opponent = True
                    break
                opponent_count += 1
            else:
                empty_count += 1

        # 窗口两端检查
        left_blocked = (i - 1 < 0 or line[i - 1] == opponent)  # 左端是否被堵
        right_blocked = (i + 5 >= n or line[i + 5] == opponent)  # 右端是否被堵

        # 根据连续的棋子数和窗口两端判断棋形
        if player_count == 5:  # 连五
            pattern_count["five_in_a_row"] += 1
            i += 1  # 连五优先，跳过1个位置继续
            continue
        elif player_count == 4 and empty_count == 1:  # 四连
            if not left_blocked and not right_blocked:
                pattern_count["live_four"] += 1  # 两端均未堵
            else:
                pattern_count["blocked_four"] += 1  # 一端被堵
            i += 1
            continue
        elif player_count == 3 and empty_count == 2:  # 三连
            if not left_blocked and not right_blocked:
                pattern_count["live_three"] += 1  # 两端均未堵
            else:
                pattern_count["sleep_three"] += 1  # 一端被堵
            i += 1
            continue
        elif player_count == 2 and empty_count == 3:  # 二连
            if not left_blocked and not right_blocked:
                pattern_count["live_two"] += 1  # 两端均未堵
            else:
                pattern_count["sleep_two"] += 1  # 一端被堵
            i += 1
            continue

        i += 1  # 如果没有匹配到任何棋形，则窗口右移一格

    return pattern_count

# 示例棋盘的一行
#line = [0, 1, 1, 0, 1, 1, 0, 0, 2, 2, 2, 1, 1, 1, 1, 0]
line = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# 当前玩家是 1
player = 1

# 检查棋形
result = evaluate_scan_line(line, player)

# 打印结果
print(line)
print("棋形统计：", result)

