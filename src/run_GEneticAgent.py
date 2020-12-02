from Board import Field
from Piece import Tetromino
import cv2
from PIL import Image
import random
import time
import numpy as np

COLORS = {
    0: (255, 255, 255),
    1: (247, 64, 99),
    2: (0, 167, 247),
}

def play(cur_field, best_field, col, row, piece, old_score, new_score):
    
    for r in range(piece.height(), row+1):
        default = cur_field.copy()
        default._place_tetromino_graphv(piece, r, col)
        render(default.state,old_score)
        
    render(best_field.state, new_score)

def render(board, score):
    '''Renders the current board'''
    img = [COLORS[p] for row in board for p in row]
    img = np.array(img).reshape(20, 10, 3).astype(np.uint8)
    img = img[..., ::-1] # Convert RRG to BGR (used by cv2)
    img = Image.fromarray(img, 'RGB')
    img = img.resize((10 * 25, 20 * 25))
    img = np.array(img)
    cv2.putText(img, str(score), (22, 22), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
    cv2.imshow('image', np.array(img))
    cv2.waitKey(1)

def show():
    weights = [-0.13915911, 0.67934716, 0.44521076, 0.54977305, -0.06502272, 0.44480747, -0.17748352,  0.18160665,  0.75582129,  0.39691385]
    tetrominos = [
        Tetromino.ITetromino(),
        Tetromino.OTetromino(),
        Tetromino.TTetromino(),
        Tetromino.STetromino(),
        Tetromino.ZTetromino(),
        Tetromino.JTetromino(),
        Tetromino.LTetromino()
    ]
    field = Field()
    pieces = 0
    cleared_lines = 0
    score = 0
    while True:
        cur_field = field
        tetromino = random.choice(tetrominos)
        best_field, num_lines_cleared, row, col, piece = cur_field.get_optimal_drop(tetromino, weights)
        if best_field == None:
            break
        # print(field)

        pieces += 1
        cleared_lines += num_lines_cleared
        old_score = score
        score = pieces + (10 * cleared_lines* cleared_lines)

        play(cur_field, best_field, col, row, piece, old_score, score)
        
        field = best_field
        time.sleep(0.1)
    print('Performance: {}'.format(pieces))

show()