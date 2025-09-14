from PyQt5.QtCore import QThread, pyqtSignal
from hide_methods import hide_file_in_image

class HideThread(QThread):
    result_signal = pyqtSignal(bool, str)

    def __init__(self, image_path, secret_path, output_path):
        super().__init__()
        self.image_path = image_path
        self.secret_path = secret_path
        self.output_path = output_path

    def run(self):
        success, result = hide_file_in_image(self.image_path, self.secret_path, self.output_path)
        self.result_signal.emit(success, result)
