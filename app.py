import sys,json
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# class_
from class_.MenuBar import *
from class_.Content import *


class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'English Myanmar Dictionary'
        self.top = 100
        self.left = 200
        self.width = 600
        self.height = 400
        # init
        self.__configDB()
        self.__config()
        self.__initUI()
        self.__menu_event()

    def __configDB(self):
        config = self.__get_config()
        if config != None:
            if config['is_max']:
                self.showMaximized()
            else:
                self.left = config['left']
                self.top = config['top']
                self.width = config['width']
                self.height = config['height']
            

    def __config(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('assets/png/icon.png'))
        self.setGeometry(self.left, self.top, self.width, self.height)

    def __initUI(self):
        # main layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(3, 0, 3, 3)
        # class_
        self.mainMenuBar = MenuBar()
        self.content = Content()

        # add layout
        self.mainLayout.addWidget(self.mainMenuBar)
        self.mainLayout.addLayout(self.content)

        # set layout
        self.setLayout(self.mainLayout)

    #####################################
    # menu event
    def __menu_event(self):
        self.mainMenuBar.viewMenu.triggered[QAction].connect(
            self.view_menu_event)
        self.mainMenuBar.editMenu.triggered[QAction].connect(
            self.edit_menu_event)
        self.mainMenuBar.google_wiki_action_change = self.google_wiki_action_change

    # view menu
    def view_menu_event(self, q):
        name = q.text()
        if name == 'Hide History':
            self.mainMenuBar.historyAction.setText('Show History')
            self.content.searchContent.hide_history()
        elif name == 'Show History':
            self.mainMenuBar.historyAction.setText('Hide History')
            self.content.searchContent.show_history()

    # edit menu
    def edit_menu_event(self, q):
        name = q.text()
        if name == 'Clear History':
            self.content.searchContent.clear_history()
    
    #google_wiki_action_change
    def google_wiki_action_change(self):
        self.content.searchContent.config()
    #####################################

    #####################################
    # event
    def keyPressEvent(self, e):
        # enter key
        if e.key() == Qt.Key_Enter - 1:
            self.content.searchBar.speech_word()
            # search google
            self.content.search_google()

    def moveEvent(self, e):
        self.__set_config()
        
    def resizeEvent(self,e):
        self.__set_config()
            
    #####################################

    #####################################
    # config database

    def __get_config(self):
        try:
            with open('assets/db/config.json','r') as f:
                return json.loads(f.read())
                f.close()
        except:
            print('read config error')
            return  None

    def __set_config(self):
        config = {}
        left = self.pos().x()
        top = self.pos().y()
        width = self.size().width()
        height = self.size().height()
        if self.isMaximized():
            config = {'width':width,'height':height,'left':left,'top':top,'is_max':True}
        else:
            config = {'width':width,'height':height,'left':left,'top':top,'is_max':False}
        try:
            
            with open('assets/db/config.json','w') as f:
                f.write(json.dumps(config))
                f.close()
        except:
            print('set config error')
    #####################################


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()

    sys.exit(app.exec_())
