import sqlite3
import os
import random
from engine.src.constants.engineTypes import boardType, MoveType
from engine.src.constants.static import EMPTY, WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EN_PASSENT
from engine.src.helpers.square_analysis import is_empty, get_type

class Searcher():
    def __init__(self) -> None:
        self.db_path = os.path.join(os.path.dirname(__file__), 'open.db')
        self.db = sqlite3.connect(self.db_path)
        self.executor = self.db.cursor()
        self.board = ''

        self.map = {
            f'{WHITE}{PAWN}': 'P',
            f'{WHITE}{KNIGHT}': 'N',
            f'{WHITE}{BISHOP}': 'B',
            f'{WHITE}{ROOK}': 'R',
            f'{WHITE}{QUEEN}': 'Q',
            f'{WHITE}{KING}': 'K',

            f'{BLACK}{PAWN}': 'p',
            f'{BLACK}{KNIGHT}': 'n',
            f'{BLACK}{BISHOP}': 'b',
            f'{BLACK}{ROOK}': 'r',
            f'{BLACK}{QUEEN}': 'q',
            f'{BLACK}{KING}': 'k',
        }

        self.square_letter_map = {
            0: 'a',
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h'
        }
    
    def query_theory(self, board: boardType, color_to_move: str) -> MoveType:
        '''Given a board state, return a random theoretical move it has.'''
        fen = self.board_to_fen(board, color_to_move)

        results = self.executor.execute('SELECT new from transpositions WHERE inital == (SELECT pk FROM positions WHERE position == ?)', (fen,))
        results = results.fetchall()
        
        chosen = random.choice(results)

        new_pos = self.executor.execute('SELECT position FROM positions WHERE pk == ?', (chosen[0],))
        new_pos_str: str = new_pos.fetchone()[0]

        return self.get_move_from_fen(fen.split()[0], new_pos_str.split()[0])

    def get_move_from_fen(self, old_pos: str, new_pos: str) -> MoveType:
        '''Given two FEN strings that are 1 move apart, return the move that was played.'''
        print(old_pos)
        print(new_pos)

    def board_to_fen(self, board: boardType, color_to_move: str) -> str:
        '''Given a boardType and the color who's turn it is to move, return a FEN string (move and halfmove counter removed).'''
        fen = ''
        count = 0
        ep_pos = (-1, -1)
        for y in range(8):
            for x in range(8):
                square = board[y][x]
                if is_empty(square):
                    if get_type(square) == EN_PASSENT:
                        ep_pos = (x,y)
                    count += 1
                else:
                    if count > 0:
                        fen += str(count)
                        count = 0
                    fen += self.map[square[0].lower() + square[1]]
            if count > 0:
                fen += str(count)
                count = 0
            if y < 7:
                fen += '/'
        fen += f'  {color_to_move}'

        castle_rights = ''
        # white castling
        king_not_moved = get_type(board[7][4]) == KING and board[7][4][0] == 'W'
        king_rook_not_moved = get_type(board[7][7]) == ROOK and board[7][7][0] == 'W'
        if king_not_moved and king_rook_not_moved:
            castle_rights += 'K'
        queen_rook_not_moved = get_type(board[7][0]) == ROOK and board[7][0][0] == 'W'
        if king_not_moved and queen_rook_not_moved:
            castle_rights += 'Q'

        # black castling
        king_not_moved = get_type(board[0][4]) == KING and board[0][4][0] == 'B'
        king_rook_not_moved = get_type(board[0][7]) == ROOK and board[0][7][0] == 'B'
        if king_not_moved and king_rook_not_moved:
            castle_rights += 'k'
        queen_rook_not_moved = get_type(board[0][0]) == ROOK and board[0][0][0] == 'B'
        if king_not_moved and queen_rook_not_moved:
            castle_rights += 'q'

        # no one can castle
        if castle_rights == '':
            castle_rights = '-' 

        fen += f'  {castle_rights}'

        if ep_pos[0] == -1:
            en_passent = '-'
        else:
            en_passent = self.square_letter_map[ep_pos[0]] + str(ep_pos[1]+1)
        fen += f'  {en_passent}'
        return fen