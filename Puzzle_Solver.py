from copy import copy, deepcopy
from queue import PriorityQueue


class State(object):
    def __init__(self,gameBoard,level):
        self.gameBoard = gameBoard
        self.possiMove = []
        self.curreMoves = []
        self.level = level
        self.aStar = 0

    def generatePossiMove(self):
        posiMove = []
        if self.gameBoard[0][0] != '0' and self.gameBoard[1][0] != '0' and self.gameBoard[2][0] != '0':
            posiMove.append('L')
        if self.gameBoard[0][2] != '0' and self.gameBoard[1][2] != '0' and self.gameBoard[2][2] != '0':
            posiMove.append('R')
        if '0' not in self.gameBoard[0]:
            posiMove.append('U')
        if '0' not in self.gameBoard[2]:
            posiMove.append('D')
        self.possiMove = posiMove

    def generateAstar(self, goal_board):
        mah = 0
        for i in range(1, 9):
            sLoc = findLoc(self.gameBoard, str(i))
            gLoc = findLoc(goal_board, str(i))
            mah = mah + abs(sLoc[0] - gLoc[0]) + abs(sLoc[1] - gLoc[1])
        self.aStar = self.level + mah

    def __gt__(self, other):
        if self.aStar > other.aStar:
            return True
        else:
            return False


def readFile(filename):
    f = open(filename, "r")
    content = f.read().splitlines()
    fileBoard = [line.split() for line in content]
    return fileBoard[0:3], fileBoard[4:7]

def boardPrint(gameBoard):
    for i in gameBoard:
        print(i)

def findLoc(gameBoard, item):
    for i in range(3):
        for j in range(3):
            if gameBoard[i][j] == item:
                return [i,j]


def boardMove(currBoard, move):
    whiteLoc = findLoc(currBoard, '0')
    newBoard = deepcopy(currBoard)
    if move == 'U':
        newBoard[whiteLoc[0]][whiteLoc[1]] = newBoard[whiteLoc[0]-1][whiteLoc[1]]
        newBoard[whiteLoc[0]-1][whiteLoc[1]] = '0'
    elif move == 'D':
        newBoard[whiteLoc[0]][whiteLoc[1]] = newBoard[whiteLoc[0]+1][whiteLoc[1]]
        newBoard[whiteLoc[0]+1][whiteLoc[1]] = '0'
    elif move == 'L':
        newBoard[whiteLoc[0]][whiteLoc[1]] = newBoard[whiteLoc[0]][whiteLoc[1]-1]
        newBoard[whiteLoc[0]][whiteLoc[1]-1] = '0'
    elif move == 'R':
        newBoard[whiteLoc[0]][whiteLoc[1]] = newBoard[whiteLoc[0]][whiteLoc[1]+1]
        newBoard[whiteLoc[0]][whiteLoc[1]+1] = '0'
    return newBoard

def generateNewState(currState, move, goal_board):
    newBoard = boardMove(currState.gameBoard, move)
    newState = State(newBoard,currState.level+1)
    currMoves = deepcopy(currState.curreMoves)
    currMoves.append(move)
    newState.curreMoves = currMoves
    newState.generateAstar(goal_board)
    newState.generatePossiMove()
    return newState


initial_board, goal_board = readFile("input2.txt")
initial_state = State(initial_board,0)
initial_state.generatePossiMove()
initial_state.generateAstar(goal_board)
visited_board = [initial_board]
pri_queue = [initial_state]
counter = 1
while pri_queue:
    pri_queue.sort(reverse=True)
    current_state = pri_queue.pop()
    if current_state.gameBoard == goal_board:
        print("Correct Moves:",current_state.curreMoves)
        print("Depth:",current_state.level)
        print("Node created:", counter)
        break
    for move in current_state.possiMove:
        newState = generateNewState(current_state, move, goal_board)
        if newState.gameBoard in visited_board:
            continue
        else:
            counter += 1
            visited_board.append(newState.gameBoard)
            pri_queue.append(newState)