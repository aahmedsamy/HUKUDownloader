import os
import sys

import requests
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PyQt5.uic import loadUi
from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property
from helpers.convertions import convert_bytes
from helpers.validators import is_url

# download_ui, _ = loadUiType(path.join(path.dirname(__file__), "../resources/download.ui"))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_PATH = os.path.join(BASE_DIR, 'resources/base/')


class Download(QMainWindow):
    def __init__(self, parent, total_size, url, save_location, **kwargs):
        super().__init__(parent)
        loadUi(RESOURCES_PATH + 'download.ui', self)
        self.parent = parent
        self.parent.UrlText.setText("")
        self.parent.SaveLocationText.setText("")
        self.parent.TSizeLcd.display("0")
        self.total_size = total_size
        self.url = url
        self.save_location = save_location
        self.file_name = self.save_location.split('/')[-1]
        self.handle_ui()
        self.handle_buttons()

    def handle_ui(self):
        self.setFixedSize(713, 376)
        self.setWindowTitle(f"Downloading {self.file_name}")
        self.FileNameLabel.setText(self.file_name)
        self.DownloadUrlLabel.setText(self.url)
        self.handle_total_size_lcd(self.total_size)

    def handle_buttons(self):
        self.StopButton.clicked.connect(self.handle_stop_button)

    def handle_stop_button(self):
        pass

    def handle_total_size_lcd(self, total_size):
        sz_data = convert_bytes(self.total_size)
        self.TSizeLcd.display(sz_data['value'])
        self.tsLable.setText(f"Total size({sz_data['type']})")

    def handle_progress_bar(self, blocknum, blocksize, totalsize):
        downloaded = blocknum * blocksize
        remaining = totalsize - downloaded
        ds_data = convert_bytes(downloaded)
        self.dsLabel.setText(f"Downloaded Size({ds_data['type']})")
        rs_data = convert_bytes(remaining)
        self.RSLabel.setText(f"Downloaded Size({rs_data['type']})")
        self.RSizeLcd.display(rs_data['value'])
        self.DSizeLcd.display(ds_data['value'])
        if totalsize > 0:
            precent = downloaded * 100 // totalsize
            self.progressBar.setValue(precent)
        QApplication.processEvents()

    def load_ui(self):
        return self.show()

    def start(self, **kwargs):
        self.load_ui()
        url = self.url
        save_location = self.save_location
        res = dict()
        headers = dict()
        if 'headers' in kwargs.keys():
            headers = kwargs['headers']
        headers[
            'User-agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        kwargs['headers'] = headers
        r = requests.get(url, stream=True, **kwargs)
        res['file_name'] = save_location.split('/')[-1]
        res['url'] = url
        try:
            with open(save_location, "wb") as f:
                i = 1
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        self.handle_progress_bar(i, 1024, self.total_size)
                        i = i + 1
            res['status'] = "success"
            res['time'] = ''
            res['total_size'] = self.total_size
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


class MainApp(QMainWindow):
    def __init__(self, ui, parent=None):
        super().__init__(parent)
        loadUi(ui, self)
        self.handle_ui()
        self.handle_buttons()
        self.handle_texts()
        self.total_size = 0

    def handle_ui(self):
        self.setFixedSize(605, 353)
        self.UrlText.setText("")
        self.setWindowTitle("HUKUDownloader")
        # https://files.wikicourses.net/c/c-c-basics.zip

    def get_total_size(self, url):
        res = requests.head(url, allow_redirects=True)
        return int(res.headers['content-length'])

    def handle_texts(self):
        self.UrlText.textChanged.connect(self.handle_total_size_lcd)

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

    def handle_buttons(self):
        self.NormalDownloadButton.clicked.connect(self.handle_normal_download)
        self.BrowseButton.clicked.connect(self.handle_browse_button)
        # self.YouTubeVideoDownloadButton.clicked.connect(self.handle_youtube_video_download)
        # self.PlayListDownloadButton.clicked.connect(self.handle_youtube_playlist_download)

    def handle_browse_button(self):
        save_location = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All files (*.*)")
        self.SaveLocationText.setText(save_location[0])

    def handle_youtube_video_download(self):
        pass

    def handle_youtube_playlist_download(self):
        pass

    def handle_normal_download(self):

        url = self.UrlText.text().strip()
        save_location = self.SaveLocationText.text().strip()
        if not save_location:
            QMessageBox.warning(self, "Download Location", "Please Enter a download location")
            return
        if is_url(url):

            download = Download(self, self.total_size, url, save_location)
            download.start()
            self.UrlText.setText("")
            self.SaveLocationText.setText("")
            # self.download_file(url, save_location)
            # threading.Thread(target=self.download_file, args=(url, save_location))
            # urllib.request.urlretrieve(url, save_location, self.handle_progress_bar)
            # QMessageBox.information(self, "Download Completed", "The Download finished")
        else:
            QMessageBox.warning(self, "Invalid Url", "Please Enter a Valid url")


class AppContext(ApplicationContext):
    def run(self):
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
# https://doc-0c-24-docs.googleusercontent.com/docs/securesc/eta4tnfkm2srtblrsqufrc1om6v6ec1k/3sgb340b7uq59raau630ibq5r3b4gnuh/1591282575000/15530971891307717937/18240035718256758723/11ltIeHHwFWd5IsBDf-YNY4JsGljfUs3I?e=download&authuser=0
