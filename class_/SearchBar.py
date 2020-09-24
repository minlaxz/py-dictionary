from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pyttsx3


class SearchBar(QHBoxLayout):
    def __init__(self):
        super().__init__()
        # speech
        self.speech = pyttsx3.init()
        # widget
        self.search_input = QLineEdit()
        self.search_sound = QPushButton()
        # config
        self.__setConfig()
        self.__event()
        self.__keyborad_event()

        # add
        self.addWidget(self.search_input)
        self.addWidget(self.search_sound)

    def __setConfig(self):
        self.search_input.setPlaceholderText('Search...')
        self.search_sound.setIcon(QIcon(QPixmap('assets/png/sound.png')))
        self.search_input.setToolTip('Ctrl+S')
        self.search_sound.setToolTip('Enter')

    def speech_word(self):
        word = self.search_input.text()
        # check
        if word != '':
            self.speech.say(word)
            self.speech.runAndWait()

    #####################################
    # event
    def __event(self):
        self.search_sound.clicked.connect(self.speech_word)

    #####################################

    #####################################
    # keyboard event
    def __keyborad_event(self):
        # search field set focus
        focus = QShortcut(QKeySequence('Ctrl+S'), self.search_input)
        focus.activated.connect(lambda: self.search_input.setFocus(True))

    #####################################
