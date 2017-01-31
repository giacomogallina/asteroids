# -*- coding: utf-8 -*-
import pygame, time, sys, socket
from class_Ship import *
from class_Settings_window import *
#from class_Engine import Engine
from gui_objects import *

pygame.font.init()

class Game:
    points_font = pygame.font.Font(None, 36)
    level_font = pygame.font.Font(None, 100)
    start_font = pygame.font.Font(None, 200)
    started = False
    Ps = []
    username = 'test'
    events_queue = ''
    status = []


    def __init__(self):
        global highscore, window_width, window_height, framerate, players, settings_file, surface
        self.import_settings()
        self.surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('ASTEROIDS / Game')
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
        a = time.time() - self.frame_time
        if a > 1 and self.frame%100 == 0:
            print('gui back of', a)
        self.frame_time += self.frame_duration
        self.frame += 1

    def events(self):
        self.events_queue = ''
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.events_queue += self.username + ',lt,'
                if event.key == pygame.K_RIGHT:
                    self.events_queue += self.username + ',rt,'
                if event.key == pygame.K_UP:
                    self.events_queue += self.username + ',ut,'
                # if self.players == 2:
                #     if event.key == pygame.K_a:
                #         self.shuttle_2.left = True
                #     if event.key == pygame.K_d:
                #         self.shuttle_2.right = True
                #     if event.key == pygame.K_w:
                #         self.shuttle_2.up = True
                #     if event.key == pygame.K_RCTRL:
                #         self.shuttle_1.shoot = True
                #     if event.key == pygame.K_LCTRL:
                #         self.shuttle_2.shoot = True
                # else:
                if event.key == pygame.K_SPACE:
                    self.events_queue += self.username + ',st,'

                if event.key == pygame.K_ESCAPE:
                    self.draw_options()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.events_queue += self.username + ',lf,'
                if event.key == pygame.K_RIGHT:
                    self.events_queue += self.username + ',rf,'
                if event.key == pygame.K_UP:
                    self.events_queue += self.username + ',uf,'
                # if self.players == 2:
                #     if event.key == pygame.K_a:
                #         self.shuttle_2.left = False
                #     if event.key == pygame.K_d:
                #         self.shuttle_2.right = False
                #     if event.key == pygame.K_w:
                #         self.engine.shuttle_2.up = False
        if self.events_queue == '':
            self.events_queue = 'null'

    def connect(self, server, port):
        self.s = socket.socket()
        self.s.connect((server, port))
        print(self.s.recv(1024).decode('ascii'))
        msg = 'connection working!'
        self.s.send(msg.encode('ascii'))
        time.sleep(0.1)
        #name = 'test'
        #self.s.send(name.encode('ascii'))

    def communicate(self):
        if self.events_queue != 'null':
            self.events_queue = self.events_queue[:-1]
        #print(self.events_queue)
        self.s.send(self.events_queue.encode('ascii'))
        #print('events sent!')
        temp_status = self.s.recv(1024).decode('ascii')
        #print('status received!')
        if temp_status != 'null':
            temp_status = temp_status.split(',')
            print(temp_status)
            self.status = []
            self.status.append(int(temp_status[0]))
            self.status.append(int(temp_status[1]))
            for i in range(5):
                self.status.append([])
            x = 3
            p = int(temp_status[x-1])
            for i in range(p):
                self.status[2].append(temp_status[x+6*i:x+6*i+6])
            x += 6 * p + 1
            ba = int(temp_status[x-1])
            for i in range(ba):
                self.status[3].append(temp_status[x+3*i:x+3*i+3])
            x += 3 * ba + 1
            ma = int(temp_status[x-1])
            for i in range(ma):
                self.status[4].append(temp_status[x+3*i:x+3*i+3])
            x += 3 * ma + 1
            sa = int(temp_status[x-1])
            for i in range(sa):
                self.status[5].append(temp_status[x+3*i:x+3*i+3])
            x += 3 * sa + 1
            s = int(temp_status[x-1])
            for i in range(s):
                self.status[6].append(temp_status[x+8*i:x+8*i+8])

        #print(self.status)

    def check_for_level(self):
        if self.level == self.old_level and self.frame > self.level_start_frame:
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
        #self.check_for_level()
        self.old_level = self.level
        self.level = self.status[1]

        for i in self.status[2]:
            #if not i.unused():
            draw_projectile(self.surface, float(i[0]), float(i[1]), float(i[2]), int(i[3]), int(i[4]), int(i[5]))
        for i in self.status[3]:
            draw_asteroid(self.surface, float(i[0]), float(i[1]), float(i[2]), 'big')
        for i in self.status[4]:
            draw_asteroid(self.surface, float(i[0]), float(i[1]), float(i[2]), 'medium')
        for i in self.status[5]:
            draw_asteroid(self.surface, float(i[0]), float(i[1]), float(i[2]), 'small')
        for i in self.status[6]:
            draw_ship(self.surface, float(i[1]), float(i[2]), float(i[3]), i[4], int(i[5]), int(i[6]), int(i[7]))
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
        #self.engine = Engine()
        #self.engine.players[self.username] = Ship(self.engine, (255, 255, 255))
        self.frame = 0
        self.level_start_frame  = 2 * self.framerate
        self.points = 0
        self.lifes = 3
        #self.engine.start_level(1)
        self.draw_start_screen()
        #self.engine.start()
        self.connect('192.168.1.8', 12345)
        self.level = 0
        while True:
            self.wait_next_frame()
            #print('done!')
            self.events()
            self.communicate()
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
