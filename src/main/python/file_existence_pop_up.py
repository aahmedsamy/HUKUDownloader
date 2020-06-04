from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget
from PyQt5.uic import loadUiType

import os
from os import path
import urllib.request
import sys

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "../resources/file_existence_pop_up.resources"))


class FileExistencePopUp(QWidget, FORM_CLASS):
    def __init__(self, parent=None):
        super(FileExistencePopUp, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.handle_ui()
        self.handle_buttons()

    def handle_ui(self):
        self.setFixedSize(615, 201)

    def handle_buttons(self):
        self.CancelButton.clicked.connect(self.handle_cancel)
        self.ReplaceButton.clicked.connect(self.handle_replace)
        self.DownloadButton.clicked.connect(self.handle_download)


    def handle_save_location(self):
        self.SaveLocationText.textChanged.connect(self.handle_buttons)

    def handle_download(self):

        url = self.UrlText.text()
        save_location = self.SaveLocationText.text().strip()
        if not save_location:
            QMessageBox.warning(self, "Download Location", "Please Enter a download location")
            return
        if is_url(url):
            try:
                save_location += f"/{url.split('/')[-1]}"
                if check_file_existance(save_location):

                urllib.request.urlretrieve(url, save_location, self.handle_progress_bar)
                self.progressBar.setValue(0)
                QMessageBox.information(self, "Download Completed", "The Download finished")
            except Exception as e:
                QMessageBox.warning(self, "Download Error", f"The Download failed with exception {e}")


        else:
            QMessageBox.warning(self, "Invalid Url", "Please Enter a Valid url")


# https://aahmedsamy.me
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
