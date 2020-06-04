import sys
from os import path

import requests
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PyQt5.uic import loadUi
from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property
from helpers.convertions import convert_bytes
from helpers.validators import is_url


# FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "../resources/main.ui"))


class MainApp(QMainWindow):
    def __init__(self, ui, parent=None):
        super().__init__(parent)
        QMainWindow.__init__(self)
        loadUi(ui, self)
        self.handle_ui()
        self.handle_buttons()
        self.handle_texts()
        self.total_size = 0

    def handle_ui(self):
        self.setFixedSize(615, 427)
        self.progressBar.setValue(0)
        self.UrlText.setText("")
        self.setWindowTitle("HUKUDownloader")
        # https://files.wikicourses.net/c/c-c-basics.zip

    def get_total_size(self, url):
        res = requests.head(url)
        return int(res.headers['content-length'])

    def handle_total_size_lcd(self):
        url = self.UrlText.text().strip()
        if is_url(url):
            try:
                # it slows down the inserting the download url
                self.total_size = self.get_total_size(url)
                sz_data = convert_bytes(self.total_size)
                self.TSizeLcd.display(sz_data['value'])
                self.tsLable.setText(f"Total size({sz_data['type']})")
            except:
                pass

    def handle_texts(self):
        self.UrlText.textChanged.connect(self.handle_total_size_lcd)

    def handle_buttons(self):
        self.NormalDownloadButton.clicked.connect(self.handle_normal_download)
        self.BrowseButton.clicked.connect(self.handle_browse_button)
        # self.YouTubeVideoDownloadButton.clicked.connect(self.handle_youtube_video_download)
        # self.PlayListDownloadButton.clicked.connect(self.handle_youtube_playlist_download)

    def handle_progress_bar(self, blocknum, blocksize, totalsize):
        downloaded = blocknum * blocksize
        ds_data = convert_bytes(downloaded)
        self.dsLabel.setText(f"Downloaded Size({ds_data['type']})")
        self.DSizeLcd.display(ds_data['value'])
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

    def download_file(self, url, location, **kwargs):
        res = dict()
        headers = dict()
        if 'headers' in kwargs.keys():
            headers = kwargs['headers']
        headers['user-agent'] = "HUKUDownloader/1.0.0"
        kwargs['headers'] = headers
        r = requests.get(url, stream=True, **kwargs)
        res['file_name'] = url.split('/')[-1]
        res['url'] = url
        try:
            with open(location, "wb") as f:
                i = 1
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        self.handle_progress_bar(i, 1024, self.total_size)
                        i = i + 1
            res['status'] = "success"
            res['time'] = ''
            res['total_size'] = ''
            res['downloaded_size'] = ''
        except Exception as e:
            res['status'] = "fail"
            res['exception'] = e

        if res['status'] == "success":
            message = f"Downloaded file {res['file_name']} from {res['url']} in {res['time']}.\n" \
                      f"{res['downloaded_size']}/{res['total_size']} downloaded"
            QMessageBox.information(self, "Download Completed!", message)
        else:
            QMessageBox.warning(self, f"Download Error",
                                f"Download {res['file_name']} from {res['url']} failed with exception {res['exception']}")

    def handle_normal_download(self):

        url = self.UrlText.text().strip()
        save_location = self.SaveLocationText.text().strip()
        if not save_location:
            QMessageBox.warning(self, "Download Location", "Please Enter a download location")
            return
        if is_url(url):
            if not path.isfile(save_location):
                save_location += f".{url.split('.')[-1]}"
            self.download_file(url, save_location)
            # threading.Thread(target=self.download_file, args=(url, save_location))
            # urllib.request.urlretrieve(url, save_location, self.handle_progress_bar)
            # QMessageBox.information(self, "Download Completed", "The Download finished")
        else:
            QMessageBox.warning(self, "Invalid Url", "Please Enter a Valid url")


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

# https://57-2.files-mutaz.net/W7_Pro_SP1_En_x64.iso
