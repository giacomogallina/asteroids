import math
import pygame

radius = {'big' : 50, 'medium' : 25, 'small' : 15}


def draw_ship(surface, X, Y, D, up, r, g, b):
    pygame.draw.lines(surface, (r, g, b), True, (\
    (X + 10 * math.cos(D), Y  - 10 * math.sin(D)),\
    (X + 10 * math.cos((D + math.pi*3/4)%(2*math.pi)), Y  - 10 * math.sin((D + math.pi*3/4)%(2*math.pi))),\
    (X + 10 * math.cos((D + math.pi*5/4)%(2*math.pi)), Y  - 10 * math.sin((D + math.pi*5/4)%(2*math.pi))),\
    ), 1)
    if up == 'True':
        pygame.draw.lines(surface, (r, g, b), True, (\
            (X - 14 * math.cos(D), \
             Y + 14 * math.sin(D)),\
            (X - 14 * math.cos(D) \
             + 7 * math.cos(D-math.pi/4), \
             Y + 14 * math.sin(D)\
             - 7 * math.sin(D-math.pi/4)),\
            (X - 14 * math.cos(D) \
             + 7 * math.cos(D+math.pi/4), \
             Y + 14 * math.sin(D)\
             - 7 * math.sin(D+math.pi/4))), 1)

def draw_asteroid(surface, X, Y, D, Type):
    global radius
    pygame.draw.circle(surface, (255, 255, 255), (int(X), int(Y)), radius[Type], 1)


def draw_projectile(surface, X, Y, D, r, g, b):
    pygame.draw.circle(surface, (r, g, b), (int(X), int(Y)), 2, 0)
