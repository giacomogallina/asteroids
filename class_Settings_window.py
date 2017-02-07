import sys, pygame, class_Ship, time, random
#from class_Ship import *

pygame.init()
points_font = pygame.font.Font(None, 36)

white = (255, 255, 255)
grey = (127, 127, 127)
black = (0, 0, 0)


class VBox():
    X, Y = 0, 0
    widgets = []
    size = [0, 0]

    def set_size(self):
        self.size = [0, 0]
        for i in self.widgets:
            i.X = self.X
            i.Y = self.Y + self.size[1]
            widget_size = i.set_size()
            if self.size[0] < widget_size[0]:
                self.size[0] = widget_size[0]
            self.size[1] += widget_size[1]
        return self.size

    def draw(self):
        for i in self.widgets:
            i.draw()

    def check(self, pos):
        for i in self.widgets:
            i.check(pos)



class HBox():
    X, Y = 0, 0
    widgets = []
    size = [0, 0]

    def set_size(self):
        self.size = [0, 0]
        for i in self.widgets:
            i.X = self.X + self.size[0]
            i.Y = self.Y
            widget_size = i.set_size()
            if self.size[1] < widget_size[1]:
                self.size[1] = widget_size[1]
            self.size[0] += widget_size[0]
        return self.size

    def draw(self):
        for i in self.widgets:
            i.draw()

    def check(self, pos):
        for i in self.widgets:
            i.check(pos)



class Frame():
    X, Y = 0, 0

    def __init__(self, widget, frame = False, border = 5, surface = ''):
        self.widget = widget
        self.frame = frame
        self.border = border
        self.surface = surface

    def set_size(self):
        self.widget.X = self.X + self.border
        self.widget.Y = self.Y + self.border
        widget_size = self.widget.set_size()
        self.size = [widget_size[0] + 2 * self.border, \
                     widget_size[1] + 2 * self.border]
        return self.size

    def draw(self):
        if self.border:
            pygame.draw.lines(self.surface, white, True,\
                              ((self.X, self.Y),\
                               (self.X, self.Y + self.size[1]),\
                               (self.X + self.size[0], self.Y + self.size[1]),\
                               (self.X + self.size[0], self.Y)))
        self.widget.draw()

    def check(self, pos):
        self.widget.check(pos)



class Label():
    X, Y = 0, 0

    def __init__(self, surface, text, frame = 5):
        self.text = text
        self.surface = surface
        self.frame = frame
        self.make_text()

    def make_text(self):
        x, y = list(points_font.size(self.text))
        self.size = [x + 2 * self.frame, y + 2 * self.frame]
        self.box = points_font.render(self.text, 0, white)

    def set_text(self, text):
        self.text = text
        self.make_text()

    def set_size(self):
        return self.size

    def draw(self):
        self.surface.blit(self.box, (self.X + self.frame, self.Y + self.frame))

    def check(self, pos):
        pass



class Button():
    X, Y = 0, 0
    background_color = black
    text_color = white

    def __init__(self, surface, text, function, frame = 5, border = True):
        self.function = function
        self.text = text
        self.surface = surface
        self.frame = frame
        #print (self.frame)
        self.border = border
        self.make_text()

    def make_text(self):
        x, y = list(points_font.size(self.text))
        self.size = [x + 2 * self.frame, y + 2 * self.frame]
        self.box = points_font.render(self.text, 0, white)

    def set_text(self, text):
        self.text = text
        self.make_text()

    def set_size(self):
        return self.size

    def draw(self):
        if self.below_mouse(pygame.mouse.get_pos()):
            self.background_color = white
            self.text_color = black
            self.box = points_font.render(self.text, 0, self.text_color)
        else:
            self.background_color = black
            self.text_color = white
            self.box = points_font.render(self.text, 0, self.text_color)

        pygame.draw.rect(self.surface, self.background_color,\
                         (self.X, self.Y, self.size[0], self.size[1]))
        if self.border:
            pygame.draw.lines(self.surface, self.text_color, True,\
                              ((self.X, self.Y),\
                               (self.X, self.Y + self.size[1]),\
                               (self.X + self.size[0], self.Y + self.size[1]),\
                               (self.X + self.size[0], self.Y)))
        self.surface.blit(self.box, (self.X + self.frame, self.Y + self.frame))

    def below_mouse(self, pos):
        if pos[0] >= self.X and pos[0] <= self.X + self.size[0] and\
        pos[1] >= self.Y and pos[1] <= self.Y + self.size[1]:
            return True
        return False

    def check(self, pos):
        if self.below_mouse(pos):
            self.function()



class Main_window():
    def __init__(self, surface):
        self.surface = surface
        self.widget = Label("Still no widgets here =(", self.surface)

    def update(self):
        self.surface.fill(black)
        self.widget.set_size()
        self.widget.draw()
        pygame.display.update()

    def check(self, pos):
        self.widget.check(pos)



class Space():
    X, Y = 0, 0
    def __init__(self, width, height):
        self.size = [width, height]

    def set_size(self):
        return self.size

    def draw(self):
        pass

    def check(self, pos):
        pass



class Line():
    X, Y = 0, 0

    def __init__(self, surface, lenght, vertical = False):
        self.surface = surface
        self.lenght = lenght
        self.vertical = vertical

    def check(self, pos):
        pass

    def set_size(self):
        if self.vertical:
            return [1, self.lenght]
        else:
            return [self.lenght, 1]

    def draw(self):
        if self.vertical:
            points = ((self.X, self.Y), (self.X, self.Y + self.lenght))
        else:
            points = ((self.X, self.Y), (self.X + self.lenght, self.Y))
        pygame.draw.lines(self.surface, white, False, points)


class Bar():
    X, Y = 0, 0
    size = [120, 30]
    cursor_pos = 0

    def __init__(self, surface, min_value, max_value):
        self.surface = surface
        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value

    def set_size(self):
        return self.size

    def set_cursor_pos(self):
        self.cursor_pos = 100 * (self.value - self.min_value)\
        / (self.max_value - self.min_value)

    def draw(self):
        self.set_cursor_pos()
        pygame.draw.rect(self.surface, grey, (self.X + 10, self.Y + 10, 100, 10))
        pygame.draw.rect(self.surface, white, \
                         (self.X + self.cursor_pos + 5, self.Y, 10, 30))

    def below_mouse(self, pos):
        if pos[0] >= self.X + 10 and pos[0] <= self.X + 110 and\
        pos[1] >= self.Y + 10 and pos[1] <= self.Y + 20:
            return True
        return False

    def check(self, pos):
        if self.below_mouse(pos):
            self.cursor_pos = pos[0] - self.X - 10
            self.value = int((self.cursor_pos) * \
                             (self.max_value - self.min_value)\
                             / 100 + self.min_value)



class Slider():
    X, Y = 0, 0

    def __init__(self, surface, width, min_value, max_value, text):
        self.width = width
        self.h = HBox()
        self.h2 = HBox()
        self.bar = Bar(surface, min_value, max_value)
        self.plus_button = Button(surface, '+', self.plus, border = False)
        self.less_button = Button(surface, '-', self.less, border = False)
        self.l = Label(surface, text)
        self.v = Label(surface, str(min_value))
        self.s = Space(50, 0)
        self.h.widgets = [self.l, self.v, self.s]
        self.h2.widgets = [self.less_button, self.bar, self.plus_button]
        #self.h2.set_size()
        #print(self.h2.size)

    def set_size(self):
        self.h.X, self.h.Y = self.X, self.Y
        size = self.h.set_size()
        self.h2.X, self.h2.Y = self.X + self.width - 162, self.Y
        self.h2.set_size()
        if size[0] < self.width:
            return [self.width, size[1]]
        return size

    def get_value(self):
        return self.bar.value

    def set_value(self, value):
        self.bar.value = value

    def draw(self):
        self.h.draw()
        self.h2.draw()

    def check(self, pos):
        self.h.check(pos)
        self.h2.check(pos)
        self.v.set_text(str(self.bar.value))

    def plus(self):
        if self.bar.value < self.bar.max_value:
            self.bar.value += 1

    def less(self):
        if self.bar.value > self.bar.min_value:
            self.bar.value -= 1


if __name__ == '__main__':
    pass



class Settings_window():

    def __init__(self, boss):
        self.boss = boss
        self.surface = self.boss.surface

        v = VBox()
        self.f = Frame(v, surface = self.surface, border = True)
        self.f.X = self.boss.window_width // 4
        self.f.Y = self.boss.window_height // 4

        sliders_width = self.boss.window_width // 2 - 10
        #print(sliders_width)
        s_w = Slider(self.surface, sliders_width, 320, 3840, 'Window Width')
        s_h = Slider(self.surface, sliders_width, 240, 2160, 'Window Height')
        s_f = Slider(self.surface, sliders_width, 30, 240, 'Framerate')
        s_p = Slider(self.surface, sliders_width, 1, 2, 'Players')

        s_w.set_value(self.boss.window_width)
        s_h.set_value(self.boss.window_height)
        s_f.set_value(self.boss.framerate)
        s_p.set_value(self.boss.players)

        self.s = [s_w, s_h, s_f, s_p]

        htitle = HBox()
        title = Label(self.surface, 'Settings')
        exit_button = Button(self.surface, 'X', self.stop, border = False)
        s1 = Space(self.f.X - 100, 0) #aggiustare
        htitle.widgets = [exit_button, s1, title]

        s2 = Space(5, 0)
        l1 = Line(self.surface, sliders_width-10)
        h2 = HBox()
        h2.widgets = [s2, l1]

        s5 = Space(5, 0)
        l2 = Line(self.surface, sliders_width-10)
        h4 = HBox()
        h4.widgets = [s5, l2]

        quit_button = Button(self.surface, 'Quit', self.boss.quit, border = False)
        apply_button = Button(self.surface, 'Apply', self.apply, border = False)
        s4 = Space(sliders_width-200, 0) #aggiustare
        h3 = HBox()
        h3.widgets = [s4, apply_button, Space(20, 0), quit_button]

        s3 = Space(0, self.boss.window_height//2 - 200) #aggiustare

        v.widgets = [htitle, h2, s_w, s_h, s_f, s_p, s3, h4, h3]

        self.run()

    def run(self):
        self.keep_running = True
        self.f.set_size()
        self.f.check((0, 0))
        while self.keep_running:
            event = pygame.event.poll()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    #print('event!')
                    self.f.check(pygame.mouse.get_pos())
            self.surface.fill(black)
            self.f.draw()
            pygame.display.update()

    def stop(self):
        self.keep_running = False

    def apply(self):
        old_framerate = self.boss.framerate
        old_players = self.boss.players
        settings_file = open('settings.txt', 'w')
        settings_file.write(str(self.boss.highscore)+'\n'\
                            +str(self.s[0].get_value())+'\n'+\
                            str(self.s[1].get_value())+'\n'\
                            +str(self.s[2].get_value())+'\n'+\
                            str(self.s[3].get_value()))
        settings_file.close()
        self.boss.import_settings()
        self.boss.surface = pygame.display.set_mode\
        ((self.boss.window_width, self.boss.window_height))
        self.boss.frame_duration = 1.0 / self.boss.framerate
        pygame.display.update()

    def quit(self):
        self.boss.quit()
