import random
import cv2
import numpy as np
from PIL import Image
from time import sleep

# Tetris game class
class Tetris:

    '''Tetris game class'''

    # BOARD
    MAP_EMPTY = 0
    MAP_BLOCK = 1
    MAP_PLAYER = 2
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20

    TETROMINOS = {
        0: { # I
            0: [(0,0), (1,0), (2,0), (3,0)],
            90: [(1,0), (1,1), (1,2), (1,3)],
            180: [(3,0), (2,0), (1,0), (0,0)],
            270: [(1,3), (1,2), (1,1), (1,0)],
        },
        1: { # T
            0: [(1,0), (0,1), (1,1), (2,1)],
            90: [(0,1), (1,2), (1,1), (1,0)],
            180: [(1,2), (2,1), (1,1), (0,1)],
            270: [(2,1), (1,0), (1,1), (1,2)],
        },
        2: { # L
            0: [(1,0), (1,1), (1,2), (2,2)],
            90: [(0,1), (1,1), (2,1), (2,0)],
            180: [(1,2), (1,1), (1,0), (0,0)],
            270: [(2,1), (1,1), (0,1), (0,2)],
        },
        3: { # J
            0: [(1,0), (1,1), (1,2), (0,2)],
            90: [(0,1), (1,1), (2,1), (2,2)],
            180: [(1,2), (1,1), (1,0), (2,0)],
            270: [(2,1), (1,1), (0,1), (0,0)],
        },
        4: { # Z
            0: [(0,0), (1,0), (1,1), (2,1)],
            90: [(0,2), (0,1), (1,1), (1,0)],
            180: [(2,1), (1,1), (1,0), (0,0)],
            270: [(1,0), (1,1), (0,1), (0,2)],
        },
        5: { # S
            0: [(2,0), (1,0), (1,1), (0,1)],
            90: [(0,0), (0,1), (1,1), (1,2)],
            180: [(0,1), (1,1), (1,0), (2,0)],
            270: [(1,2), (1,1), (0,1), (0,0)],
        },
        6: { # O
            0: [(1,0), (2,0), (1,1), (2,1)],
            90: [(1,0), (2,0), (1,1), (2,1)],
            180: [(1,0), (2,0), (1,1), (2,1)],
            270: [(1,0), (2,0), (1,1), (2,1)],
        }
    }

    COLORS = {
        0: (255, 255, 255),
        1: (247, 64, 99),
        2: (0, 167, 247),
    }


    def __init__(self):
        self.reset()

    
    def reset(self):
        '''Resets the game, returning the current state'''
        self.board = [[0] * Tetris.BOARD_WIDTH for _ in range(Tetris.BOARD_HEIGHT)]
        self.game_over = False
        self.bag = list(range(len(Tetris.TETROMINOS)))
        random.shuffle(self.bag)
        self.next_piece = self.bag.pop()
        self._new_round()
        self.score = 0
        self.blocks = 0
        return self._get_board_props(self.board)


    def _get_rotated_piece(self):
        '''Returns the current piece, including rotation'''
        return Tetris.TETROMINOS[self.current_piece][self.current_rotation]


    def _get_complete_board(self):
        '''Returns the complete board, including the current piece'''
        piece = self._get_rotated_piece()
        piece = [np.add(x, self.current_pos) for x in piece]
        board = [x[:] for x in self.board]
        for x, y in piece:
            board[y][x] = Tetris.MAP_PLAYER
        return board


    def get_game_score(self):
        '''Returns the current game score.

        Each block placed counts as one.
        For lines cleared, it is used BOARD_WIDTH * lines_cleared ^ 2.
        '''
        return self.score
    

    def _new_round(self):
        '''Starts a new round (new piece)'''
        # Generate new bag with the pieces
        if len(self.bag) == 0:
            self.bag = list(range(len(Tetris.TETROMINOS)))
            random.shuffle(self.bag)
        
        self.current_piece = self.next_piece
        self.next_piece = self.bag.pop()
        self.current_pos = [3, 0]
        self.current_rotation = 0

        if self._check_collision(self._get_rotated_piece(), self.current_pos):
            self.game_over = True


    def _check_collision(self, piece, pos):
        '''Check if there is a collision between the current piece and the board'''
        for x, y in piece:
            x += pos[0]
            y += pos[1]
            print(f"checking {x,y}")
            if x < 0 or x >= Tetris.BOARD_WIDTH or y < 0:
                return 1
            if y >= Tetris.BOARD_HEIGHT or self.board[y][x] == Tetris.MAP_BLOCK:
                return 2
        return False


    def _rotate(self, angle):
        '''Change the current rotation'''
        r = self.current_rotation + angle

        if r == 360:
            r = 0
        if r < 0:
            r += 360
        elif r > 360:
            r -= 360

        self.current_rotation = r


    def _add_piece_to_board(self, piece, pos):
        '''Place a piece in the board, returning the resulting board'''        
        board = [x[:] for x in self.board]
        for x, y in piece:
            print(f"Adding piece to board {y + pos[1], x + pos[0]}")
            board[y + pos[1]][x + pos[0]] = Tetris.MAP_BLOCK
        self.blocks += 4
        return board


    def _clear_lines(self, board):
        '''Clears completed lines in a board'''
        ''' return features 1 '''
        # Check if lines can be cleared
        lines_to_clear = [index for index, row in enumerate(board) if sum(row) == Tetris.BOARD_WIDTH]
        print(f"lines need to clean {lines_to_clear}")
        if lines_to_clear:
            board = [row for index, row in enumerate(board) if index not in lines_to_clear]
            # Add new lines at the top
            for _ in lines_to_clear:
                board.insert(0, [0 for _ in range(Tetris.BOARD_WIDTH)])
            self.blocks -= len(lines_to_clear) * Tetris.BOARD_WIDTH
        return len(lines_to_clear), board


    def _number_of_holes(self, board):
        '''Number of holes in the board (empty sqquare with at least one block above it)'''
        ''' return features 2, 9, 10, 6, 8'''
        holes = 0
        num_rows_with_hole = set()
        min_i = 21 #
        highest_hole = 0
        lst = []
        well_cells = 0

        for col in zip(*board):
            i = 0
            while i < Tetris.BOARD_HEIGHT and col[i] != Tetris.MAP_BLOCK:
                i += 1
            lst.append(i)
            min_i = min(i, min_i)
            highest_hole = Tetris.BOARD_HEIGHT - min_i
            cur_hole = []
            for r in col[i+1:]:
                if r == Tetris.MAP_EMPTY:
                    cur_hole.append(r)
                    num_rows_with_hole.add(r)
            # cur_hole = len([x for x in col[i+1:] if x == Tetris.MAP_EMPTY])
            holes += len(cur_hole)
        for i in range(len(lst)):
            if i == 0:
                if lst[1] != lst[0]:
                    well_cells += 1
            elif i == len(lst) - 1:
                if lst[i] != lst[i -1]:
                    well_cells += 1
            else:
                if lst[i] != lst[i -1] and lst[i] != lst[i + 1]:
                    well_cells += 1
                

        return holes, highest_hole, min_i, len(num_rows_with_hole), well_cells


    def _bumpiness(self, board):
        '''Sum of the differences of heights between pair of columns'''
        ''' return features 3, 7'''
        total_bumpiness = 0
        max_bumpiness = 0
        min_ys = []

        for col in zip(*board):
            i = 0
            while i < Tetris.BOARD_HEIGHT and col[i] != Tetris.MAP_BLOCK:
                i += 1
            min_ys.append(i)
        
        for i in range(len(min_ys) - 1):
            bumpiness = abs(min_ys[i] - min_ys[i+1])
            max_bumpiness = max(bumpiness, max_bumpiness)
            total_bumpiness += abs(min_ys[i] - min_ys[i+1])

        return total_bumpiness, max_bumpiness


    def _height(self, board):
        '''Sum and maximum height of the board'''
        ''' retrun features 4'''
        sum_height = 0
        max_height = 0
        min_height = Tetris.BOARD_HEIGHT

        for col in zip(*board):
            i = 0
            while i < Tetris.BOARD_HEIGHT and col[i] == Tetris.MAP_EMPTY:
                i += 1
            height = Tetris.BOARD_HEIGHT - i
            sum_height += height
            if height > max_height:
                max_height = height
            elif height < min_height:
                min_height = height

        return sum_height, max_height, min_height


    def _get_board_props(self, board):
        '''Get properties of the board'''
        lines, board = self._clear_lines(board)
        holes, highest_hole, min_i, num_rows_with_hole, well_cells = self._number_of_holes(board)
        total_bumpiness, max_bumpiness = self._bumpiness(board)
        sum_height, max_height, min_height = self._height(board)
        return [lines, holes, total_bumpiness, max_height, self.blocks, num_rows_with_hole, max_bumpiness, well_cells, highest_hole, min_i]


    def get_next_states(self):
        '''Get all possible next states'''
        states = {}
        piece_id = self.current_piece
        
        if piece_id == 6: 
            rotations = [0]
        elif piece_id == 0:
            rotations = [0, 90]
        else:
            rotations = [0, 90, 180, 270]

        # For all rotations
        for rotation in rotations:
            piece = Tetris.TETROMINOS[piece_id][rotation]
            min_x = min([p[0] for p in piece])
            max_x = max([p[0] for p in piece])

            # For all positions
            for x in range(-min_x, Tetris.BOARD_WIDTH - max_x):
                pos = [x, 0]

                # Drop piece
                while not self._check_collision(piece, pos):
                    pos[1] += 1
                pos[1] -= 1

                # Valid move
                if pos[1] >= 0:
                    board = self._add_piece_to_board(piece, pos)
                    states[(x, rotation)] = self._get_board_props(board)

        return states


    def get_state_size(self):
        '''Size of the state'''
        return 4


    def key_control(self, x, rotation, reversed=False):
        # for player mode, we have x to be -1 (left), 0 (down), 1 (right)
        # and rotation to be -1 (clockwise) or 1 (counter clockwise)
        if reversed:
            multiplier = -1
        else:
            multiplier = 1

        # print(f"get multiplier {multiplier}")

        if rotation:
            degree = 90 * multiplier
            # print(f"rotation with degrees {degree}")
            if rotation > 0:
                self._rotate(-degree)
            else:
                self._rotate(degree)
        else:
            if x:
                # print(f"horizontal move {x * multiplier}")
                self.current_pos[0] += x * multiplier
            else:
                # print(f"vertical move {multiplier}")
                self.current_pos[1] += multiplier

    def _init_game(self):
            self._new_round()
            self.render()

    def play(self, x, rotation, render=False, render_delay=None, player_mode=False):
        '''Makes a play given a position and a rotation, returning the reward and if the game is over'''
        # print("playing as player")
        if not player_mode:
            self.current_pos = [x, 0]
            self.current_rotation = rotation
        else:
            self.finished_round = False # for player mode only

        # print(f"player mode with current state: {self.current_pos, self.current_rotation}")

        if player_mode:
            self.key_control(x, rotation)
            # print(f"after key control: {self.current_pos, self.current_rotation}")
            
            check = self._check_collision(self._get_rotated_piece(), self.current_pos)
            if check > 0:
                print(f"the value of check is {check}")
                self.key_control(x, rotation, reversed=True)
                if check == 2:
                    print("collision here, start new game")
                    self.finished_round = True
            else:
                print("successfully rendered")
                self.render()

        else:
            # Drop piece
            while not self._check_collision(self._get_rotated_piece(), self.current_pos):
                if render:
                    self.render()
                    if render_delay:
                        sleep(render_delay)
                self.current_pos[1] += 1
            self.current_pos[1] -= 1

        # Update board and calculate score
        if (not player_mode) or self.finished_round:
            print(f"calculating score for {self.current_pos}, {self.current_rotation}")
            self.board = self._add_piece_to_board(self._get_rotated_piece(), self.current_pos)
            lines_cleared, self.board = self._clear_lines(self.board)
            score = 1 + (lines_cleared ** 2) * Tetris.BOARD_WIDTH
            self.score += score
            self.finished_round = False
            self._new_round()
            self.render()

        if not player_mode:
            # Start new round
            self._new_round()
        if self.game_over:
            score -= 2

        # print("about to return")
        if not player_mode:
            return score, self.game_over


    def render(self):
        '''Renders the current board'''
        img = [Tetris.COLORS[p] for row in self._get_complete_board() for p in row]
        img = np.array(img).reshape(Tetris.BOARD_HEIGHT, Tetris.BOARD_WIDTH, 3).astype(np.uint8)
        img = img[..., ::-1] # Convert RRG to BGR (used by cv2)
        img = Image.fromarray(img, 'RGB')
        img = img.resize((Tetris.BOARD_WIDTH * 25, Tetris.BOARD_HEIGHT * 25))
        img = np.array(img)
        cv2.putText(img, str(self.score), (22, 22), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        cv2.imshow('image', np.array(img))
        cv2.waitKey(1)
        # print("finishing rendering")
