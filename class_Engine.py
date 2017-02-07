import math, threading, socket
from class_Ship import *


class Engine(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.listeners = []
        self.connections_accepter = Connections_accepter(self)
        self.Ps = []
        self.tick_rate = 250
        self.tick_duration = 1 / self.tick_rate
        self.level_start_tick = -1
        self.tick = 0
        # list of lists like [user, command], where command is
        # ut, lt, rt, st, uf, lf, rf
        self.events = []
        self.status = 'null'
        self.players = {}
        self.level = 0
        self.As = []
        self.window_width = 800
        self.window_height = 800
        self.lifes = 5
        self.points = 0
        self.highscore = 0
        self.acceleration = 1000.0 / (self.tick_rate**2)
        self.friction = 0.8 ** (1.0/self.tick_rate)
        self.rotation_speed = 5.0 / self.tick_rate
        self.projectile_speed = 400.0 / self.tick_rate
        self.asteroid_speed = 200.0 / self.tick_rate
        for i in range(0, 8):
            self.Ps.append(Projectile(self))

    def wait_next_tick(self):
        while time.time() < self.next_tick_time + self.tick_duration:
            time.sleep(0.001)
        a = time.time() - self.next_tick_time
        if a > 1 and self.tick % 250 == 0:
            print('engine back of', a)
        self.next_tick_time += self.tick_duration
        self.tick += 1

    def event_handle(self):
        for i in self.events:
            try:
                # print('event:', i)
                if i[1][1] == 't':
                    value = True
                elif i[1][1] == 'f':
                    value = False
                if i[1][0] == 's':
                    self.players[i[0]].shoot = value
                elif i[1][0] == 'l':
                    self.players[i[0]].left = value
                elif i[1][0] == 'u':
                    self.players[i[0]].up = value
                elif i[1][0] == 'r':
                    self.players[i[0]].right = value
            except(IndexError):
                print('caught an error while processing these events:\n',
                      self.events)
        self.events = []
        # self.status = ''

    def start_level(self, level):
        for i in range(0, self.level * 14):
            self.As.append(Asteroid(self))
        for i in range(0, self.level * 14, 7):
            self.As[i].generate(i)
        self.level_start_tick = -1

    def check_for_level(self):
        for i in self.As:
            if not i.dead:
                return False
        if self.level_start_tick < self.tick:
            self.level_start_tick = self.tick + 2 * self.tick_rate
            self.level += 1
        if self.tick == self.level_start_tick:
            self.start_level(self.level)

    def move(self):
        self.check_for_level()
        for i in self.players:
            self.players[i].move()
            self.players[i].is_destroied()
        for i in self.Ps:
            i.remove()
            if not i.unused():
                i.move()
        for i in self.As:
            i.move()
            i.is_destroied()

    def make_status(self):
        new_status = [0, 0, [], [], [], [], []]
        new_status[1] = self.level
        for i in self.Ps:
            if not i.unused():
                new_status[2].append([i.X, i.Y, i.D, i.color[0],
                                      i.color[1], i.color[2]])

        types = ['big', 'medium', 'small']
        for i in range(len(types)):
            for j in self.As:
                if not j.dead and j.Type == types[i]:
                    new_status[3+i].append([j.X, j.Y, 0])

        for i in self.players.keys():
            s = self.players[i]
            if not s.pulsing or (time.time() - s.pulse_time) % 0.5 <= 0.3:
                new_status[6].append([i, s.X, s.Y, s.D, s.up, s.color[0],
                                      s.color[1], s.color[2]])
        temp_status = str(new_status[0]) + ',' + str(new_status[1])
        for i in new_status[2:]:
            temp_status += ',' + str(len(i))
            for j in i:
                for k in j:
                    temp_status += ',' + str(k)
        self.status = temp_status
        # print(new_status)
        # print(self.status)

    def run(self):
        self.next_tick_time = time.time()
        while True:
            self.event_handle()
            self.wait_next_tick()
            self.move()
            self.make_status()


class Listener(threading.Thread):
    def __init__(self, client, boss):
        threading.Thread.__init__(self)
        self.boss = boss
        self.c, self.addr = client
        self.start()

    def run(self):
        msg = 'Thank you for connecting'
        self.c.send(msg.encode('ascii'))
        print(self.c.recv(1024).decode('ascii'))
        self.boss.players['test'] = Ship(self.boss, (255, 255, 255))
        while True:
            msg = self.c.recv(1024).decode('ascii')
            # print('events received:\n', msg)
            if msg != 'null':
                msg = msg.split(',')
                for i in range(len(msg)//2):
                    self.boss.events.append([msg[2*i], msg[2*i+1]])
            status = self.boss.status.encode('ascii')
            try:
                self.c.send(status)
            except(BrokenPipeError):
                print('client disconnected')
                break
            # print('status sent!')
        self.c.close()


class Connections_accepter(threading.Thread):
    def __init__(self, boss):
        threading.Thread.__init__(self)
        self.boss = boss
        self.s = socket.socket()
        self.s.bind(('192.168.1.8', 12346))
        self.start()

    def run(self):
        while True:
            self.s.listen(5)
            self.boss.listeners.append(Listener(self.s.accept(), self.boss))
