import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog
from PyQt5.QtCore import QTimer
from ui import VaultUI
from hide_methods import (
    hide_as_hidden_folder, unhide_hidden_folder,
    hide_in_ntfs_stream, extract_from_ntfs_stream,
    hide_file_in_image, extract_file_from_image
)
from threaded_tasks import HideThread

class App(VaultUI):
    def __init__(self):
        super().__init__()
        self.hide_button.clicked.connect(self.perform_hide)
        self.unhide_button.clicked.connect(self.perform_unhide)

        self.last_locked_path = None

        # Start auto-check timer
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.auto_check_unlock)
        self.check_timer.start(5000)  # Check every 5 seconds

    def convert_to_24h(self, hour, minute, ampm):
        if ampm == "PM" and hour != 12:
            hour += 12
        if ampm == "AM" and hour == 12:
            hour = 0
        return hour, minute

    def perform_hide(self):
        method = self.method_box.currentText()

        if method == "Steganography":
            image_path, _ = QFileDialog.getOpenFileName(self, "Select PNG image", "", "PNG Files (*.png)")
            secret_path = self.file_label.text()
            if not image_path or not secret_path or secret_path == "No file selected":
                QMessageBox.warning(self, "Missing", "Please select both image and secret file.")
                return
            output_path = "output_stego.png"
            self.thread = HideThread(image_path, secret_path, output_path)
            self.thread.result_signal.connect(self.handle_hide_result)
            self.thread.start()
            QMessageBox.information(self, "Started", "Hiding in progress...")

        elif method == "Hidden Folder":
            path, _ = QFileDialog.getOpenFileName(self, "Select File to Hide")
            if path:
                success, msg = hide_as_hidden_folder(path)
                QMessageBox.information(self, "Result", msg) if success else QMessageBox.critical(self, "Error", msg)

        elif method == "NTFS Stream":
            cover, _ = QFileDialog.getOpenFileName(self, "Select Cover File")
            secret, _ = QFileDialog.getOpenFileName(self, "Select Secret File")
            if cover and secret:
                success, msg = hide_in_ntfs_stream(cover, secret)
                QMessageBox.information(self, "Result", msg) if success else QMessageBox.critical(self, "Error", msg)

        elif method == "Time Lock":
            folder_path = QFileDialog.getExistingDirectory(self, "Select Folder to Lock/Unlock")
            if not folder_path:
                return

            self.last_locked_path = folder_path

            sh = self.start_hour.value()
            sm = self.start_minute.value()
            sap = self.start_ampm.currentText()

            eh = self.end_hour.value()
            em = self.end_minute.value()
            eap = self.end_ampm.currentText()

            start_hr, start_min = self.convert_to_24h(sh, sm, sap)
            end_hr, end_min = self.convert_to_24h(eh, em, eap)

            now = datetime.now()
            now_minutes = now.hour * 60 + now.minute
            start_minutes = start_hr * 60 + start_min
            end_minutes = end_hr * 60 + end_min

            if start_minutes <= now_minutes < end_minutes:
                os.system(f'attrib -h -s "{folder_path}"')
                QMessageBox.information(self, "Unlocked ✅", f"Folder is now unlocked.\nTime: {sh}:{sm:02d} {sap} - {eh}:{em:02d} {eap}")
            else:
                os.system(f'attrib +h +s "{folder_path}"')
                QMessageBox.information(self, "Locked 🔒", f"Folder is locked outside allowed time.")

    def auto_check_unlock(self):
        if not self.last_locked_path:
            return

        sh = self.start_hour.value()
        sm = self.start_minute.value()
        sap = self.start_ampm.currentText()

        eh = self.end_hour.value()
        em = self.end_minute.value()
        eap = self.end_ampm.currentText()

        start_hr, start_min = self.convert_to_24h(sh, sm, sap)
        end_hr, end_min = self.convert_to_24h(eh, em, eap)

        now = datetime.now()
        now_minutes = now.hour * 60 + now.minute
        start_minutes = start_hr * 60 + start_min
        end_minutes = end_hr * 60 + end_min

        if start_minutes <= now_minutes < end_minutes:
            os.system(f'attrib -h -s "{self.last_locked_path}"')
        else:
            os.system(f'attrib +h +s "{self.last_locked_path}"')

    def handle_hide_result(self, success, result):
        if success:
            QMessageBox.information(self, "Success", f"Hidden inside image:\n{result}")
        else:
            QMessageBox.critical(self, "Error", result)

    def perform_unhide(self):
        method = self.method_box.currentText()

        if method == "Steganography":
            image_path, _ = QFileDialog.getOpenFileName(self, "Select Stego Image", "", "PNG Files (*.png)")
            if image_path:
                success, result = extract_file_from_image(image_path)
                QMessageBox.information(self, "Success", result) if success else QMessageBox.critical(self, "Error", result)

        elif method == "Hidden Folder":
            path, _ = QFileDialog.getOpenFileName(self, "Select File to Unhide")
            if path:
                success, msg = unhide_hidden_folder(path)
                QMessageBox.information(self, "Success", msg) if success else QMessageBox.critical(self, "Error", msg)

        elif method == "NTFS Stream":
            cover, _ = QFileDialog.getOpenFileName(self, "Select Cover File")
            output, _ = QFileDialog.getSaveFileName(self, "Save Extracted File As", "recovered_file")
            if cover and output:
                success, msg = extract_from_ntfs_stream(cover, output)
                QMessageBox.information(self, "Success", msg) if success else QMessageBox.critical(self, "Error", msg)

def main():
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
