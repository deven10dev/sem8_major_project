from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog
from router import ScreenStack

class HomeScreen(QDialog, ScreenStack):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi("screens/ui/home_screen.ui",self)
        self.home_screen_photo.setPixmap(QPixmap('images/1.png'))
        self.getStarted.clicked.connect(self.goToSelectionScreen)
