from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PyQt5.uic import loadUi

from helpers.validators import is_url

from os import path
import urllib.request
import sys

# FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "../resources/main.ui"))


class MainApp(QMainWindow):
    def __init__(self, ui, parent=None):
        super().__init__(parent)
        QMainWindow.__init__(self)
        loadUi(ui, self)
        self.handle_ui()
        self.handle_buttons()


    def handle_ui(self):
        self.setFixedSize(615, 427)
        self.progressBar.setValue(0)
        self.UrlText.setText("")
        self.setWindowTitle("HUKUDownloader")
        # https://files.wikicourses.net/c/c-c-basics.zip

    def handle_buttons(self):
        self.NormalDownloadButton.clicked.connect(self.handle_normal_download)
        self.BrowseButton.clicked.connect(self.handle_browse_button)
        # self.YouTubeVideoDownloadButton.clicked.connect(self.handle_youtube_video_download)
        # self.PlayListDownloadButton.clicked.connect(self.handle_youtube_playlist_download)

    def handle_progress_bar(self, blocknum, blocksize, totalsize):
        downloaded = blocknum * blocksize
        self.DSizeLcd.display(downloaded / 1000000)
        self.TSizeLcd.display(totalsize / 1000000)
        if totalsize > 0:
            precent = downloaded * 100 // totalsize
        self.progressBar.setValue(precent)
        QApplication.processEvents()

    def handle_browse_button(self):
        save_location = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All files (*.*)")
        self.SaveLocationText.setText(save_location[0])

    def handle_youtube_video_download(self):
        pass

    def handle_youtube_playlist_download(self):
        pass

    def handle_normal_download(self):

        url = self.UrlText.text()
        save_location = self.SaveLocationText.text().strip()
        if not save_location:
            QMessageBox.warning(self, "Download Location", "Please Enter a download location")
            return
        if is_url(url):
            try:
                save_location += f".{url.split('.')[-1]}"
                urllib.request.urlretrieve(url, save_location, self.handle_progress_bar)
                QMessageBox.information(self, "Download Completed", "The Download finished")
            except Exception as e:
                QMessageBox.warning(self, "Download Error", f"The Download failed with exception {e}")


        else:
            QMessageBox.warning(self, "Invalid Url", "Please Enter a Valid url")


# def main():
#     appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
#     window = MainApp()
#     window.show()
#     exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
#     sys.exit(exit_code)


class AppContext(ApplicationContext):
    def run(self):
        self.window.resize(250, 150)
        self.window.show()
        return appctxt.app.exec_()

    def get_design(self):
        qtCreatorFile = self.get_resource("main.ui")
        return qtCreatorFile

    @cached_property
    def window(self):
        return MainApp(self.get_design())


if __name__ == '__main__':
    appctxt = AppContext()  # 1. Instantiate ApplicationContext
    exit_code = appctxt.run()
    sys.exit(exit_code)
    # window.resize(250, 150)
    # window.show()
    # exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    # sys.exit(exit_code)
