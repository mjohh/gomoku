from gomoku_v2 import * 
from test import *

def test_heuristic_evaluate():
    # 测试棋局1：连五
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    board[7][7:12] = [1, 1, 1, 1, 1]  # 连五
    score = heuristic_evaluate(board, 1)
    board[7][7:12] = [0, 0, 0, 0, 0]  # 连五
    print(f"测试棋局1（连五）得分: {score}")

    board[7][7] = 1  # 连五
    board[8][8] = 1  # 连五
    board[9][9] = 1  # 连五
    board[10][10] = 1  # 连五
    board[11][11] = 1  # 连五
    score = heuristic_evaluate(board, 1)
    board[7][7] = 0  # 连五
    board[8][8] = 0  # 连五
    board[9][9] = 0  # 连五
    board[10][10] = 0  # 连五
    board[11][11] = 0  # 连五
    print(f"测试棋局1（连五）得分: {score}")

    board[0][13] = 1  # 连五
    board[1][12] = 1  # 连五
    board[2][11] = 1  # 连五
    board[3][10] = 1  # 连五
    board[4][9] = 1  # 连五
    score = heuristic_evaluate(board, 1)
    board[0][13] = 0  # 连五
    board[1][12] = 0  # 连五
    board[2][11] = 0  # 连五
    board[3][10] = 0  # 连五
    board[4][9] = 0  # 连五
    print(f"测试棋局1（连五）得分: {score}")

    # 测试棋局2：活四
    board[7][6:10] = [1, 1, 1, 1]  # 活四
    score = heuristic_evaluate(board, 1)
    board[7][6:10] = [0, 0, 0, 0]  # 活四
    print(f"测试棋局2（活四）得分: {score}")

    # 测试棋局3：冲四
    board[7][6:10] = [1, 1, 1, 1]  # 冲四
    board[7][10] = -1  # 堵住一端
    score = heuristic_evaluate(board, 1)
    board[7][6:10] = [0, 0, 0, 0]  # 冲四
    board[7][10] = 0  # 堵住一端
    print(f"测试棋局3（冲四）得分: {score}")

    # 测试棋局4：活三
    board[7][6:9] = [1, 1, 1]  # 活三
    score = heuristic_evaluate(board, 1)
    board[7][6:9] = [0, 0, 0]  # 活三
    print(f"测试棋局4（活三）得分: {score}")

    # 测试棋局5：眠三
    board[7][6:9] = [1, 1, 1]  # 眠三
    board[7][9] = -1  # 堵住一端
    score = heuristic_evaluate(board, 1)
    board[7][6:9] = [0, 0, 0]  # 眠三
    board[7][9] = 0  # 堵住一端
    print(f"测试棋局5（眠三）得分: {score}")

    # 测试棋局6：活二
    board[7][6:8] = [1, 1]  # 活二
    score = heuristic_evaluate(board, 1)
    board[7][6:8] = [0, 0]  # 活二
    print(f"测试棋局6（活二）得分: {score}")

    # 测试棋局7：眠二
    board[7][6:8] = [1, 1]  # 眠二
    board[7][8] = -1  # 堵住一端
    score = heuristic_evaluate(board, 1)
    board[7][6:8] = [0, 0]  # 眠二
    board[7][8] = 0  # 堵住一端
    print(f"测试棋局7（眠二）得分: {score}")

    # 连五+对手冲四
    board[0][13] = 1  # 连五
    board[1][12] = 1  # 连五
    board[2][11] = 1  # 连五
    board[3][10] = 1  # 连五
    board[4][9] = 1  # 连五
    board[7][6:10] = [-1, -1, -1, -1]  # 冲四
    board[7][10] = 1  # 堵住一端
    score = heuristic_evaluate(board, 1)
    board[7][6:10] = [0, 0, 0, 0]  # 冲四
    board[7][10] = 0  # 堵住一端
    board[0][13] = 0  # 连五
    board[1][12] = 0  # 连五
    board[2][11] = 0  # 连五
    board[3][10] = 0  # 连五
    board[4][9] = 0  # 连五
    print(f"测试棋局（连五+对手冲四）得分: {score}")

# 调用测试函数
test_heuristic_evaluate()
