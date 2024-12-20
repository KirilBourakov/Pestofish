import pygame
from game.game_states.AbstractState import AbstractState
import game.assets.assets as assets
import game.constants.globals as globals

class EndState(AbstractState):
    def enter(self, args):
        self.conclusion = args[0]
        self.ready_to_exit_bool = False
    
    def handle_click(self, x, y):
        self.ready_to_exit_bool = True

    def handle_key_press(self, event):
        self.ready_to_exit_bool = True
    
    def ready_to_exit(self):
        return self.ready_to_exit_bool
    
    def exit(self):
        return ["start", ""]
    
    def update(self):
        window = pygame.display.get_surface() 
        window.fill("black")

        render = assets.text_large.render(self.conclusion, False, "white")
        x,y = assets.text_large.size(self.conclusion)

        window.blit(render, (int((globals.appsize-x)/2), int((globals.appsize-y)/2)))