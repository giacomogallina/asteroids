# -*- coding: utf-8 -*-
import pygame, time, sys
from class_Ship import *
from class_Settings_window import *

pygame.font.init()

class Game:
    points_font = pygame.font.Font(None, 36)
    level_font = pygame.font.Font(None, 100)
    start_font = pygame.font.Font(None, 200)
    started = False
    Ps = []

    def __init__(self):
        global highscore, window_width, window_height, framerate, players, settings_file, surface
        self.import_settings()
        self.surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('ASTEROIDS / Game')
        self.acceleration = 1000.0 / (self.framerate**2)
        self.friction = 0.8 ** (1.0/self.framerate)
        self.rotation_speed = 5.0 / self.framerate
        self.projectile_speed = 400.0 / self.framerate
        self.asteroid_speed = 200.0 / self.framerate
        self.frame_time = time.time()
        self.frame_duration = 1.0 / self.framerate
        self.frame = 0
        for i in range(0, 8):
            self.Ps.append(Projectile(self))

    def import_settings(self):
        try:
            settings_file = open('settings.txt', 'r+')
        except:
            create = open('settings.txt', 'w')
            create.write('0\n600\n480\n30\n1')
            create.close()
            settings_file = open('settings.txt', 'r+')

        settings = settings_file.readlines()
        settings_file.close()
        self.highscore = int(settings[0])
        self.window_width = int(settings[1])
        self.window_height = int(settings[2])
        self.framerate = int(settings[3])
        self.players = int(settings[4])

    def wait_next_frame(self):
        while time.time() < self.frame_time + self.frame_duration:
            time.sleep(0.001)
        self.frame_time += self.frame_duration
        self.frame += 1

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.shuttle_1.left = True
                if event.key == pygame.K_RIGHT:
                    self.shuttle_1.right = True
                if event.key == pygame.K_UP:
                    self.shuttle_1.up = True
                if self.players == 2:
                    if event.key == pygame.K_a:
                        self.shuttle_2.left = True
                    if event.key == pygame.K_d:
                        self.shuttle_2.right = True
                    if event.key == pygame.K_w:
                        self.shuttle_2.up = True
                    if event.key == pygame.K_RCTRL:
                        self.shuttle_1.shoot = True
                    if event.key == pygame.K_LCTRL:
                        self.shuttle_2.shoot = True
                else:
                    if event.key == pygame.K_SPACE:
                        self.shuttle_1.shoot = True

                if event.key == pygame.K_ESCAPE:
                    self.draw_options()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.shuttle_1.left = False
                if event.key == pygame.K_RIGHT:
                    self.shuttle_1.right = False
                if event.key == pygame.K_UP:
                    self.shuttle_1.up = False
                if self.players == 2:
                    if event.key == pygame.K_a:
                        self.shuttle_2.left = False
                    if event.key == pygame.K_d:
                        self.shuttle_2.right = False
                    if event.key == pygame.K_w:
                        self.shuttle_2.up = False

    def start_level(self, level):
        for i in range(0, self.level * 14):
            self.As.append(Asteroid(self))
        for i in range(0, self.level * 14, 7):
            self.As[i].generate(i)
        self.level_start_frame = -1

    def check_for_level(self):
        for i in self.As:
            if i.dead == False:
                return False
        if self.level_start_frame < self.frame:
            self.level_start_frame = self.frame + 2 * self.framerate
        lc = 255 * (1-(math.fabs(self.level_start_frame - self.framerate \
                                 -self.frame)/self.framerate))
        level_box = self.level_font.render('Level ' + str(self.level+1), \
                                           0, (lc, lc, lc))
        self.surface.blit(level_box, ((self.window_width - \
                                       self.level_font.size\
                                       ('Level ' + str(self.level))[0])/2, \
                                      (self.window_height - self.level_font.size\
                                       ('Level ' + str(self.level))[1])/2))
        if self.frame == self.level_start_frame:
            self.level +=1
            self.start_level(self.level)

    def draw_points(self):
        points_box = self.points_font.render(str(self.points), 0,\
                                             (255, 255, 255))
        self.surface.blit(points_box, \
                          (self.window_width - self.points_font.size\
                          (str(self.points))[0] - 10, 10))

    def draw_lifes(self):
        lifes_box = self.points_font.render('Δ x ' + str(self.lifes), 0, \
                                            (255, 255, 255))
        self.surface.blit(lifes_box, (10, 10))

    def draw_highscore(self):
        highscore_box = self.points_font.render('HIGHSCORE: ' + \
                                                str(self.highscore),\
                                                0, (255, 255, 255))
        self.surface.blit(highscore_box, ((self.window_width - \
                                           self.points_font.size\
                                           ('HIGHSCORE: ' + \
                                            str(self.highscore))[0])/2, 10))

    def draw_options(self):
        #print("options hasn't been implemented yet")

        s = Settings_window(self)

        self.frame_time = time.time()

    def move(self):
        self.check_for_level()
        self.shuttle_1.move()
        self.shuttle_1.is_destroied()
        if self.players == 2:
            self.shuttle_2.move()
            self.shuttle_2.is_destroied()
        for i in self.Ps:
            i.remove()
            if not i.unused():
                i.move()
        for i in self.As:
            i.move()
            i.is_destroied()
        self.draw_points()
        self.draw_lifes()
        self.draw_highscore()
        pygame.display.update()

    def wait_for_space(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.draw_options()
        time.sleep(0.01)

    def draw_gameover(self):
        death_frame = self.frame

        while True:
            self.wait_next_frame()
            gc = 255 * (self.frame - death_frame)/self.framerate
            self.surface.fill((0, 0, 0))
            gameover_box_1 = self.level_font.render('GAME OVER', \
                                                    0, (gc, gc, gc))
            self.surface.blit(gameover_box_1, ((self.window_width - self.level_font.size\
                                           ('GAME OVER')[0])/2, \
                                          (self.window_height - self.level_font.size\
                                           ('GAME OVER')[1])/2))
            gameover_box_2 = self.points_font.render('press SPACE to restart', \
                                                     0, (gc, gc, gc))
            self.surface.blit(gameover_box_2, ((self.window_width - self.points_font.size\
                                           ('press SPACE to restart')[0])/2, \
                                          (self.window_height - self.points_font.size\
                                           ('press SPACE to restart')[1])/2+50))
            pygame.display.update()
            if self.frame == death_frame + self.framerate:
                break
        while True:
            self.surface.fill((0, 0, 0))
            gameover_box_1 = self.level_font.render('GAME OVER',\
                                                    0, (gc, gc, gc))
            self.surface.blit(gameover_box_1, \
                         ((self.window_width - self.level_font.size\
                           ('GAME OVER')[0])/2, \
                          (self.window_height - self.level_font.size\
                           ('GAME OVER')[1])/2))
            gameover_box_2 = self.points_font.render('press SPACE to restart', \
                                                     0, (gc, gc, gc))
            self.surface.blit(gameover_box_2, \
                         ((self.window_width - self.points_font.size\
                           ('press SPACE to restart')[0])/2, \
                          (self.window_height - self.points_font.size\
                           ('press SPACE to restart')[1])/2+50))
            pygame.display.update()
            if self.wait_for_space():
                break
        self.frame_time = time.time()
        while True:
            self.wait_next_frame()
            gc = 255 * (1-(self.frame - death_frame - self.framerate)*1.0/self.framerate) +1
            self.surface.fill((0, 0, 0))
            gameover_box_1 = self.level_font.render('GAME OVER', \
                                                    0, (gc, gc, gc))
            self.surface.blit(gameover_box_1, \
                         ((self.window_width - self.level_font.size\
                           ('GAME OVER')[0])/2, \
                          (self.window_height - self.level_font.size\
                           ('GAME OVER')[1])/2))
            gameover_box_2 = self.points_font.render('press SPACE to restart', \
                                                     0, (gc, gc, gc))
            self.surface.blit(gameover_box_2, \
                         ((self.window_width - self.points_font.size\
                           ('press SPACE to restart')[0])/2,\
                          (self.window_height - self.points_font.size\
                           ('press SPACE to restart')[1])/2+50))
            pygame.display.update()
            if self.frame == death_frame + 2*self.framerate:
                break

        return True

    def start(self):
        self.frame_time = time.time()
        if self.players == 2:
            self.shuttle_1 = Ship(self, (0, 255, 0))
            self.shuttle_2 = Ship(self, (255, 0, 0))
        else:
            self.shuttle_1 = Ship(self)
        self.level = 0
        self.frame = 0
        self.level_start_frame  = 2 * self.framerate
        self.points = 0
        self.As = []
        if self.players == 2:
            self.lifes = 5
        else:
            self.lifes = 3
        self.start_level(self.level)
        while True:
            self.wait_next_frame()
            self.events()
            self.surface.fill((0, 0, 0))
            self.move()
            if self.lifes <= 0:
                break

    def draw_start_screen(self):
        while True:
            self.surface.fill((0, 0, 0))
            start_box_1 = self.start_font.render('ASTEROIDS', \
                                                 0, (255, 255, 255))
            self.surface.blit(start_box_1, ((self.window_width - self.start_font.size\
                                        ('ASTEROIDS')[0])/2, \
                                       (self.window_height - self.start_font.size\
                                        ('ASTEROIDS')[1])/2 - 100))
            gameover_box_2 = self.points_font.render('press SPACE to start', \
                                                     0, (255, 255, 255))
            self.surface.blit(gameover_box_2, ((self.window_width - self.points_font.size\
                                           ('press SPACE to start')[0])/2, \
                                          (self.window_height - self.points_font.size\
                                           ('press SPACE to start')[1])/2+100))
            credits_box = self.points_font.render('a game by Giacomo Gallina', \
                                                  0, (255, 255, 255))
            self.surface.blit(credits_box, ((self.window_width - self.points_font.size\
                                        ('a game by Giacomo Gallina')[0])/2, \
                                       (self.window_height - self.points_font.size\
                                        ('a game by Giacomo Gallina')[1])/2))
            pygame.display.update()
            if self.wait_for_space():
                break
        self.started = True
