
from class_Game import Game

game = Game()

game.draw_start_screen()
game.started = True
while True:
    game.start()
    game.draw_gameover()
