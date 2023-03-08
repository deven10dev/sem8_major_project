from PyQt5.QtWidgets import QFileDialog
 from screens.selection_screen import SelectionScreen

class ScreenStack():
    def goToPreviousScreen(self):
        main_widget.setCurrentIndex(main_widget.currentIndex()-1)
        main_widget.removeWidget(main_widget.widget(main_widget.currentIndex()+1))

    def goToSelectionScreen(self):
        selection_screen = SelectionScreen()
        main_widget.addWidget(selection_screen)
        main_widget.setCurrentIndex(main_widget.currentIndex()+1)

    # def goToRecordedVideoScreen(self):
    #     recorded_screen = RecordedVideoScreen()
    #     main_widget.addWidget(recorded_screen)
    #     main_widget.setCurrentIndex(main_widget.currentIndex()+1)
    
    # def goToVideoScreen(self):
    #     video_screen = VideoScreen()
    #     main_widget.addWidget(video_screen)
    #     main_widget.setCurrentIndex(main_widget.currentIndex()+1)
    
    # def goToExcSelectionScreen(self):
    #     exc_selection_screen = ExcSelectionScreen()
    #     main_widget.addWidget(exc_selection_screen)
    #     main_widget.setCurrentIndex(main_widget.currentIndex()+1)

    # def goToExcteachScreen(self):
    #     exc_teach_screen = ExcTeachScreen()
    #     main_widget.addWidget(exc_teach_screen)
    #     main_widget.setCurrentIndex(main_widget.currentIndex()+1)

    def uploadFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', 'C:')
        self.filename.setText(fname[0])
