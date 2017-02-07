# -*- coding: utf-8 -*-
import pygame, time, sys, socket, threading, logging
from class_Ship import *
from class_Settings_window import *
# from class_Engine import Engine
from gui_objects import *

pygame.font.init()
white = (255, 255, 255)


class Game:
    points_font = pygame.font.Font(None, 36)
    level_font = pygame.font.Font(None, 100)
    start_font = pygame.font.Font(None, 200)
    started = False
    Ps = []
    username = 'test'
    events_queue = ''
    status = [0, 0, [], [], [], [], []]
    auto_move = False

    def __init__(self):
        global highscore, window_width, window_height, framerate, \
               players, settings_file, surface
        self.import_settings()
        self.surface = pygame.display.set_mode((self.window_width,
                                                self.window_height))
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
        if a > 1 and self.frame % 100 == 0:
            print('gui back of', a)
        self.frame_time += self.frame_duration
        self.frame += 1

    def events(self):
        self.events_queue = ''
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.events_queue += self.username + ',lt,'
                elif event.key == pygame.K_RIGHT:
                    self.events_queue += self.username + ',rt,'
                elif event.key == pygame.K_UP:
                    self.events_queue += self.username + ',ut,'
                elif event.key == pygame.K_SPACE:
                    self.events_queue += self.username + ',st,'
                elif event.key == pygame.K_ESCAPE:
                    self.draw_options()
                elif event.key == pygame.K_TAB:
                    self.draw_players()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.events_queue += self.username + ',lf,'
                elif event.key == pygame.K_RIGHT:
                    self.events_queue += self.username + ',rf,'
                elif event.key == pygame.K_UP:
                    self.events_queue += self.username + ',uf,'
        if self.events_queue == '':
            self.events_queue = 'null'
        if self.auto_move:
            self.events_queue = 'test,rt,'
            if self.frame % 20 == 0:
                self.events_queue += 'test,st,'

    def connect(self, server, port):
        self.communicator.s = socket.socket()
        self.communicator.s.connect((server, port))
        print(self.communicator.s.recv(1024).decode('ascii'))
        msg = 'connection working!'
        self.communicator.s.send(msg.encode('ascii'))
        time.sleep(0.1)
        self.communicator.start()
        # name = 'test'
        # self.s.send(name.encode('ascii'))

    def check_for_level(self):
        if self.level == self.old_level and \
                self.frame > self.level_start_frame:
            return False
        if self.level_start_frame < self.frame:
            self.level_start_frame = self.frame + 2 * self.framerate
        lc = 255 * (1-(math.fabs(self.level_start_frame - self.framerate
                                 - self.frame)/self.framerate))
        level_box = self.level_font.render('Level ' + str(self.level),
                                           0, (lc, lc, lc))
        size = self.level_font.size('Level ' + str(self.level))
        self.surface.blit(level_box, ((self.window_width - size[0])/2,
                                      (self.window_height - size[1])/2))

    def draw_points(self):
        points_box = self.points_font.render(str(self.points), 0,
                                             (255, 255, 255))
        self.surface.blit(points_box,
                          (self.window_width - self.points_font.size
                           (str(self.points))[0] - 10, 10))

    def draw_lifes(self):
        lifes_box = self.points_font.render('Δ x ' + str(self.lifes), 0,
                                            (255, 255, 255))
        self.surface.blit(lifes_box, (10, 10))

    def draw_highscore(self):
        highscore_box = self.points_font.render('HIGHSCORE: ' +
                                                str(self.highscore),
                                                0, (255, 255, 255))
        self.surface.blit(highscore_box, ((self.window_width -
                                           self.points_font.size
                                           ('HIGHSCORE: ' +
                                            str(self.highscore))[0])/2, 10))

    def draw_options(self):
        # print("options hasn't been implemented yet")

        s = Settings_window(self)

        self.frame_time = time.time()

    def draw_players(self):
        print('test')

    def quit(self):
        self.communicator.keep = False
        self.communicate.set()
        sys.exit()

    def move(self):
        self.check_for_level()
        self.old_level = self.level
        try:
            self.level = self.status[1]
            for i in self.status[2]:
                # if not i.unused():
                draw_projectile(self.surface, float(i[0]), float(i[1]),
                                float(i[2]), int(i[3]), int(i[4]), int(i[5]))
            for i in self.status[3]:
                draw_asteroid(self.surface, float(i[0]), float(i[1]),
                              float(i[2]), 'big')
            for i in self.status[4]:
                draw_asteroid(self.surface, float(i[0]), float(i[1]),
                              float(i[2]), 'medium')
            for i in self.status[5]:
                draw_asteroid(self.surface, float(i[0]), float(i[1]),
                              float(i[2]), 'small')
            for i in self.status[6]:
                draw_ship(self.surface, float(i[1]), float(i[2]), float(i[3]),
                          i[4], int(i[5]), int(i[6]), int(i[7]))
        except(IndexError, ValueError):
            logging.error('cought an error while processing this status \
                          (move function):\n' +
                          str(self.communicator.temp_s) + '\n' +
                          str(self.status))
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

    def draw_gameover(self, gc, size1, size2):
        c = (gc, gc, gc)
        box_1 = self.level_font.render('GAME OVER', 0, )
        self.surface.blit(box_1, ((self.window_width - size1[0])/2,
                                  (self.window_height - size1[1])/2))
        box_2 = self.points_font.render('press SPACE to restart', 0, c)
        self.surface.blit(box_2, ((self.window_width - size2[0])/2,
                                  (self.window_height - size2[1])/2+50))

    def make_gameover(self):
        death_frame = self.frame
        size1 = self.level_font.size('GAME OVER')
        size2 = self.points_font.size('press SPACE to restart')
        while True:
            self.wait_next_frame()
            gc = 255 * (self.frame - death_frame)/self.framerate
            self.surface.fill((0, 0, 0))
            self.draw_gameover(gc, size1, size2)
            pygame.display.update()
            if self.frame == death_frame + self.framerate:
                break
        while True:
            self.surface.fill((0, 0, 0))
            self.draw_gameover(gc, size1, size2)
            pygame.display.update()
            if self.wait_for_space():
                break
        self.frame_time = time.time()
        while True:
            self.wait_next_frame()
            gc = 255 * (1-(self.frame - death_frame - self.framerate) * 1.0 /
                        self.framerate) + 1
            self.surface.fill((0, 0, 0))
            self.draw_gameover(gc, size1, size2)
            pygame.display.update()
            if self.frame == death_frame + 2 * self.framerate:
                break

        return True

    def start(self):
        self.frame_time = time.time()
        self.frame = 0
        self.level_start_frame = 2 * self.framerate
        self.points = 0
        self.lifes = 3
        self.draw_start_screen()
        logging.basicConfig(filename='game.log', level=logging.DEBUG)
        logging.info('\nnew game started at ' + str(time.time()) + '\n')
        self.communicate = threading.Event()
        self.communicator = Communicator(self)
        self.connect('192.168.1.8', 12346)
        self.level = 0
        self.old_level = 0
        while True:
            self.communicate.set()
            # print('communicate set')
            self.wait_next_frame()
            # print('done!')
            self.events()
            self.surface.fill((0, 0, 0))
            self.move()
            # print('drawing...')
            if self.lifes <= 0:
                break

    def draw_start_screen(self):
        size1 = self.start_font.size('ASTEROIDS')
        size2 = self.points_font.size('press SPACE to start')
        size3 = self.points_font.size('a game by Giacomo Gallina')
        while True:
            self.surface.fill((0, 0, 0))
            box_1 = self.start_font.render('ASTEROIDS', 0, white)
            self.surface.blit(box_1, ((self.window_width - size1[0])/2,
                                      (self.window_height - size1[1])/2 - 100))
            box_2 = self.points_font.render('press SPACE to start', 0, white)
            self.surface.blit(box_2, ((self.window_width - size2[0])/2,
                                      (self.window_height - size2[1])/2+100))
            box_3 = self.points_font.render('a game by Giacomo Gallina', 0,
                                            white)
            self.surface.blit(box_3, ((self.window_width - size3[0])/2,
                                      (self.window_height - size3[1])/2))
            pygame.display.update()
            if self.wait_for_space():
                break
        self.started = True


class Communicator(threading.Thread):
    def __init__(self, boss):
        threading.Thread.__init__(self)
        self.boss = boss

    def run(self):
        self.keep = True
        while True:
            self.boss.communicate.wait()
            if not self.keep:
                break
            self.boss.communicate.clear()
            # print('communicating...')
            events = 'null'
            if self.boss.events_queue != 'null':
                events = self.boss.events_queue[:-1]
            # print(self.events_queue)
            self.s.send(events.encode('ascii'))
            # print('events sent!')
            self.temp_s = self.s.recv(1048576).decode('ascii')
            # print('status received!')
            if self.temp_s != 'null':
                self.temp_s = self.temp_s.split(',')
                # print(temp_s)
                self.boss.status = []
                try:
                    self.boss.status.append(int(self.temp_s[0]))
                    self.boss.status.append(int(self.temp_s[1]))
                    for i in range(5):
                        self.boss.status.append([])
                    x = 3
                    p = int(self.temp_s[x-1])
                    for i in range(p):
                        self.boss.status[2].append(self.temp_s[x+6*i:x+6*i+6])
                    x += 6 * p + 1
                    ba = int(self.temp_s[x-1])
                    for i in range(ba):
                        self.boss.status[3].append(self.temp_s[x+3*i:x+3*i+3])
                    x += 3 * ba + 1
                    ma = int(self.temp_s[x-1])
                    for i in range(ma):
                        self.boss.status[4].append(self.temp_s[x+3*i:x+3*i+3])
                    x += 3 * ma + 1
                    sa = int(self.temp_s[x-1])
                    for i in range(sa):
                        self.boss.status[5].append(self.temp_s[x+3*i:x+3*i+3])
                    x += 3 * sa + 1
                    s = int(self.temp_s[x-1])
                    for i in range(s):
                        self.boss.status[6].append(self.temp_s[x+8*i:x+8*i+8])
                except(IndexError):
                    logging.error('cought an error while processing this status\
                                   (communicator):\n' + str(self.temp_s))
            # print(self.status)
