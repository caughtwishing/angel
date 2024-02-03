from mines.accuracy import *

class Algorithm:
    def __init__(self,history):
        self.max_tiles = 4
        self.history = history
    def predict(self):
        history = self.history

        board = [0] * 25
        n = 0

        def get_spot(a, b):
            nonlocal n
            for val in [abs(tup[0] - tup[1]) for tup in zip(a, b)]:
                if board[val] == 0 and n < self.max_tiles:
                    board[val] = 1
                    n += 1

        for v in history:
            if n < self.max_tiles:
                get_spot(v['uncoveredLocations'], v['mineLocations'])
            else:
                break
        accuracy = get_accuracy(board)
        board = ["✅" if x == 1 else "💣" for x in board]
        board_str = "\n".join("".join(map(str, board[i:i + 5])) for i in range(0, len(board), 5))
        return board_str, accuracy
