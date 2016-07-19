import math, time, sys, pygame, random

pygame.init()
pygame.font.init()

def import_settings():
    global highscore, window_width, window_height, framerate, players, settings_file, surface
    try:
        settings_file = open('settings.txt', 'r+')
    except:
        create = open('settings.txt', 'w')
        create.write('0\n600\n480\n30\n1')
        create.close()
        settings_file = open('settings.txt', 'r+')
    highscore = int(settings_file.readlines()[0])
    settings_file.close()
    settings_file = open('settings.txt', 'r+')
    window_width = int(settings_file.readlines()[1])
    settings_file.close()
    settings_file = open('settings.txt', 'r+')
    window_height = int(settings_file.readlines()[2])
    settings_file.close()
    settings_file = open('settings.txt', 'r+')
    framerate = int(settings_file.readlines()[3])
    settings_file.close()
    settings_file = open('settings.txt', 'r+')
    players = int(settings_file.readlines()[4])
    settings_file.close()
    surface = pygame.display.set_mode((window_width, window_height))

import_settings()

pygame.display.set_caption('Asteroids')
acceleration = 1000.0 / (framerate**2)
#print(acceleration)
friction = 0.8 ** (1.0/framerate)
rotation_speed = 5.0 / framerate
projectile_speed = 400.0 / framerate
asteroid_speed = 200.0 / framerate
frame_time = time.time()
frame_duration = 1.0 / framerate
frame = 0

def wait_next_frame():
    global frame_time, frame_duration, frame
    while time.time() < frame_time + frame_duration:
        time.sleep(0.001)
    frame_time += frame_duration
    frame += 1

def events():
    global left, right, up, shoot
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shuttle_1.left = True
            if event.key == pygame.K_RIGHT:
                shuttle_1.right = True
            if event.key == pygame.K_UP:
                shuttle_1.up = True
            if event.key == pygame.K_a:
                shuttle_2.left = True
            if event.key == pygame.K_d:
                shuttle_2.right = True
            if event.key == pygame.K_w:
                shuttle_2.up = True
            if players == 2:
                if event.key == pygame.K_RCTRL:
                    shuttle_1.shoot = True
                if event.key == pygame.K_LCTRL:
                    shuttle_2.shoot = True
            else:
                if event.key == pygame.K_SPACE:
                    shuttle_1.shoot = True

            if event.key == pygame.K_ESCAPE:
                draw_options()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                shuttle_1.left = False
            if event.key == pygame.K_RIGHT:
                shuttle_1.right = False
            if event.key == pygame.K_UP:
                shuttle_1.up = False
            if event.key == pygame.K_a:
                shuttle_2.left = False
            if event.key == pygame.K_d:
                shuttle_2.right = False
            if event.key == pygame.K_w:
                shuttle_2.up = False

class projectiles:
    global window_width, window_height
    X = -10
    Y = -10
    Vx = 0
    Vy = 0
    birth = 0
    color = (0, 0, 0)

    def shoot(self, x, y, Vx, Vy ,D, color):
        self.X = x + 10 * math.cos(D)
        self.Y = y - 10 * math.sin(D)
        self.Vx = projectile_speed * math.cos(D) + Vx
        self.Vy = -1 * projectile_speed * math.sin(D) + Vy
        self.birth = time.time()
        self.color = color

    def remove(self):
        if time.time() - self.birth > 2:
            self.X = -100
            self.Y = -100
            self.Vx = 0
            self.Vy = 0

    def move(self):
        self.X = (self.X + self.Vx)%window_width
        self.Y = (self.Y + self.Vy)%window_height
        pygame.draw.circle(surface, self.color, (int(self.X), int(self.Y)), 2, 0)

    def unused(self):
        if self.X == -100 and self.Y == -100:
            return True
        else:
            return False

Ps = []
for i in range(0, 8):
    Ps.append(projectiles())

class asteroids:
    global window_width, window_height, points, highscore, settings_file
    mass = {'big' : 4, 'medium' : 2, 'small' : 1}
    radius = {'big' : 50, 'medium' : 25, 'small' : 15}
    Type = 'big'
    X = -100
    Y = -100
    Vx = 0
    Vy = 0
    dead = True
    list_position = 0

    def generate(self, position):
        self.X = (random.randint(0, window_width // 2) - window_width/4) % window_width
        self.Y = (random.randint(0, window_height // 2) - window_height/4) % window_height
        self.Vx = (random.random() * 2 -1) * asteroid_speed
        self.Vy = (asteroid_speed ** 2 - self.Vx ** 2) ** 0.5
        self.dead = False
        self.list_position = position

    def move(self):
        if not self.dead:
            self.X = (self.X + self.Vx)%window_width
            self.Y = (self.Y + self.Vy)%window_height
            pygame.draw.circle(surface, (255, 255, 255), (int(self.X), int(self.Y)), self.radius[self.Type], 1)

    def is_destroied(self):
        global points, highscore, settings_file
        for i in Ps:
            if not i.unused():
                if math.hypot(self.X - i.X, self.Y - i.Y) <= self.radius[self.Type]:
                    self.dead = True
                    i.X = -100
                    i.Y = -100
                    if self.Type == 'big'or self.Type == 'medium':
                        if self.Type == 'big':
                            son1 = As[self.list_position + 1]
                            son2 = As[self.list_position + 4]
                            son1.generate(self.list_position + 1)
                            son2.generate(self.list_position + 4)
                            points += 20
                        elif self.Type == 'medium':
                            son1 = As[self.list_position + 1]
                            son2 = As[self.list_position + 2]
                            son1.generate(self.list_position + 1)
                            son2.generate(self.list_position + 2)
                            points += 50
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
                        points += 100
                    self.X = -100
                    self.Y = -100
                    if points > highscore:
                        highscore = points

#FONTS
points_font = pygame.font.Font(None, 36)
level_font = pygame.font.Font(None, 100)
start_font = pygame.font.Font(None, 200)

class ship:
    X = window_width/2
    Y = window_height/2
    D = math.pi/2
    Vx = 0
    Vy = 0
    left = False
    right = False
    up = False
    shoot = False
    pulsing = True
    color = (255, 255, 255)
    pulse_time = time.time()

    def move(self):
        global points, acceleration
        if self.left:
            self.D = (self.D + rotation_speed) % (math.pi * 2)
        if self.right:
            self.D = (self.D - rotation_speed) % (math.pi * 2)
        if self.up:
            self.Vx += (acceleration / 2 * math.cos(self.D))
            self.Vy -= (acceleration / 2 * math.sin(self.D))
        self.Vx *= friction
        self.Vy *= friction
        self.X = (self.X + self.Vx) % window_width
        self.Y = (self.Y + self.Vy) % window_height
        if self.up:
            self.Vx += (acceleration / 2 * math.cos(self.D))
            self.Vy -= (acceleration / 2 * math.sin(self.D))
        if not self.pulsing or (time.time() - self.pulse_time)%0.5 >= 0.2:
            pygame.draw.lines(surface, self.color, True, (\
            (self.X + 10 * math.cos(self.D), self.Y  - 10 * math.sin(self.D)),\
            (self.X + 10 * math.cos((self.D + math.pi*3/4)%(2*math.pi)), self.Y  - 10 * math.sin((self.D + math.pi*3/4)%(2*math.pi))),\
            (self.X + 10 * math.cos((self.D + math.pi*5/4)%(2*math.pi)), self.Y  - 10 * math.sin((self.D + math.pi*5/4)%(2*math.pi))),\
            ), 1)
            if self.up:
                pygame.draw.lines(surface, self.color, True, (\
                    (self.X - 14 * math.cos(self.D), self.Y + 14 * math.sin(self.D)),\
                    (self.X - 14 * math.cos(self.D) + 7 * math.cos(self.D-math.pi/4), self.Y + 14 * math.sin(self.D)- 7 * math.sin(self.D-math.pi/4)),\
                    (self.X - 14 * math.cos(self.D) + 7 * math.cos(self.D+math.pi/4), self.Y + 14 * math.sin(self.D)- 7 * math.sin(self.D+math.pi/4)),\
                    ), 1)
        if time.time()-self.pulse_time > 3:
            self.pulsing = False
        if self.shoot:
            points -= 1
            for i in Ps:
                if i.unused():
                    i.shoot(self.X, self.Y, self.Vx, self.Vy, self.D, self.color)
                    self.shoot = False
                    break

    def is_destroied(self):
        global lifes
        if not self.pulsing:
            for i in As:
                if math.hypot(self.X - i.X, self.Y - i.Y) <= i.radius[i.Type] +5:
                    self.pulsing = True
                    self.pulse_time = time.time()
                    self.X = window_width/2
                    self.Y = window_height/2
                    self.D = math.pi/2
                    self.Vx = 0
                    self.Vy = 0
                    lifes -= 1
                    break
            for i in Ps:
                if math.hypot(self.X - i.X, self.Y - i.Y) <= 8:
                    self.pulsing = True
                    self.pulse_time = time.time()
                    self.X = window_width/2
                    self.Y = window_height/2
                    self.D = math.pi/2
                    self.Vx = 0
                    self.Vy = 0
                    lifes -= 1
                    break

def rounding(n):
    if n-int(n)<int(n)+1-n:
        return int(n)
    else:
        return int(n)+1

class button:
    global window_width, window_height
    position = 0
    text = ''
    main_color = (255, 255, 255)
    background_color = (0, 0, 0)

    def init(self, text, position):
        self.text = text
        self.position = position

    def draw(self):
        box = points_font.render(self.text, 0, self.main_color)
        pygame.draw.rect(surface, self.background_color, (window_width//4+5, window_height//4+41+51*self.position, points_font.size(self.text)[0]+10, 36))
        pygame.draw.lines(surface, (255, 255, 255), True, ((window_width//4+5, window_height//4+41+51*self.position),\
                                                           (window_width//4+5, window_height//4+41+36+51*self.position),\
                                                           (window_width//4+15+points_font.size(self.text)[0], window_height//4+41+36+51*self.position),\
                                                           (window_width//4+15+points_font.size(self.text)[0], window_height//4+41+51*self.position)))
        surface.blit(box, (window_width//4+10, window_height//4+41+5+51*self.position))

    def is_clicked(self):
        if pygame.mouse.get_pos()[0]>window_width//4+5 and pygame.mouse.get_pos()[0] < window_width//4+15+points_font.size(self.text)[0] and\
        pygame.mouse.get_pos()[1]>window_height//4+41+51*self.position and pygame.mouse.get_pos()[1] < window_height//4+41+36+51*self.position:
            self.background_color = (255, 255, 255)
            self.main_color = (0, 0, 0)
            if pygame.mouse.get_pressed()[0]:
                return True
        else:
            self.background_color = (0, 0, 0)
            self.main_color = (255, 255, 255)
        return False

quit_button = button()
quit_button.init('Quit', 6)
apply_button = button()
apply_button.init('Apply', 5)

class bar:
    global window_width, window_height
    position = 0
    value = 0
    max_value = 1
    min_value = 1
    text = ''
    bar_color = (127, 127, 127)
    cursor_color = (255, 255, 255)
    left_border = window_width//4     #options border
    right_border = window_width*3//4  #options border
    up_border = window_height//4      #options border
    left_distance = 10
    right_distance = 40
    bar_lenght = 100
    text_Height = 36
    pos_Height = 0
    cursor_pos = 0
    plus = points_font.render('+', 0, (255, 255, 255))
    less = points_font.render('-', 0, (255, 255, 255))
    plus_pressed = False
    less_pressed = False

    def init(self, text, position, value, max_value, min_value):
        self.text, self.position, self.value, self.max_value, self.min_value = text, position, value, max_value, min_value
        self.pos_Height = position*51
        self.cursor_pos = self.bar_lenght*(self.value-self.min_value)//(self.max_value-self.min_value)
        if self.value > self.max_value:
            self.value = self.max_value
        if self.value < self.min_value:
            self.value = self.min_value

    def draw(self):
        box = points_font.render(self.text + ': ' + str(self.value), 0, (255, 255, 255))
        surface.blit(box, (window_width//4+self.left_distance, self.up_border+41+5+self.pos_Height))
        pygame.draw.rect(surface, self.bar_color, (self.right_border-self.right_distance-self.bar_lenght, self.up_border+41+self.pos_Height+12, self.bar_lenght, 12))
        pygame.draw.rect(surface, self.cursor_color, \
                         (self.right_border-self.right_distance-self.bar_lenght+self.cursor_pos-6, self.up_border+41+self.pos_Height, 12, 36))
        surface.blit(self.plus, (self.right_border-self.right_distance+10, self.up_border+41+5+self.pos_Height))
        surface.blit(self.less, (self.right_border-self.right_distance-self.bar_lenght-points_font.size('-')[0]-10, self.up_border+41+5+self.pos_Height))
        if self.value > self.max_value:
            self.value = self.max_value
        if self.value < self.min_value:
            self.value = self.min_value

    def move(self):
        if not pygame.mouse.get_pressed()[0]:
            self.plus_pressed, self.less_pressed = False, False
        if pygame.mouse.get_pos()[0]>=self.right_border-self.bar_lenght-self.right_distance and pygame.mouse.get_pos()[0]<=self.right_border-self.right_distance and \
        pygame.mouse.get_pos()[1]>=self.up_border+41+5+self.pos_Height and pygame.mouse.get_pos()[1]<=self.up_border+41+5+self.pos_Height+self.text_Height and \
        pygame.mouse.get_pressed()[0]:
            self.value = rounding(((pygame.mouse.get_pos()[0]-(self.right_border-self.bar_lenght-self.right_distance))*(self.max_value-self.min_value))/self.bar_lenght+self.min_value)
            self.cursor_pos = self.bar_lenght*(self.value-self.min_value)//(self.max_value-self.min_value)
        if pygame.mouse.get_pos()[0]>=self.right_border-self.right_distance+10 and pygame.mouse.get_pos()[0]<=self.right_border-self.right_distance+10+points_font.size('+')[0] and \
        pygame.mouse.get_pos()[1]>=self.up_border+41+5+self.pos_Height and pygame.mouse.get_pos()[1]<=self.up_border+41+5+self.pos_Height+points_font.size('+')[1] and \
        pygame.mouse.get_pressed()[0] and not self.plus_pressed:
            self.value += 1
            self.cursor_pos = self.bar_lenght*(self.value-self.min_value)//(self.max_value-self.min_value)
            self.plus_pressed = True
        if pygame.mouse.get_pos()[0]>=self.right_border-self.right_distance-self.bar_lenght-points_font.size('-')[0]-10 and pygame.mouse.get_pos()[0]<=self.right_border-self.right_distance-self.bar_lenght-10 and \
        pygame.mouse.get_pos()[1]>=self.up_border+41+5+self.pos_Height and pygame.mouse.get_pos()[1]<=self.up_border+41+5+self.pos_Height+points_font.size('-')[1] and \
        pygame.mouse.get_pressed()[0] and not self.less_pressed:
            self.value -= 1
            self.cursor_pos = self.bar_lenght*(self.value-self.min_value)//(self.max_value-self.min_value)
            self.less_pressed = True
        if self.value > self.max_value:
            self.value = self.max_value
        if self.value < self.min_value:
            self.value = self.min_value

WW = bar()
WW.init('Width', 1, window_width, 3840, 1)
WH = bar()
WH.init('Height', 2, window_height, 2160, 1)
FR = bar()
FR.init('Framerate', 3, framerate, 240, 1)
MP = bar()
MP.init('Players', 4, players, 2, 1)
bars = [WW, WH, FR, MP]

def draw_options():
    global frame, frame_time, window_width, window_height, frame_duration, bars, acceleration, \
    friction, rotation_speed, projectile_speed, asteroid_speed, framerate, lifes, players, shuttle_2
    quitbackground_color = (0, 0, 0)
    quitmain_color = (255, 255, 255)
    while True:
        title_box = points_font.render('OPTIONS', 0, (255, 255, 255))
        pygame.draw.rect(surface, (0, 0, 0), (window_width/4, window_height/4, window_width/2, window_height/2))
        pygame.draw.lines(surface, (255, 255, 255), True, ((window_width/4, window_height/4), (window_width*3/4, window_height/4), (window_width*3/4, window_height*3/4), (window_width/4, window_height*3/4)), 1)
        surface.blit(title_box, ((window_width - points_font.size('OPTIONS')[0])//2, window_height//4 + 5))
        apply_button.draw()
        if apply_button.is_clicked():
            old_players = players
            old_framerate = framerate
            settings_file = open('settings.txt', 'w')
            settings_file.write(str(highscore)+'\n'+str(WW.value)+'\n'+str(WH.value)+'\n'+str(FR.value)+'\n'+str(MP.value))
            settings_file.close()
            import_settings()
            for i in bars:
                i.left_border = window_width//4     #options border
                i.right_border = window_width*3//4  #options border
                i.up_border = window_height//4      #options border
            acceleration = 1000.0 / (framerate**2)
            #print(acceleration)
            friction = 0.8 ** (1.0/framerate)
            rotation_speed = 5.0 / framerate
            projectile_speed = 400.0 / framerate
            asteroid_speed = 200.0 / framerate
            frame_duration = 1.0 / framerate
            if game_started:
                shuttle_1.Vx *= old_framerate/framerate
                shuttle_1.Vy *= old_framerate/framerate
                if players == 2:
                    try:
                        shuttle_2.Vx *= old_framerate/framerate
                        shuttle_2.Vy *= old_framerate/framerate
                    except:
                        shuttle_2 = ship()
                        shuttle_2.Vx *= old_framerate/framerate
                        shuttle_2.Vy *= old_framerate/framerate
                        shuttle_1.color = (0, 255, 0)
                        shuttle_2.color = (255, 0, 0)
                for i in Ps:
                    i.Vx *= old_framerate/framerate
                    i.Vy *= old_framerate/framerate
                for i in As:
                    i.Vx *= old_framerate/framerate
                    i.Vy *= old_framerate/framerate
                players = MP.value
                if old_players != players:
                    if players == 2:
                        lifes += 2
                    else:
                        lifes -= 2
                        shuttle_1.color = (255, 255, 255)
        quit_button.draw()
        if quit_button.is_clicked():
            settings_file = open('settings.txt', 'r+')
            settings_file.write(str(highscore)+'\n'+str(window_width)+'\n'+str(window_height)+'\n'+str(framerate)+'\n'+str(players))
            settings_file.close()
            pygame.quit()
            sys.exit()
        for i in bars:
            i.move()
            i.draw()
        pygame.display.update()
        wait_next_frame()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

def start_level(level):
    global As, level_start_frame
    for i in range(0, level * 14):
        As.append( asteroids())
    for i in range(0, level * 14, 7):
        As[i].generate(i)
    level_start_frame = -1

def check_for_level():
    global level, frame, level_start_frame, framerate
    for i in As:
        if i.dead == False:
            return False
    if level_start_frame < frame:
        level_start_frame = frame + 2 * framerate
    lc = 255 * (1-(math.fabs(level_start_frame - framerate -frame)/framerate))
    level_box = level_font.render('Level ' + str(level+1), 0, (lc, lc, lc))
    surface.blit(level_box, ((window_width - level_font.size('Level ' + str(level))[0])/2, (window_height - level_font.size('Level ' + str(level))[1])/2))
    if frame == level_start_frame:
        level +=1
        start_level(level)

def draw_points():
    global points
    points_box = points_font.render(str(points), 0, (255, 255, 255))
    surface.blit(points_box, (window_width - points_font.size(str(points))[0] - 10, 10))

def draw_lifes():
    global lifes
    lifes_box = points_font.render('Δ x ' + str(lifes), 0, (255, 255, 255))
    surface.blit(lifes_box, (10, 10))

def draw_highscore():
    global highscore
    highscore_box = points_font.render('HIGHSCORE: ' + str(highscore), 0, (255, 255, 255))
    surface.blit(highscore_box, ((window_width - points_font.size('HIGHSCORE: ' + str(highscore))[0])/2, 10))

def move():
    global level, players
    check_for_level()
    shuttle_1.move()
    shuttle_1.is_destroied()
    if players == 2:
        shuttle_2.move()
        shuttle_2.is_destroied()
    for i in Ps:
        i.remove()
        if not i.unused():
            i.move()
    for i in As:
        i.move()
        i.is_destroied()
    draw_points()
    draw_lifes()
    draw_highscore()
    pygame.display.update()

def wait_for_space():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            draw_options()
    time.sleep(0.01)

def draw_gameover():
    global lifes, frame, framerate, frame_time
    death_frame = frame
    while True:
        wait_next_frame()
        gc = 255 * (frame - death_frame)/framerate
        surface.fill((0, 0, 0))
        gameover_box_1 = level_font.render('GAME OVER', 0, (gc, gc, gc))
        surface.blit(gameover_box_1, ((window_width - level_font.size('GAME OVER')[0])/2, (window_height - level_font.size('GAME OVER')[1])/2))
        gameover_box_2 = points_font.render('press SPACE to restart', 0, (gc, gc, gc))
        surface.blit(gameover_box_2, ((window_width - points_font.size('press SPACE to restart')[0])/2, (window_height - points_font.size('press SPACE to restart')[1])/2+50))
        pygame.display.update()
        if frame == death_frame + framerate:
            break
    while True:
        surface.fill((0, 0, 0))
        gameover_box_1 = level_font.render('GAME OVER', 0, (gc, gc, gc))
        surface.blit(gameover_box_1, ((window_width - level_font.size('GAME OVER')[0])/2, (window_height - level_font.size('GAME OVER')[1])/2))
        gameover_box_2 = points_font.render('press SPACE to restart', 0, (gc, gc, gc))
        surface.blit(gameover_box_2, ((window_width - points_font.size('press SPACE to restart')[0])/2, (window_height - points_font.size('press SPACE to restart')[1])/2+50))
        pygame.display.update()
        if wait_for_space():
            break
    frame_time = time.time()
    while True:
        wait_next_frame()
        gc = 255 * (1-(frame - death_frame - framerate)/framerate) +1
        surface.fill((0, 0, 0))
        gameover_box_1 = level_font.render('GAME OVER', 0, (gc, gc, gc))
        surface.blit(gameover_box_1, ((window_width - level_font.size('GAME OVER')[0])/2, (window_height - level_font.size('GAME OVER')[1])/2))
        gameover_box_2 = points_font.render('press SPACE to restart', 0, (gc, gc, gc))
        surface.blit(gameover_box_2, ((window_width - points_font.size('press SPACE to restart')[0])/2, (window_height - points_font.size('press SPACE to restart')[1])/2+50))
        pygame.display.update()
        if frame == death_frame + 2*framerate:
            break

def start_game():
    global lifes, level, frame, framerate, level_start_frame, points, shuttle_1, shuttle_2, frame_time, As, players
    frame_time = time.time()
    if players == 2:
        shuttle_1 = ship()
        shuttle_2 = ship()
        shuttle_1.color = (0, 255, 0)
        shuttle_2.color = (255, 0, 0)
    else:
        shuttle_1 = ship()
    level = 0
    frame = 0
    level_start_frame  = 2 * framerate
    points = 0
    As = []
    if players == 2:
        lifes = 5
    else:
        lifes = 3
    start_level(level)
    while True:
        wait_next_frame()
        events()
        surface.fill((0, 0, 0))
        move()
        if lifes <= 0:
            break

def draw_start_screen():
    while True:
        surface.fill((0, 0, 0))
        start_box_1 = start_font.render('ASTEROIDS', 0, (255, 255, 255))
        surface.blit(start_box_1, ((window_width - start_font.size('ASTEROIDS')[0])/2, (window_height - start_font.size('ASTEROIDS')[1])/2 - 100))
        gameover_box_2 = points_font.render('press SPACE to start', 0, (255, 255, 255))
        surface.blit(gameover_box_2, ((window_width - points_font.size('press SPACE to start')[0])/2, (window_height - points_font.size('press SPACE to start')[1])/2+100))
        credits_box = points_font.render('a game by Giacomo Gallina', 0, (255, 255, 255))
        surface.blit(credits_box, ((window_width - points_font.size('a game by Giacomo Gallina')[0])/2, (window_height - points_font.size('a game by Giacomo Gallina')[1])/2))
        pygame.display.update()
        if wait_for_space():
            break

game_started = False
draw_start_screen()
game_started = True
while True:
    start_game()
    draw_gameover()
