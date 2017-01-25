
from class_Game import Game

game = Game()

while True:
    game.draw_start_screen()
    game.started = True
    while True:
        game.start()
        replay = game.draw_gameover()
        if not replay:
            break
