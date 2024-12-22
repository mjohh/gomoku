## -*- coding: utf-8 -*-
import math
import random
import unittest
import copy

BOARD_SIZE = 3
PLAYER = 1
OPPONENT = -1
TIMES = 800 

#board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def is_game_over(board):
    #check row
    for row in board:
        if sum(row)==3 or sum(row)==-3:
            return True, sum(row)//3
    #check col
    for col in range(BOARD_SIZE):
        col_sum = sum([board[row][col] for row in range(BOARD_SIZE)])
        if col_sum==3 or col_sum==-3:
            return True, col_sum//3
    #check diagonal
    diag1_sum = sum([board[i][i] for i in range(BOARD_SIZE)])
    diag2_sum = sum([board[i][BOARD_SIZE-1-i] for i in range(BOARD_SIZE)])
    if diag1_sum==3 or diag1_sum==-3:
        return True, diag1_sum//3
    if diag2_sum==3 or diag2_sum==-3:
        return True, diag2_sum//3
    #if board is full, draw
    if all([board[row][col]!=0 for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)]):
        return True, 0.5 #let ai learn draw, better than loss
    return False, None

def get_possible_moves(board):
    moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col]==0:
                moves.append((row, col))
    return moves

def make_move(state, move, player):
    #new_state = [row.copy() for row in state]
    new_state = [copy.deepcopy(row) for row in state]
    row, col = move
    new_state[row][col] = player 
    return new_state

class TreeNode:
    def __init__(self, state, player, parent=None):
        self.state = state #board state
        self.player = player
        self.parent = parent #parent node
        self.children = [] #children nodes list
        self.visits = 0 #node visited cnt
        self.wins = 0 #wins cnt start from this node
        self.move = (None,None)#the move cause the state

C = 1.414

def print_node(node):
    print('state=',node.state,'player=',node.player,'children=',node.children,'v=',node.visits,'w=',node.wins,'mv=',node.move)

def uct_val(node):
    if node.visits==0:
        return float('inf')
    return node.wins/node.visits + C*math.sqrt(math.log(node.parent.visits)/node.visits)

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

def expand(node):
    possible_moves = get_possible_moves(node.state)
    for move in possible_moves:
        new_state = make_move(node.state, move, -node.player)
        child = TreeNode(new_state, -node.player, parent=node)
        child.move=move #record the move for return of main proces
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
        state = make_move(state, move)
'''
def simulate(node):
    player = node.player
    state = node.state
    while True:
        game_over,winner = is_game_over(state)
        if game_over:
            return winner
        possible_moves = get_possible_moves(state)
        move = random.choice(possible_moves)
        player = -player
        state =  make_move(state, move, player)

def backpropagate(node, result):
    while node:
        node.visits += 1
        if result==PLAYER:
            node.wins += 1
        # learn draw, better than loss
        elif result==0.5:
            node.wins += 0.5
        node = node.parent

def monte_carlo_search(board, player):
    #game begin,asume no.0 step is -1, then the no.1 step will be 1
    root = TreeNode(board, -player)
    for _ in range(TIMES):
        selected = select(root)
        #print_node(selected)
        children = expand(selected)
        if children:
            #simulated_state = random.choice(children).state
            #result = simulate(simulated_state)
            child = random.choice(children)
            result = simulate(child)
            #backpropagate(selected, resul)
            backpropagate(child, result)#backpropagate from the bottom node
    print_mcts_tree(root,depth=2)
    best_child = max(root.children, key=lambda x:x.wins)
    return best_child.move

# 打印棋盘函数
def print_board(board):
    for row in board:
        print(" | ".join(map(lambda x: "X" if x == 1 else ("O" if x == -1 else " "), row)))
        print("-" * (BOARD_SIZE * 4 - 1))
    print('')


# 用于打印蒙特卡罗树的函数，通过递归遍历树节点，增加参数depth控制打印层数
def print_mcts_tree(node, indent="", is_last=True, depth=float('inf')):
    if depth == 0:
        return
    # 先打印当前节点的信息
    symbol = "└── " if is_last else "├── "
    #print(indent + symbol + f"Player: {node.player}, Move: {node.move}, Visits: {node.visits}, Wins: {node.wins}")
    print(indent + symbol + "Player: %s, Move: %s, Visits: %s, Wins: %s" % (node.player, node.move, node.visits, node.wins))
    indent += "    " if is_last else "│   "
    # 获取子节点列表长度，用于判断是否是最后一个子节点
    child_count = len(node.children)
    for index, child in enumerate(node.children):
        is_last_child = index == child_count - 1
        print_mcts_tree(child, indent, is_last_child, depth - 1)

if __name__ == "__main__":
    # 初始化棋盘
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    # 假设玩家1先开始
    current_player = 1
    print("井字棋游戏开始！")
    #print_board(board)
    while True:
        game_over, winner = is_game_over(board)
        if game_over:
            if winner == 0:
                print("平局！")
            else:
                #print(f"玩家{winner}获胜！")
                print("玩家%s获胜！" % winner)
            break
        if current_player == 1:
            # 玩家1使用蒙特卡罗搜索算法来决策落子位置
            move = monte_carlo_search(board, current_player)
            board = make_move(board, move, current_player)
            current_player = -1
        else:
            # 玩家2进行用户输入落子
            while True:
                try:
                    #row = int(input("请输入你要落子的行（0 - 2）："))
                    #col = int(input("请输入你要落子的列（0 - 2）："))
                    print("请输入你的走法 (行 列): ")
                    row, col = map(int, raw_input().split())
                    if (row, col) in get_possible_moves(board):
                        board = make_move(board, (row, col), current_player)
                        current_player = 1
                        break
                    else:
                        print("该位置已被占用，请重新输入！")
                except ValueError:
                    print("输入无效，请输入整数！")
        print_board(board)
'''
# 测试类，继承自unittest.TestCase
class TestMonteCarloTree(unittest.TestCase):
    def setUp(self):
        # 初始化一个简单的初始棋盘状态，用于测试
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    # 测试节点扩展功能
    def test_expand(self):
        root = TreeNode(self.board, 1)
        initial_children_count = len(root.children)
        children = expand(root)
        self.assertEqual(len(children) > initial_children_count, True)

    # 测试选择操作
    def test_select(self):
        root = TreeNode(self.board, 1)
        children = expand(root)
        selected_node = select(root)
        self.assertEqual(isinstance(selected_node, TreeNode), True)

    # 测试模拟操作是否能正常结束游戏并返回结果
    def test_simulate(self):
        root = TreeNode(self.board, 1)
        children = expand(root)
        simulated_child = random.choice(children)
        result = simulate(simulated_child)
        self.assertEqual(result in [1, -1, 0], True)

    # 测试反向传播是否正确更新节点的访问次数和获胜次数
    def test_backpropagate(self):
        root = TreeNode(self.board, 1)
        children = expand(root)
        simulated_child = random.choice(children)
        result = simulate(simulated_child)
        backpropagate(simulated_child, result)
        self.assertEqual(simulated_child.visits > 0, True)
        self.assertEqual(simulated_child.wins >= 0, True)

    # 测试蒙特卡罗搜索主函数是否能返回一个合法的落子位置
    def test_monte_carlo_search(self):
        result = monte_carlo_search(self.board, 1)
        self.assertEqual(result in get_possible_moves(self.board), True)


if __name__ == '__main__':
    unittest.main()


class TestIsGameOver(unittest.TestCase):
    def test_win_in_row(self):
        """测试行方向获胜的情况"""
        board = [[1, 1, 1],
                 [0, 0, 0],
                 [0, 0, 0]]
        result = is_game_over(board)
        self.assertEqual(result, (True, 1))

    def test_win_in_column(self):
        """测试列方向获胜的情况"""
        board = [[1, 0, 0],
                 [1, 0, 0],
                 [1, 0, 0]]
        result = is_game_over(board)
        self.assertEqual(result, (True, 1))

    def test_win_in_diagonal_1(self):
        """测试主对角线方向获胜的情况"""
        board = [[1, 0, 0],
                 [0, 1, 0],
                 [0, 0, 1]]
        result = is_game_over(board)
        self.assertEqual(result, (True, 1))

    def test_win_in_diagonal_2(self):
        """测试副对角线方向获胜的情况"""
        board = [[0, 0, 1],
                 [0, 1, 0],
                 [1, 0, 0]]
        result = is_game_over(board)
        self.assertEqual(result, (True, 1))

    def test_draw(self):
        """测试平局的情况"""
        board = [[-1, -1, 1],
                 [1, 1, -1],
                 [-1, -1, 1]]
        result = is_game_over(board)
        self.assertEqual(result, (True, 0))

    def test_game_not_over(self):
        """测试游戏未结束的情况"""
        board = [[1, 0, 0],
                 [0, 1, 0],
                 [0, 0, 0]]
        result = is_game_over(board)
        self.assertEqual(result, (False, None))

if __name__ == '__main__':
    unittest.main()
'''
