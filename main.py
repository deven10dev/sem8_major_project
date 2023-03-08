import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QFileDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import cv2

 
class ScreenStack():
    def goToPreviousScreen(self):
        main_widget.setCurrentIndex(main_widget.currentIndex()-1)
        # main_widget.removeWidget(main_widget.widget(main_widget.currentIndex()+1))

    def goToSelectionScreen(self):
        selection_screen = SelectionScreen()
        main_widget.addWidget(selection_screen)
        main_widget.setCurrentIndex(main_widget.currentIndex()+1)

    def goToRecordedVideoScreen(self):
        recorded_screen = RecordedVideoScreen()
        main_widget.addWidget(recorded_screen)
        main_widget.setCurrentIndex(main_widget.currentIndex()+1)
    
    def goToVideoScreen(self):
        video_screen = VideoScreen()
        main_widget.addWidget(video_screen)
        main_widget.setCurrentIndex(main_widget.currentIndex()+1)
    
    def goToExcSelectionScreen(self):
        exc_selection_screen = ExcSelectionScreen()
        main_widget.addWidget(exc_selection_screen)
        main_widget.setCurrentIndex(main_widget.currentIndex()+1)

    def goToExcteachScreen(self):
        exc_teach_screen = ExcTeachScreen()
        main_widget.addWidget(exc_teach_screen)
        main_widget.setCurrentIndex(main_widget.currentIndex()+1)

    def uploadFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', 'C:')
        self.filename.setText(fname[0])


class HomeScreen(QDialog, ScreenStack):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi("screens/ui/home_screen.ui",self)
        self.home_screen_photo.setPixmap(QPixmap('images/1.png'))
        self.getStarted.clicked.connect(self.goToVideoScreen)


class SelectionScreen(QDialog, ScreenStack):
    def __init__(self):
        super(SelectionScreen, self).__init__()
        loadUi("screens/ui/selection_screen.ui",self)
        self.selection_screen_photo.setPixmap(QPixmap('images/2.png'))
        self.pushButton_3.clicked.connect(self.goToRecordedVideoScreen)
        self.gotoexcteachbutton.clicked.connect(self.goToExcteachScreen)
        self.gotoexcselectionbutton.clicked.connect(self.goToExcSelectionScreen)
        self.backButton.clicked.connect(self.goToPreviousScreen)


class RecordedVideoScreen(QDialog, ScreenStack):
    def __init__(self):
        super(RecordedVideoScreen, self).__init__()
        loadUi("screens/ui/recorded_video.ui",self)
        self.recorded_video_screen_photo.setPixmap(QPixmap('images/3.png'))
        self.upload.clicked.connect(self.uploadFile)
        self.backButton.clicked.connect(self.goToPreviousScreen)
        self.startButton.clicked.connect(self.goToVideoScreen)


class ExcSelectionScreen(QDialog, ScreenStack):
    def __init__(self):
        super(ExcSelectionScreen, self).__init__()
        loadUi("screens/ui/exc_selection_screen.ui",self)
        self.exe_selec_screen_photo.setPixmap(QPixmap('images/4.png'))
        self.backButton.clicked.connect(self.goToPreviousScreen)
        self.startButton.clicked.connect(self.goToVideoScreen)


class ExcTeachScreen(QDialog, ScreenStack):
    def __init__(self):
        super(ExcTeachScreen, self).__init__()
        loadUi("screens/ui/exc_teach_screen.ui",self)
        self.trainingbutton.clicked.connect(self.uploadFile)
        self.testingbutton.clicked.connect(self.uploadFile)
        self.backButton.clicked.connect(self.goToPreviousScreen)
        self.startButton.clicked.connect(self.goToVideoScreen)


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        print("Video Thread Start")
        self._run_flag = True

    def run(self):
        # capture from web cam
        # cap = cv2.VideoCapture(1)
        cap = cv2.VideoCapture(r"C:\Users\Deven\Desktop\Projects\B Tech Projects\videos\curls_2.mp4")
        while self._run_flag:
            print("Video Thread running")
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)

        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        print("Video Thread Stop")
        self._run_flag = False
        self.wait()


class VideoScreen(QDialog, ScreenStack):
    def __init__(self):
        super(VideoScreen, self).__init__()
        loadUi("screens/ui/video_screen.ui",self)
        self.backButton.clicked.connect(self.goToPreviousScreen)

        self.disply_width = 640
        self.display_height = 480

        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)

        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread()
        
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        
        # start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        print("Video Thread updating image")
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        print("Video Thread converting")
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


# main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    home_screen = HomeScreen()

    main_widget = QtWidgets.QStackedWidget()
    main_widget.addWidget(home_screen)
    main_widget.showMaximized()
    main_widget.setWindowTitle("Daily Exercise")
    main_widget.show()

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")