from class_Projectile import Projectile
from class_Asteroid import Asteroid
import math, time, pygame

class Ship:
    D = math.pi/2
    Vx = 0
    Vy = 0
    left = False
    right = False
    up = False
    shoot = False
    pulsing = True

    def __init__(self, boss, color = (255, 255, 255)):
        self.boss = boss
        self.X = boss.window_width/2
        self.Y = boss.window_height/2
        self.color = color
        self.pulse_time = time.time()

    def move(self):
        if self.left:
            self.D = (self.D + self.boss.rotation_speed) % (math.pi * 2)
        if self.right:
            self.D = (self.D - self.boss.rotation_speed) % (math.pi * 2)
        if self.up:
            self.Vx += (self.boss.acceleration / 2 * math.cos(self.D))
            self.Vy -= (self.boss.acceleration / 2 * math.sin(self.D))
        self.Vx *= self.boss.friction
        self.Vy *= self.boss.friction
        self.X = (self.X + self.Vx) % self.boss.window_width
        self.Y = (self.Y + self.Vy) % self.boss.window_height
        if self.up:
            self.Vx += (self.boss.acceleration / 2 * math.cos(self.D))
            self.Vy -= (self.boss.acceleration / 2 * math.sin(self.D))
        if not self.pulsing or (time.time() - self.pulse_time)%0.5 >= 0.2:
            pygame.draw.lines(self.boss.surface, self.color, True, (\
            (self.X + 10 * math.cos(self.D), self.Y  - 10 * math.sin(self.D)),\
            (self.X + 10 * math.cos((self.D + math.pi*3/4)%(2*math.pi)), self.Y  - 10 * math.sin((self.D + math.pi*3/4)%(2*math.pi))),\
            (self.X + 10 * math.cos((self.D + math.pi*5/4)%(2*math.pi)), self.Y  - 10 * math.sin((self.D + math.pi*5/4)%(2*math.pi))),\
            ), 1)
            if self.up:
                pygame.draw.lines(self.boss.surface, self.color, True, (\
                    (self.X - 14 * math.cos(self.D), \
                     self.Y + 14 * math.sin(self.D)),\
                    (self.X - 14 * math.cos(self.D) \
                     + 7 * math.cos(self.D-math.pi/4), \
                     self.Y + 14 * math.sin(self.D)\
                     - 7 * math.sin(self.D-math.pi/4)),\
                    (self.X - 14 * math.cos(self.D) \
                     + 7 * math.cos(self.D+math.pi/4), \
                     self.Y + 14 * math.sin(self.D)\
                     - 7 * math.sin(self.D+math.pi/4))), 1)
        if time.time()-self.pulse_time > 3:
            self.pulsing = False
        if self.shoot:
            self.boss.points -= 1
            for i in self.boss.Ps:
                if i.unused():
                    i.shoot(self.X, self.Y, self.Vx, self.Vy, self.D, self.color)
                    self.shoot = False
                    break

    def is_destroied(self):
        if not self.pulsing:
            for i in self.boss.As:
                if math.hypot(self.X - i.X, self.Y - i.Y) <= i.radius[i.Type] +5:
                    self.pulsing = True
                    self.pulse_time = time.time()
                    self.X = self.boss.window_width/2
                    self.Y = self.boss.window_height/2
                    self.D = math.pi/2
                    self.Vx = 0
                    self.Vy = 0
                    self.boss.lifes -= 1
                    break
            for i in self.boss.Ps:
                if math.hypot(self.X - i.X, self.Y - i.Y) <= 8:
                    self.pulsing = True
                    self.pulse_time = time.time()
                    self.X = self.boss.window_width/2
                    self.Y = self.boss.window_height/2
                    self.D = math.pi/2
                    self.Vx = 0
                    self.Vy = 0
                    self.boss.lifes -= 1
                    break
