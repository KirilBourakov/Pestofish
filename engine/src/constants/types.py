from engine.src.constants.constants import BLACK, WHITE
from typing import TypedDict


# Represents the way a piece can move
Vector = TypedDict('Vector', {'maxForce': int, 'directions': list[tuple[int, int]]})

# Represents a list of pieces that can see a square by color
coloredPiecesList = TypedDict('BoardAnalysis', {BLACK: list[tuple[int, int]], WHITE: list[tuple[int, int]]})