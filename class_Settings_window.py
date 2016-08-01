from PyQt4 import QtGui, QtCore
import sys

class Settings_window(QtGui.QMainWindow):

    value_changers = []

    def __init__(self, boss):
        self.boss = boss
        # old_window_width = self.boss.window_width
        # old_window_height = self.boss.window_height
        # old_framerate = self.boss.framerate
        # old_players = self.boss.players
        # new_window_width = self.boss.window_width
        # new_window_height = self.boss.window_height
        # new_framerate = self.boss.framerate
        # new_players = self.boss.players

        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('ASTEROIDS / Settings')




        quit_button = QtGui.QPushButton('Quit')
        apply_button = QtGui.QPushButton('Apply')
        self.value_changers.append(Value_changer(self, self.boss.players, \
                                        1, 2))

        quit_button.clicked.connect(self.quit)
        apply_button.clicked.connect(self.apply)

        cwidget = QtGui.QWidget()
        self.grid = QtGui.QGridLayout()
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

        window_width_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        window_height_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        framerate_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        players_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)

        window_width_slider.valueChanged[int].connect(self.value_changers[0].change_value)
        window_height_slider.valueChanged[int].connect(self.value_changers[1].change_value)
        framerate_slider.valueChanged[int].connect(self.value_changers[2].change_value)
        players_slider.valueChanged[int].connect(self.value_changers[3].change_value)

        self.grid.addWidget(window_width_slider, 0, 2)
        self.grid.addWidget(window_height_slider, 1, 2)
        self.grid.addWidget(framerate_slider, 2, 2)
        self.grid.addWidget(players_slider, 3, 2)
        self.grid.addWidget(apply_button, 5, 1)
        self.grid.addWidget(quit_button, 5, 2)



        cwidget.setLayout(self.grid)
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
        self.lenght = 100
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
        self.new_value = int((value/self.lenght*(self.max-self.min))+self.min)
        print(self.new_value)
        #print('test')
        self.label.setText(str(self.new_value))
