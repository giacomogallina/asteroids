from class_Projectile import Projectile
from class_Asteroid import Asteroid
import math, time

class Ship:
    D = math.pi/2
    Vx = 0
    Vy = 0
    left = False
    right = False
    up = 0
    shoot = False
    pulsing = True

    def __init__(self, boss, name, color=(255, 255, 255)):
        self.boss = boss
        self.name = name
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
        if time.time()-self.pulse_time > 3:
            self.pulsing = False
        if self.shoot:
            self.boss.points -= 1
            for i in self.boss.Ps:
                if i.unused():
                    i.shoot(self.X, self.Y, self.Vx, self.Vy, self.D,
                            self.color)
                    self.shoot = False
                    break

    def is_destroied(self):
        if not self.pulsing:
            for i in self.boss.As:
                if not i.dead:
                    a = self.X - i.X
                    b = self.Y - i.Y
                    c = i.radius[i.Type] + 5
                    if b <= c:
                        if a**2 + b**2 <= c**2:
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
                if not i.unused():
                    a = self.X - i.X
                    b = self.Y - i.Y
                    if b <= 8:
                        if a**2 + b**2 <= 8**2:
                            self.pulsing = True
                            self.pulse_time = time.time()
                            self.X = self.boss.window_width/2
                            self.Y = self.boss.window_height/2
                            self.D = math.pi/2
                            self.Vx = 0
                            self.Vy = 0
                            self.boss.lifes -= 1
                            break
