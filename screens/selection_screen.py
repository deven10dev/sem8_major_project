from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog
from router import ScreenStack

class SelectionScreen(QDialog, ScreenStack):
    def __init__(self):
        super(SelectionScreen, self).__init__()
        loadUi("screens/ui/selection_screen.ui",self)
        self.selection_screen_photo.setPixmap(QPixmap('images/2.png'))
        self.pushButton_3.clicked.connect(self.goToRecordedVideoScreen)
        self.gotoexcteachbutton.clicked.connect(self.goToExcteachScreen)
        self.gotoexcselectionbutton.clicked.connect(self.goToExcSelectionScreen)
        self.backButton.clicked.connect(self.goToPreviousScreen)
