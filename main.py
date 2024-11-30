if __name__ == "__main__":
    import pygame
    import game.constants.globals as globals
    pygame.init()
    pygame.display.set_caption('Chess')
    # TODO: have window be resizable, based on constant values
    window = pygame.display.set_mode((globals.appsize, globals.appsize+70))
    from game.game_states.StateManager import StateManager
    is_running = True
    manager = StateManager()

    while is_running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousepos = pygame.mouse.get_pos()
                gridx, gridy = int(mousepos[0]/globals.grid_size), int(mousepos[1]/globals.grid_size)
                manager.handle_click((gridx, gridy))
            if event.type == pygame.KEYDOWN:
                manager.handle_key_press(event)

        manager.update()
        pygame.display.update()