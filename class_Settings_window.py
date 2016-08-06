from PyQt4 import QtGui, QtCore
import sys

class Settings_window(QtGui.QMainWindow):

    value_changers = []

    def __init__(self, boss):
        self.boss = boss


        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('ASTEROIDS / Settings')




        quit_button = QtGui.QPushButton('Quit')
        apply_button = QtGui.QPushButton('Apply')


        quit_button.clicked.connect(self.quit)
        apply_button.clicked.connect(self.apply)

        cwidget = QtGui.QWidget()
        self.grid = QtGui.QGridLayout()
        self.vbox = QtGui.QVBoxLayout()
        self.hbox = QtGui.QHBoxLayout()
        self.grid.addWidget(QtGui.QLabel('Window Width:'), 0, 0)
        self.grid.addWidget(QtGui.QLabel('Window Height:'), 1, 0)
        self.grid.addWidget(QtGui.QLabel('Framerate:'), 2, 0)
        self.grid.addWidget(QtGui.QLabel('Players:'), 3, 0)

        self.window_width_label = QtGui.QLabel(str(self.boss.window_width))
        self.window_height_label = QtGui.QLabel(str(self.boss.window_height))
        self.framerate_label = QtGui.QLabel(str(self.boss.framerate))
        self.players_label = QtGui.QLabel(str(self.boss.players))

        self.value_changers.append\
        (Value_changer(self.window_width_label, self.boss.window_width, 320, 3840))
        self.value_changers.append\
        (Value_changer(self.window_height_label, self.boss.window_height, 240, 2160))
        self.value_changers.append\
        (Value_changer(self.framerate_label, self.boss.framerate, 30, 240))
        self.value_changers.append\
        (Value_changer(self.players_label, self.boss.players, 1, 2))

        self.grid.addWidget(self.window_width_label, 0, 1)
        self.grid.addWidget(self.window_height_label, 1, 1)
        self.grid.addWidget(self.framerate_label, 2, 1)
        self.grid.addWidget(self.players_label, 3, 1)

        self.sliders = []

        for i in range(4):
            self.sliders.append(QtGui.QSlider(QtCore.Qt.Horizontal, self))
            self.sliders[i].valueChanged[int].connect(self.value_changers[i].change_value)
            self.grid.addWidget(self.sliders[i], i, 4)

        more_less_buttons = []

        for i in range(4):
            more_less_buttons.append(QtGui.QPushButton('-'))
            button_width = more_less_buttons[i].fontMetrics().boundingRect('-').width() + 20
            more_less_buttons[i].setMaximumWidth(button_width)
            more_less_buttons[i].clicked.connect(self.value_changers[i].less)
            self.grid.addWidget(more_less_buttons[i], i, 3)

        for i in range(4):
            more_less_buttons.append(QtGui.QPushButton('+'))
            button_width = more_less_buttons[i+4].fontMetrics().boundingRect('+').width() + 20
            more_less_buttons[i+4].setMaximumWidth(button_width)
            more_less_buttons[i+4].clicked.connect(self.value_changers[i].more)
            self.grid.addWidget(more_less_buttons[i+4], i, 5)

        self.grid.addWidget(more_less_buttons[0], 0, 3)
        self.grid.addWidget(more_less_buttons[1], 1, 3)
        self.grid.addWidget(more_less_buttons[2], 2, 3)
        self.grid.addWidget(more_less_buttons[3], 3, 3)
        self.grid.addWidget(more_less_buttons[4], 0, 5)
        self.grid.addWidget(more_less_buttons[5], 1, 5)
        self.grid.addWidget(more_less_buttons[6], 2, 5)
        self.grid.addWidget(more_less_buttons[7], 3, 5)
        self.hbox.addStretch(1)
        self.hbox.addWidget(apply_button)
        self.hbox.addWidget(quit_button)
        self.vbox.addLayout(self.grid)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)



        cwidget.setLayout(self.vbox)
        self.setCentralWidget(cwidget)

    def apply(self):
        pass

    def quit(self):
        sys.exit()




class Value_changer():

    def __init__(self, label, value, min_value, max_value):
        # self.boss = boss
        # slider = QtGui.QSlider(QtCore.Qt.Horizontal, boss)
        # slider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lenght = 99#100
        self.min = min_value
        self.max = max_value
        self.label = label
        # self.index = index
        #self.slider.setGeometry(30, 40, self.lenght, 30)
        #slider.valueChanged[int].connect(self.change_value)
        self.value = value
        self.old_value = value
        self.new_value = value
        # self.hbox = QtGui.QHBoxLayout()
        # self.hbox.addWidget(QtGui.QLabel(title + ':'))
        # self.value_label = QtGui.QLabel(str(self.new_value))
        # self.hbox.addWidget(self.value_label)
        # self.hbox.addWidget(slider)

    def change_value(self, value):
        self.new_value = int(((value*1.0)/self.lenght*(self.max-self.min))+self.min)
        #print(self.new_value)
        #print('test')
        self.label.setText(str(self.new_value))

    def more(self):
        if self.new_value < self.max:
            self.new_value += 1
            self.label.setText(str(self.new_value))

    def less(self):
        if self.new_value > self.min:
            self.new_value -= 1
            self.label.setText(str(self.new_value))
