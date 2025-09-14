from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, 
    QHBoxLayout, QComboBox, QLineEdit, QDateTimeEdit, QSpinBox
)
from PyQt5.QtCore import Qt, QDateTime, QTimer, QTime
from PyQt5.QtGui import QFont

class VaultUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛡️ SilentVault - Secure & Stealth File Locker")
        self.setFixedSize(600, 520)
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: Arial;")

        # Title
        title = QLabel("🔐 SilentVault")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # Current Time Display
        self.live_time_label = QLabel()
        self.live_time_label.setFont(QFont("Arial", 12))
        self.live_time_label.setStyleSheet("color: lightgreen;")
        self.live_time_label.setAlignment(Qt.AlignCenter)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # update every 1 second
        self.update_time()

        # File chooser
        self.file_label = QLabel("No file selected")
        self.file_button = QPushButton("📂 Choose File/Folder")
        self.file_button.clicked.connect(self.choose_file)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_button)
        file_layout.addWidget(self.file_label)

        # Method dropdown
        self.method_box = QComboBox()
        self.method_box.addItems(["Steganography", "Hidden Folder", "NTFS Stream", "Time Lock"])
        self.method_box.setStyleSheet("background-color: #333333; color: white;")

        # Time-based Lock UI (Hour + Minute + AM/PM)
        self.start_label = QLabel("Start Time:")
        self.start_hour = QSpinBox()
        self.start_hour.setRange(1, 12)
        self.start_hour.setValue(9)

        self.start_minute = QSpinBox()
        self.start_minute.setRange(0, 59)
        self.start_minute.setValue(0)

        self.start_ampm = QComboBox()
        self.start_ampm.addItems(["AM", "PM"])

        self.end_label = QLabel("End Time:")
        self.end_hour = QSpinBox()
        self.end_hour.setRange(1, 12)
        self.end_hour.setValue(5)

        self.end_minute = QSpinBox()
        self.end_minute.setRange(0, 59)
        self.end_minute.setValue(0)

        self.end_ampm = QComboBox()
        self.end_ampm.addItems(["AM", "PM"])

        time_layout = QHBoxLayout()
        time_layout.addWidget(self.start_label)
        time_layout.addWidget(self.start_hour)
        time_layout.addWidget(QLabel(":"))
        time_layout.addWidget(self.start_minute)
        time_layout.addWidget(self.start_ampm)
        time_layout.addSpacing(20)
        time_layout.addWidget(self.end_label)
        time_layout.addWidget(self.end_hour)
        time_layout.addWidget(QLabel(":"))
        time_layout.addWidget(self.end_minute)
        time_layout.addWidget(self.end_ampm)

        # Unlock trigger + date
        self.trigger_input = QLineEdit()
        self.trigger_input.setPlaceholderText("Enter Unlock Passphrase")

        self.date_picker = QDateTimeEdit(QDateTime.currentDateTime())
        self.date_picker.setCalendarPopup(True)

        # Action buttons
        self.hide_button = QPushButton("🔒 Hide")
        self.unhide_button = QPushButton("🔓 Unhide")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.hide_button)
        btn_layout.addWidget(self.unhide_button)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.live_time_label)
        layout.addLayout(file_layout)
        layout.addWidget(self.method_box)
        layout.addWidget(QLabel("🔑 Unlock Passphrase:"))
        layout.addWidget(self.trigger_input)
        layout.addWidget(QLabel("📅 Optional Unlock Date & Time:"))
        layout.addWidget(self.date_picker)
        layout.addLayout(time_layout)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        self.live_time_label.setText(f"🕒 Current Time: {current_time}")

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose a file to hide")
        if file_path:
            self.file_label.setText(file_path)
        else:
            self.file_label.setText("No file selected")
