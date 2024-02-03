## GET ACCURACY FUNCTION

def get_accuracy(n_b):
    board = [0] * 25
    for i, v in enumerate(board):
        if i in n_b:
            board[i] = 1
    n = (sum(board) + 4) / len(board) * 100
    return 100 - n