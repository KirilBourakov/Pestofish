import pygame
import constants.globals as globals

class Abstract_Piece():
    def __init__(self, type, asset, moveset, color, hops=False):
        self.type = type
        self.asset = asset
        self.moveset = moveset
        self.has_moved = False
        self.hops = hops
        self.color = color

    def getPossibleMoves(self, pos):
        moves_list = []
        for move in self.moveset:
            new_pos = (pos[0] + move[0], pos[1] + move[1])
            if (new_pos[0] >= 0) and (new_pos[1] >= 0) and (new_pos[0] <= 7) and (new_pos[1] <= 7):   
                if len(move) == 3:
                    moves_list.append(new_pos + (move[2],))
                else:
                    moves_list.append(new_pos,)
        return moves_list
    
    def get_legal_moves(self, board_obj):
        piece = board_obj.board[board_obj.selected_square[1]][board_obj.selected_square[0]]
        moves = piece.getPossibleMoves(board_obj.selected_square)
        oldx, oldy = board_obj.selected_square

        king_pos = board_obj.get_king_pos(board_obj.get_turn())    

        # given all possibly legal moves, loop over and remove illegal ones
        purged_moves = []
        for move in moves:
            legal = True

            # certain moves come with functional conditions. If the move does so, make sure the conditions are met
            if (len(move) == 3):
                newx, newy, func = move
                possible = func(old_position=board_obj.selected_square, color=piece.color, new_position=(newx, newy), board=board_obj.board, move_num=board_obj.move_counter)
                if (not possible[0]):
                    continue
                move = (newx, newy, possible[1])
            else:
                newx, newy = move
            
            x_walker, y_walker = oldx, oldy
            # This checks that there is nothing blocking you from moving to that square
            while (abs(x_walker-newx) > 1 or abs(y_walker-newy) > 1) and piece.hops == False:
                # walk across, taking the same path as the peice.  
                if x_walker < newx:
                    x_walker += 1
                if x_walker > newx:
                    x_walker -= 1
                if y_walker < newy:
                    y_walker += 1
                if y_walker > newy:
                    y_walker -= 1
                # if you meet another peice, the move is illegal
                board_square_not_empty = board_obj.board[y_walker][x_walker] is not None
                if board_square_not_empty:
                    not_occupied_by_en_passent = board_obj.board[y_walker][x_walker].type != globals.EN_PASSENT_FLAG
                    if not_occupied_by_en_passent:
                        legal = False
        
            if (board_obj.board[newy][newx] is not None) and (piece.color == board_obj.board[newy][newx].color) and (board_obj.board[newy][newx].type != globals.EN_PASSENT_FLAG):
                continue
            
            if legal: 
                purged_moves.append(move)
                       
        return purged_moves

    def show(self, x, y):
        window = pygame.display.get_surface()
        window.blit(self.asset, (x*globals.grid_size+(globals.resize_num/2), y*globals.grid_size+(globals.resize_num/2)))
