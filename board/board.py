import pygame
import assets.assets as assets
import pieces.white_pieces as wp
import pieces.black_pieces as bp
import globals

class Chess_Board():
    def __init__(self):
        self.set_board()

    def set_board(self):
        self.board = [
            [bp.rookL, bp.knight, bp.bishop, bp.queen, bp.king, bp.bishop, bp.knight, bp.rookR],
            [bp.pawn] * 8,
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [wp.pawn] * 8,
            [wp.rookL, wp.knight, wp.bishop, wp.queen, wp.king, wp.bishop, wp.knight, wp.rookR]
        ]
        self.move_counter = 0
        self.selected_square = None
        self.past_board_states = {}
        self.waiting_for_promotion = False

    def click(self, gridx, gridy):
        # TODO: make it so that a peice can only be selected on it's own turn.
        if self.selected_square == (gridx, gridy):
            return
        if self.selected_square is None and self.board[gridy][gridx] is not None:
            if self.move_counter % 2 == 0 and self.board[gridy][gridx].color == "white": 
                self.selected_square = (gridx, gridy)
            elif self.move_counter % 2 != 0 and self.board[gridy][gridx].color == "black":
                self.selected_square = (gridx, gridy) 
            return
        
        if self.selected_square != None:
            self.move(gridx, gridy)
            self.selected_square = None
            return
        
    def is_legal_move(self, newx, newy):
        # TODO: this function should be replaced with get_legal_moves which returns a list of all the moves a piece can make
        piece = self.board[self.selected_square[1]][self.selected_square[0]]
        
        # This checks that there is nothing blocking you from moving to that square
        oldx, oldy = self.selected_square
        while (abs(oldx-newx) > 1 or abs(oldy-newy) > 1) and piece.hops == False:
            # walk across, taking the same path as the peice.  
            if oldx < newx:
                oldx += 1
            if oldx > newx:
                oldx -= 1
            if oldy < newy:
                oldy += 1
            if oldy > newy:
                oldy -= 1
            # if you meet another peice, the move is illegal
            if self.board[oldy][oldx] is not None:
                return
            
        moves = piece.getPossibleMoves(self.selected_square)
        if (newx, newy) not in moves:
            return

        # TODO: add a check to see your taking your own peice
        if (self.board[newy][newx] is not None) and piece.color == self.board[newy][newx].color:
            return

    def move(self, newx, newy): 
        if self.is_legal_move(newx, newy):
            piece = self.board[self.selected_square[1]][self.selected_square[0]]
            self.board[newy][newx] = piece
            self.board[self.selected_square[1]][self.selected_square[0]] = None
            self.move_counter += 1
            piece.has_moved = True
        return    

    def update(self):
        c = 0
        light_row = False
        window = pygame.display.get_surface() 
        for y, row in enumerate(self.board):
            light_row = not light_row
            for x, column in enumerate(row):
                

                # leading with light
                if light_row:
                    if (c % 2 == 0):
                        window.blit(assets.light_square, (x*globals.grid_size,y*globals.grid_size))  
                    else:
                        window.blit(assets.dark_square, (x*globals.grid_size,y*globals.grid_size))
                else:
                    if (c % 2 == 0):
                        window.blit(assets.dark_square, (x*globals.grid_size,y*globals.grid_size))  
                    else:
                        window.blit(assets.light_square, (x*globals.grid_size,y*globals.grid_size))
                c += 1

                if column is not None:
                    column.show(x,y)
        if self.selected_square is not None:
            pygame.draw.rect(
                window, (255, 0, 0), 
                pygame.Rect(self.selected_square[0]*globals.grid_size, self.selected_square[1]*globals.grid_size, globals.grid_size, globals.grid_size),
                width=1
            )

    
                
                    

