from engine.src.constants.static import PAWN, ROOK, BISHOP, KNIGHT, QUEEN, WHITE, KING, EMPTY, MIDDLE_GAME, END_GAME

rook_map: list[list[int]] = [
    [4] * 8,
    [20] * 8,
    [7] * 8,
    [0] * 8,
    [0] * 8,
    [0] * 8,
    [0] * 8,
    [0] * 8
]

knight_map: list[list[int]] = [
    [-40,-30,-20,-10,-10,-20,-30,-40],
    [-30,  0, 10, 10, 10, 10,  0,-30],
    [-20, -1, 25, 25, 25, 25, -1,-20],
    [-10,  0, 20, 30, 30, 20,  0,-10],
    [-10,  0, 20, 25, 25, 20,  0,-10],
    [-20,  0, 20, 20, 20, 20,  0,-20],
    [-30, -2,  5,  0,  0,  5, -2,-30],
    [-40,-30,-20,-10,-10,-20,-30,-40],
]

bishop_map: list[list[int]] = [
    [-40,-10,-10,-10,-10,-10,-10,-40],
    [-30,  0,  0,  0,  0,  0,  0,-30],
    [-20,  0, 10, 10, 10,  0,  0,-20],
    [-10,  0, 30, 30, 30, 30,  0,-10],
    [-10,  0, 30, 30, 30, 30,  0,-10],
    [-20,  0, 25, 20, 20, 25,  0,-20],
    [-30, 20,  0,  0,  0,  5, 20,-30],
    [-40,-10,-10,-10,-10,-10,-10,-40]
]

pawn_map: list[list[int]] = [
    [0] * 8,
    [-30,  0,  0,  0,  0,  0,  0,-30],
    [50]*8,
    [ 40, 40, 40, 35, 45, 30, 40, 40],
    [ 20, 30, 30, 25, 30, 30, 20, 20],
    [ 10, 20, 25,  0, -5, 25, 20, 10],
    [-10, 10, 20,-20,-20, 20, 10,-10],
    [0] * 8
]

queen_map: list[list[int]] = [
    [40] * 8,
    [30] * 8,
    [20] * 8,
    [10] * 8,
    [10] * 8,
    [5] * 8,
    [5] * 8,
    [0] * 8
]

mg_king_map: list[list[int]] = [
    [-60] * 8,
    [-50] * 8,
    [-40] * 8,
    [-40] * 8,
    [-30] * 8,
    [  0,-20,-20,-20,-20,-20,-20,  0],
    [  0, -5,-10,-10,-10,-10, -5,  5],
    [ 40, 45, 45,-40,  0,-40, 45, 45],
]

eg_king_map: list[list[int]] = [
    [-40,-40,-30,-25,-25,-30,-40,-40],
    [-20,-10, -5, -5, -5, -5,-10,-20],
    [-15, -5, 20, 25, 25, 20, -5,-15],
    [-10, -5, 30, 40, 40, 30, -5,-10],
    [-10, -5, 25, 35, 35, 25, -5,-10],
    [-15, -5, 20, 25, 25, 20, -5,-15],
    [-20,-10, -5, -5, -5, -5,-10,-20],
    [-40,-40,-30,-25,-25,-30,-40,-40]
]

piece_value_map: dict[str, list[list[int]]] = {
    PAWN: pawn_map,
    BISHOP: bishop_map,
    KNIGHT: knight_map,
    ROOK: rook_map,
    QUEEN: queen_map,
    MIDDLE_GAME: mg_king_map,
    END_GAME: eg_king_map
}