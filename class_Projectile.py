import math, time, pygame

class Projectile:
    global window_width, window_height
    X = -10
    Y = -10
    Vx = 0
    Vy = 0
    birth = 0
    color = (0, 0, 0)

    def __init__(self, boss):
        self.boss = boss

    def shoot(self, x, y, Vx, Vy ,D, color):
        self.X = x + 10 * math.cos(D)
        self.Y = y - 10 * math.sin(D)
        self.Vx = self.boss.projectile_speed * math.cos(D) + Vx
        self.Vy = -1 * self.boss.projectile_speed * math.sin(D) + Vy
        self.birth = time.time()
        self.color = color

    def remove(self):
        if time.time() - self.birth > 2:
            self.X = -100
            self.Y = -100
            self.Vx = 0
            self.Vy = 0

    def move(self):
        self.X = (self.X + self.Vx)%self.boss.window_width
        self.Y = (self.Y + self.Vy)%self.boss.window_height
        pygame.draw.circle(self.boss.surface, self.color, \
                           (int(self.X), int(self.Y)), 2, 0)

    def unused(self):
        if self.X == -100 and self.Y == -100:
            return True
        else:
            return False
