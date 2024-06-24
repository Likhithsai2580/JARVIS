import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
import webbrowser

from interface import Ui_JARVIS  # Assuming Ui_JARVIS is defined in interface.py

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_JARVIS()
        self.ui.setupUi(self)
        self.connect_buttons()

    def connect_buttons(self):
        self.ui.home.clicked.connect(self.show_home)
        self.ui.advance.clicked.connect(self.show_advance)
        self.ui.about.clicked.connect(self.show_about)
        self.ui.pushButton.clicked.connect(lambda: self.open_url("https://google.com"))
        self.ui.pushButton_2.clicked.connect(lambda: self.open_url("https://github.com"))
        self.ui.pushButton_3.clicked.connect(lambda: self.open_url("https://youtube.com"))
        self.ui.pushButton_4.clicked.connect(lambda: self.open_url("https://github.com/Likhithsai2580/Automated-YouTube-Video-Creator"))
        self.ui.pushButton_5.clicked.connect(lambda: self.open_url("https://likhithsai2580.github.io/My-Website/"))

    def start_external_process(self):
        if self.external_thread and self.external_thread.isRunning():
            return

        # Replace 'python your_script.py' with your actual command
        command = ['python', 'JARVIS.py']
        self.external_process = ExternalProcess(command)
        self.external_thread = QThread()
        self.external_process.moveToThread(self.external_thread)

        self.external_process.update_text.connect(self.append_text)
        self.external_thread.started.connect(self.external_process.run)

        self.external_thread.start()

    def append_text(self, text):
        cursor = self.ui.console.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.ui.console.setTextCursor(cursor)
        self.ui.console.ensureCursorVisible()

    def show_home(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.load_gif("assests/initalizing.gif", self.ui.label_3)
        self.load_gif("assests/loop.gif", self.ui.label_9)
        self.load_gif("assests/loop2.gif", self.ui.label_10)
        self.load_gif("assests/loading.gif", self.ui.loading)
        self.start_external_process()
        QtCore.QTimer.singleShot(20000, self.load_second_gif)

    def load_gif(self, path, label):
        movie = QtGui.QMovie(path)
        label.setMovie(movie)
        label.setScaledContents(True)  # Ensure the GIF scales with the label
        movie.start()

    def load_second_gif(self):
        self.ui.loading.clear()
        self.load_gif("assests/iron-man.gif", self.ui.loading)

    def show_advance(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def show_about(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def open_url(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
