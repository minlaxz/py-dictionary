from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json


class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()

        self.__initUI()
        self.__setConfig()
        self.__event()

    def __setConfig(self):
        self.setFixedHeight(30)
        # get config
        config = self.search_config_get()
        self.is_googleAction, self.is_wikipediaAction = config.values() if config else (False, False)
        # set action
        self.googleAction.setChecked(self.is_googleAction)
        self.wikipediaAction.setChecked(self.is_wikipediaAction)

    def __initUI(self):
        self.fileMenu = self.addMenu('File')
        self.editMenu = self.addMenu('Edit')
        self.viewMenu = self.addMenu('View')

        # add action
        self.historyAction = self.viewMenu.addAction('Hide History')

        self.googleAction = QAction(
            'Search Google', self.viewMenu, checkable=True)
        self.wikipediaAction = QAction(
            'Search Wikipedia', self.viewMenu, checkable=True)
        self.viewMenu.addAction(self.googleAction)
        self.viewMenu.addAction(self.wikipediaAction)

        self.editMenu.addAction('Clear History')

    #####################################
    # event
    def __event(self):
        self.googleAction.changed.connect(self.googleActionChange)
        self.wikipediaAction.changed.connect(self.wikipediaActionChange)

    def googleActionChange(self):
        self.is_googleAction = self.googleAction.isChecked()
        self.search_config_set()
        self.google_wiki_action_change()

    def wikipediaActionChange(self):
        self.is_wikipediaAction = self.wikipediaAction.isChecked()
        self.search_config_set()
        self.google_wiki_action_change()

    #####################################
    def google_wiki_action_change(self):
        pass
    #####################################
    # search config

    def search_config_set(self):
        try:
            config = {'is_google': self.is_googleAction,
                      'is_wiki': self.is_wikipediaAction}
            with open('assets/db/search_config.json', 'w') as f:
                f.write(json.dumps(config))
        except Exception as e:
            print('search config set error')
            print(e)

    def search_config_get(self):
        try:
            with open('assets/db/search_config.json', 'r') as f:
                return json.loads(f.read())
        except:
            return None
            print('search config set error')
    #####################################
