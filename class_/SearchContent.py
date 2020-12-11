from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import googletrans
import wikipedia
import json

from class_.database import Dict, History


class SearchContent(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.trans = googletrans.Translator()
        self.wiki = wikipedia
        self.wiki.set_lang('my')
        # db
        self.db = Dict()
        self.historyDB = History()
        self.words = []
        # is search
        self.is_search_google = False
        self.is_search_wiki = False

        self.__initUI()
        self.__event()
        self.__style()
        self.config()

    def __initUI(self):
        # widget
        self.search_list = QListWidget()
        self.history_list = QListWidget()
        # config
        self.search_list.setWordWrap(True)
        # default
        self.show_history_list()
        # add
        self.addWidget(self.search_list, 10)
        self.addWidget(self.history_list, 3)

    #####################################
    # event

    def __event(self):
        pass
    #####################################

    #####################################
    # config
    def config(self):
        # get config
        config = self.search_config_get()
        if config != None:
            self.is_search_google = config['is_google']
            self.is_search_wiki = config['is_wiki']
    #####################################

    # show list

    def show_words(self, words):
        self.search_list.clear()
        for word in words:
            self.search_list.addItem(f"""{word[1]} \n{word[2]}""")
    # search from database

    def search_eng_word(self, word):
        # db
        self.words = self.db.search_eng(word)
        if self.words != None:
            self.show_words(self.words)
    
    def search_mm_word(self, word):
        # db
        self.words = self.db.search_mm(word)
        if self.words != None:
            self.show_words(self.words)
    # search from google

    def search_eng_word_google(self, word, is_set_history=True):

        if word != "":
            # set history
            if is_set_history:
                self.set_history(word)
            try:
                if self.is_search_google:
                    # find google
                    res = self.trans.translate(word, dest='my')

                    result = (0, f'{word}-Google Translate', res.text)
                    words = self.words
                    # words.append(result)
                    words.insert(0, result)
                    self.show_words(words)
            except Exception as e:
                print('google search error')
                print(e)

    # search wikipedia
    def search_eng_word_wikipedia(self, word, is_set_history=True):
        if word != "":
            # set history
            if is_set_history:
                self.set_history(word)
            try:
                if self.is_search_wiki:
                    # find google
                    res = self.wiki.summary(word)
                    result = (0, f'{word}-Wiki Translate', res)
                    words = self.words
                    # words.append(result)
                    words.insert(1, result)
                    self.show_words(words)
            except:
                print('wikipedia search error')

    #####################################
    # history list
    def set_history(self, word):
        if word != '':
            try:
                self.historyDB.add(word)
            except:
                print('add error')
            finally:
                self.show_history_list()

    def show_history_list(self):
        words = self.historyDB.findAll()
        if words != None:
            self.history_list.clear()
            for w in words:
                self.history_list.addItem(w[1])

    def clear_history(self):
        self.historyDB.deleteAll()
        self.show_history_list()
    # widget show and hide

    def hide_history(self):
        self.history_list.setHidden(True)

    def show_history(self):
        self.history_list.setHidden(False)
    #####################################

    #####################################
    # style

    def __style(self):
        self.search_list.setStyleSheet("""
            QListWidget::Item {
                border-bottom: 1px solid #333;
                padding: 10px 0;
                color:#333;
            }
        """)
    #####################################

    #####################################
    # search config
    def search_config_set(self):
        try:
            config = {'is_google': True, 'is_wiki': False}
            with open('assets/db/search_config.json', 'w') as f:
                f.write(json.dumps(config))
        except:
            print('search config set error')

    def search_config_get(self):
        try:
            with open('assets/db/search_config.json', 'r') as f:
                return json.loads(f.read())
        except:
            return None
            print('search config set error')
    #####################################
