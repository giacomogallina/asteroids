
from class_Game import Game

game = Game()

game.draw_start_screen()
while True:
    game.start()
    game.draw_gameover()
