from multiprocessing import Process, Queue, JoinableQueue
from engine.src.constants.static import BLACK, WHITE, KING, EMPTY, EN_PASSENT, PAWN
from engine.src.constants.engineTypes import MoveType, boardType, RunType
from .helpers.helpers import flip
from .helpers.board_analysis import sight_on_square, find_king
from .generator.generator import Generator
from .evaluator.evaluator import Evaluator
from .helpers.square_analysis import get_color, get_type
import copy

class EngineRunner(Process):
    def __init__(self, tasks: JoinableQueue, results: Queue, transposeTable: dict[str, float]) -> None:
        Process.__init__(self)
        self.tasks: JoinableQueue[tuple[MoveType, boardType, str]] = tasks
        self.results: Queue[RunType] = results

        self.generator: Generator = Generator()
        self.evaluator: Evaluator = Evaluator()
        self.transposeTable = transposeTable


    def run(self) -> None:
        while True:
            move, board, color = self.tasks.get()

            move, value, board, depth = self.transformer(move, board, color)
            result = RunType(move=move,value=value,board=board,depth=depth)

            self.tasks.task_done()
            self.results.put(result)

    def update(self, new: dict[str, float]) -> None:
        self.transposeTable = new

    def transformer(self, move: MoveType, board: boardType, color: str) -> tuple[MoveType, float, boardType, int]:
        '''transforms a list of value moves into one that carries a result and a transformed position'''
        new_pos: list[list[str]] = self.result(board, move)
        pos_val: tuple[float, int] = self.value(new_pos, color)
        return (move, pos_val[0], new_pos, pos_val[1])  
    
    def value(self, pos: list[list[str]], perspective: str, curr_depth: int = 1, 
            max_depth: int=3, max_val:float=float('-inf'), min_val:float=float('inf')) -> tuple[float, int]:
        '''Estimates the value of a move using evaluator and MINIMAX. Currently unfinished. 

        Keyword arguments:
        \t pos -- a board position
        \t perspective -- the perspective from which to examine the moves (IE, the person who just moved)
        \t currDepth -- the depth to which we have explored (default = 1)
        \t max_depth -- the max deppth of the engine (default = 3)
        \t max_val -- the top most value found (used in pruning) (default = -inf) 
        \t min_val -- the bottom most value found (used in pruning) (default = inf) 
        '''
        # TODO: taking far too long. Replace with bfs search to make code more debuggable 
        # TODO: eval seems to be wrong on occasion? Was getting negatives for seemingly no reason
        # base cases
        enemy_perspective: str = flip(perspective)
        if str(pos) in self.transposeTable:
            return (self.transposeTable[str(pos)], curr_depth)
        finished: bool = self.is_termainal(pos)
        if curr_depth >= max_depth or finished:
            return (self.evaluator.net_eval(pos, finished, enemy_perspective), curr_depth)
        
        # get all the possible moves
        possible_moves: list[MoveType] = self.generator.get_moves(pos, find_king(pos, enemy_perspective))
        # initalize dummy values for the best_value
        best_value = float('-inf') if enemy_perspective == WHITE else float('inf')
        search_depth = 0
        # for every move
        for move in possible_moves:
            new_pos: list[list[str]] = self.result(pos, move)
            # get the value of the new position
            pos_val, n_depth = self.value(new_pos, enemy_perspective, curr_depth=curr_depth+1, max_val=max_val, min_val=min_val)
            # update the value as needed
            if enemy_perspective == WHITE and pos_val > best_value:
                search_depth = n_depth
                best_value = max(best_value, pos_val)
            elif enemy_perspective == BLACK and pos_val < best_value:
                search_depth = n_depth
                best_value = min(best_value, pos_val)

            # keep track of max and min
            if enemy_perspective == WHITE:
                max_val = max(max_val, pos_val)
            else:
                min_val = min(min_val, pos_val)
            # prune
            if min_val <= max_val:
                break
            
        return (best_value, search_depth)
    
    def is_termainal(self, board: list[list[str]]) -> bool:
        '''Returns if the game is over. 
        Keyword arguements:
        \t board - the board 
        '''
        for color in [WHITE, BLACK]:
            enemy = flip(color)

            # see if the enemy king is in check, but has no moves
            enemy_king_pos = find_king(board, enemy)
            moves: list[MoveType] = self.generator.get_moves(board, enemy_king_pos) 
            eyes_on_king: dict[str, list[tuple[int, int]]] = sight_on_square(board, enemy_king_pos)
            king_in_check: bool = len(eyes_on_king[color]) > 0
            # a king is in checkmate
            if king_in_check: 
                if len(moves) == 0:
                    return True
            # stalemate
            if len(moves) == 0:
                return True

        # draw by fifty move rule
        # if self.fifty_move_rule_counter / 2 >= 50:
        #     return True
        return False
    
    def result(self, board: list[list[str]], move: MoveType) -> list[list[str]]:
        '''Simulates a board position
        
        Keyword arguements:
        \t board - the board 
        \t move - a dict of moveType, representing the move
        '''
        oldx, oldy = move['original']
        newx, newy = move['new']

        piece_type = get_type(board[oldy][oldx])
        color = get_color(board[oldy][oldx])

        new_board: list[list[str]] = copy.deepcopy(board)
        new_board[newy][newx] = new_board[oldy][oldx]
        new_board[newy][newx] = new_board[newy][newx][0].lower() + new_board[newy][newx][1]
        new_board[oldy][oldx] = EMPTY

        if move['promotion'] != '':
            new_board[newy][newx] = new_board[newy][newx][0].lower() + move['promotion']
        # enpassent
        if get_type(board[newy][newx]) == EN_PASSENT and piece_type == PAWN:
            offset = 1 if color == WHITE else -1
            
            new_board[newy+offset][newx] = EMPTY
        
        # double move (to place enpassent)
        delta_y = abs(oldy - newy)
        if piece_type == PAWN and delta_y == 2:
            offset = -1 if color == BLACK else 1
            new_board[newy+offset][newx] = color + EN_PASSENT

        # castling (if the king is moving more then 1 square, it must be castling)
        delta_x = abs(oldx - newx)
        if piece_type == KING and delta_x > 1:
            if newx == 2:
                new_board[newy][0] = EMPTY
                new_board[newy][newx+1] = board[newy][0].lower()
            elif newx == 6:
                new_board[newy][7] = EMPTY
                new_board[newy][5] = board[newy][0].lower()

        return new_board
