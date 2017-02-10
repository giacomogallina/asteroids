import math, random, pygame

class Asteroid:
    global window_width, window_height, points, highscore, settings_file
    mass = {'big' : 4, 'medium' : 2, 'small' : 1}
    radius = {'big' : 50, 'medium' : 25, 'small' : 15}
    Type = 'big'
    X = -100
    Y = -100
    D = 0
    Vx = 0
    Vy = 0
    dead = True
    list_position = 0

    def __init__(self, boss):
        self.boss = boss

    def generate(self, position):
        self.X = (random.randint(0, self.boss.window_width // 2) - self.boss.window_width/4) % self.boss.window_width
        self.Y = (random.randint(0, self.boss.window_height // 2) - self.boss.window_height/4) % self.boss.window_height
        self.Vx = (random.random() * 2 -1) * self.boss.asteroid_speed
        self.Vy = (self.boss.asteroid_speed ** 2 - self.Vx ** 2) ** 0.5
        self.dead = False
        self.list_position = position

    def move(self):
        if not self.dead:
            self.X = (self.X + self.Vx)%self.boss.window_width
            self.Y = (self.Y + self.Vy)%self.boss.window_height

    def is_destroied(self):
        if not self.dead:
            for i in self.boss.Ps:
                if not i.unused():
                    if math.hypot(self.X - i.X, self.Y - i.Y) <= self.radius[self.Type]:
                        self.dead = True
                        i.X = -100
                        i.Y = -100
                        if self.Type == 'big'or self.Type == 'medium':
                            if self.Type == 'big':
                                son1 = self.boss.As[self.list_position + 1]
                                son2 = self.boss.As[self.list_position + 4]
                                son1.generate(self.list_position + 1)
                                son2.generate(self.list_position + 4)
                                self.boss.points += 20
                            elif self.Type == 'medium':
                                son1 = self.boss.As[self.list_position + 1]
                                son2 = self.boss.As[self.list_position + 2]
                                son1.generate(self.list_position + 1)
                                son2.generate(self.list_position + 2)
                                self.boss.points += 50
                            son1.X = self.X
                            son1.Y = self.Y
                            son2.X = self.X
                            son2.Y = self.Y
                            alpha = random.random()
                            sin_alpha = math.sin(alpha)
                            cos_alpha = math.cos(alpha)
                            son1.Vx = self.Vx * cos_alpha - self.Vy * sin_alpha
                            son1.Vy = self.Vx * sin_alpha + self.Vy * cos_alpha
                            sin_alpha = math.sin(-alpha)
                            cos_alpha = math.cos(-alpha)
                            son2.Vx = self.Vx * cos_alpha - self.Vy * sin_alpha
                            son2.Vy = self.Vx * sin_alpha + self.Vy * cos_alpha
                            if self.Type == 'big':
                                son1.Type = 'medium'
                                son2.Type = 'medium'
                            elif self.Type == 'medium':
                                son1.Type = 'small'
                                son2.Type = 'small'
                        else:
                            self.boss.points += 100
                        self.X = -100
                        self.Y = -100
                        if self.boss.points > self.boss.highscore:
                            self.boss.highscore = self.boss.points
