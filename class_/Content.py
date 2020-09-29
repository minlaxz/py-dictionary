from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pyttsx3
import googletrans
from myanmar import language

from class_.SearchBar import *
from class_.SearchContent import *


class Content(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.__setConfig()
        self.__initUI()
        self.__event()

    def __setConfig(self):
        # self.setStretch(10, 10)
        pass

    def __initUI(self):
        # layout
        self.searchBar = SearchBar()
        self.searchContent = SearchContent()

        # add
        self.addLayout(self.searchBar, 1)
        self.addLayout(self.searchContent, 10)

    #####################################
    # event
    def __event(self):
        # searchBar event
        self.searchBar.search_input.textChanged.connect(
            self.search_input_change)
        self.searchContent.history_list.currentItemChanged.connect(
            self.history_list_change)

    #####################################
    # searchBar event func
    def search_input_change(self, word):
        if language.ismyanmar(word):
            self.searchContent.search_mm_word(word)
        else:
            self.searchContent.search_eng_word(word)

    def search_google(self):
        word = self.searchBar.search_input.text()
        self.searchContent.search_eng_word_google(word)
        self.searchContent.search_eng_word_wikipedia(word)
    #####################################
    # searchContent event func

    def history_list_change(self, q):
        if q != None:
            self.searchContent.search_eng_word(q.text())
            self.searchContent.search_eng_word_google(q.text(), False)
            self.searchContent.search_eng_word_wikipedia(q.text(), False)


#####################################
#
#####################################
