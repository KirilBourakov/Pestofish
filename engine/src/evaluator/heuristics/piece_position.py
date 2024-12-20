from engine.src.evaluator.heuristics.constants import piece_value_map
from engine.src.helpers.board_analysis import get_color, get_type, is_empty
from engine.src.constants.static import PAWN, ROOK, BISHOP, KNIGHT, QUEEN, WHITE, KING, EMPTY, MIDDLE_GAME, END_GAME, BLACK

def piece_position(square: str, location: tuple[int,int], is_endgame: bool) -> int:
    '''factor in the position of a piece'''
    factor: int = 1 if get_color(square) == WHITE else -1
    magnatude: float = 1.25

    if is_empty(square):
        return 0

    return int(piece_value_map[str(is_endgame)][square[0].lower() + square[1]][location[1]][location[0]] * factor * magnatude)