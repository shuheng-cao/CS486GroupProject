#!/usr/bin/env python3

from Piece import Tetromino

import numpy as np
import math

class Field():

    WIDTH = 10
    HEIGHT = 20
    SCORING_ELEMENTS = 6

    def __init__(self, state=None):
        """
        Initializes a Tetris Field.
        Rows increase downward and columns increase to the right.
        """
        if state is not None:
            self.state = np.array(state, dtype=np.uint8, copy=True)
        else:
            self.state = np.full((Field.HEIGHT, Field.WIDTH), 0, dtype=np.uint8)

    def __str__(self):
        """
        Returns a string representation of the field.
        """
        bar = '   |' + ' '.join(map(str, range(Field.WIDTH))) + '|\n'
        mapped_field = np.vectorize(Tetromino.TYPES.__getitem__)(self.state)
        field = '\n'.join(['{:2d} |'.format(i) +
            ' '.join(row) + '|' for i, row in enumerate(mapped_field)])
        return bar + field + '\n' + bar

    def _test_tetromino_(self, tetromino, r_start, c_start):
        """
        Tests to see if a tetromino can be placed at the specified row and
        column. It performs the test with the top left corner of the
        tetromino at the specified row and column.
        """
        r_end, c_end = r_start + tetromino.height(), c_start + tetromino.width()
        if c_start < 0 or c_end > Field.WIDTH:
            return False
        if r_start < 0 or r_end > Field.HEIGHT:
            return False
        test_area = self.state[r_start:r_end, c_start:c_end]
        for s, t in zip(test_area.flat, tetromino.flat()):
            if s != 0 and t != 0:
                return False
        return True

    def _place_tetromino_(self, tetromino, r_start, c_start):
        """
        Place a tetromino at the specified row and column.
        The bottom left corner of the tetromino will be placed at the specified
        row and column. This function does not perform checks and will overwrite
        filled spaces in the field.
        """
        r_end, c_end = r_start + tetromino.height(), c_start + tetromino.width()
        if c_start < 0 or c_end > Field.WIDTH:
            return False
        if r_start < 0 or r_end > Field.HEIGHT:
            return False
        for tr, sr in enumerate(range(r_start, r_end)):
            for tc, sc, in enumerate(range(c_start, c_end)):
                if tetromino[tr][tc] != 0:
                    self.state[sr][sc] = tetromino[tr][tc]

    def _get_tetromino_drop_row_(self, tetromino, column):
        """
        Given a tetromino and a column, return the row that the tetromino
        would end up in if it were dropped in that column.
        Assumes the leftmost column of the tetromino will be aligned with the
        specified column.
        """
        if column < 0 or column + tetromino.width() > Field.WIDTH:
            return -1
        last_fit = -1
        for row in range(tetromino.height(), Field.HEIGHT):
            if self._test_tetromino_(tetromino, row, column):
                last_fit = row
            else:
                return last_fit
        return last_fit
    
    def copy(self):
        """
        Returns a shallow copy of the field.
        """
        return Field(self.state)

    def _line_clear_(self):
        """
        Checks and removes all filled lines.
        """
        filled = np.array([row.all() and row.any() for row in self.state])
        num_clear_lines = len(self.state[filled])
        non_filled = np.array(
            [not row.all() and row.any() for row in self.state])
        if non_filled.any():
            tmp = self.state[non_filled]
            self.state.fill(0)
            self.state[Field.HEIGHT - tmp.shape[0]:] = tmp
        return num_clear_lines

    def drop(self, tetromino, column):
        """
        Drops a tetromino in the specified column.
        The leftmost column of the tetromino will be aligned with the specified
        column.
        Returns the row it was dropped in for computations or -1 if a drop was
        unable to be computed.
        """
        assert isinstance(tetromino, Tetromino)
        row = self._get_tetromino_drop_row_(tetromino, column)
        if row == -1:
            return row, -1
        self._place_tetromino_(tetromino, row, column)
        num_lines_cleared = self._line_clear_()
        return row, num_lines_cleared

    def count_gaps(self):
        """
        Check each column one by one to make sure there are no gpas in the
        column.
        """
        rows_with_holes = set()
        well_cells = 0
        gaps = 0
        filled_rows_above_highest_hole = 0
        # Cut off all the empty space above all the placed tetrominos
        top_indices = np.argmax(self.state.T != 0, axis = 1)
        # Count the number of gaps past the first filled space per column
        for col, top in zip(self.state.T, top_indices):
            for index in range(top, 20):
                if col[index] == 0:
                    gaps += 1
                    rows_with_holes.add(index)
        lst = sorted(rows_with_holes)
        if len(rows_with_holes):
            highest_hole = 20 - lst[0]
        else:
            highest_hole = 0

        for pos, row in enumerate(self.state):
            if pos == highest_hole:
                break
            elif row.all():
                filled_rows_above_highest_hole += 1

        top_indices -= 1
        for col in range(1,9):
            cur_row = top_indices[col]
            if not self.state[cur_row][col] and self.state[cur_row][col - 1] and self.state[cur_row][col + 1]:
                well_cells += 1
        return len(rows_with_holes), gaps, highest_hole, filled_rows_above_highest_hole, well_cells

    def heights(self):
        """
        Return an array containing the heights of each column.
        """
        heights = Field.HEIGHT - np.argmax(self.state.T != 0, axis=1)
        max_height = np.amax(heights)
        total_bumpiness = 0
        max_bumpiness = 0
        for i in range(9):
            bumpiness = abs(heights[i]- heights[i+1])
            max_bumpiness = max(bumpiness, max_bumpiness)
            total_bumpiness += bumpiness
        return max_height, max_bumpiness, total_bumpiness

    def get_scoring_vector(self):
        """
        Get a vector of values derived from the field used to score a tetromino
        placement.
        """
        max_height, max_bumpiness, total_bumpiness = self.heights()
        rows_with_holes, holes, highest_hole, filled_rows_above_highest_hole, well_cells = self.count_gaps()
        return np.array([
            holes,                          # number of holes
            total_bumpiness,                # sum of bumpiness
            max_height,                     # maximum height
            np.count_nonzero(self.state),   # number of blocks
            rows_with_holes,                # rows with holes
            max_bumpiness,                  # max bumpiness
            well_cells,                     # well cells
            highest_hole,                   # highest hole
            filled_rows_above_highest_hole  # rows above the highest hole
        ])

    def get_optimal_drop(self, tetromino, weights=None):
        """
        Given a tetromino and a vector of scoring weights, this method
        calculates the best placement of the tetromino, scoring each placement
        with the weight vector.
        """
        rotations = [
            tetromino,
            tetromino.copy().rotate_right(),
            tetromino.copy().flip(),
            tetromino.copy().rotate_left()
        ]

        best_field = None
        best_drop_score = math.inf
        for rotation, tetromino_ in enumerate(rotations):
            for column in range(Field.WIDTH):
                f = self.copy()
                row, num_lines_cleared = f.drop(tetromino_, column)
                if row == -1:
                    continue
                scoring_vector = f.get_scoring_vector()
                scoring_vector = np.insert(scoring_vector, 0, num_lines_cleared)
                if weights is not None:
                    score = scoring_vector.dot(weights)
                else:
                    score = scoring_vector.sum()
                if score < best_drop_score:
                    best_drop_score = score
                    best_field = f
        return best_field, num_lines_cleared