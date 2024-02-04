from mines.accuracy import *
import math

class Algorithm2:
    def __init__(self, history):
        self.max_tiles = 4
        self.history = history
    @staticmethod
    def is_neighbor(pos1: int, pos2: int) -> bool:
        row1, col1 = divmod(pos1, 5)
        row2, col2 = divmod(pos2, 5)
        distance = math.sqrt((row2 - row1) ** 2 + (col2 - col1) ** 2)
        return False if distance >= 1 else True

    def predict(self):
        x = self.history
        maxv = 0
        board = [0] * 25
        for ind in range(25):
            if not Algorithm2.is_neighbor(x[ind], x[max(ind + 1, 24)]) and maxv < self.max_tiles:
                board[x[ind]] = 1
                maxv += 1
            elif maxv >= self.max_tiles:
                break
            else:
                pass
        accuracy = get_accuracy(board)
        board = ["✅" if x == 1 else "💣" for x in board]
        board = "\n".join("".join(map(str, board[i:i + 5])) for i in range(0, len(board), 5))
        return board, accuracy
