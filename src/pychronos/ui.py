from PyQt5.QtCore import QTimer, Qt, QDateTime
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from pychronos.constants import IN_PROGRESS, LAST_MINUTES, BREAK
from pychronos.sound import play_beep_started, play_beep_finished, toggle_sound
from pychronos.timer import calculate_timer, get_status


class ChronosWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chronos")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setFixedSize(180, 100)

        self.old_pos = None
        self.last_status = None

        self._setup_ui()
        self._play_startup_beep()
        self._start_timer()

    def _play_startup_beep(self):
        if self.last_status is None:
            play_beep_started()

    def _setup_ui(self):
        self.layout = QVBoxLayout()
        self.time_label = QLabel("00:00")
        self.time_label.setFont(QFont("Courier", 36, QFont.Bold))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.time_label)
        self.setLayout(self.layout)

        self.close_button = QPushButton("X", self)
        self.close_button.setFixedSize(24, 24)
        self.close_button.move(self.width() - 28, 4)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        self.close_button.clicked.connect(self.close)

        self.sound_toggle = QPushButton("🔊", self)
        self.sound_toggle.setFixedSize(24, 24)
        self.sound_toggle.move(self.width() - 56, 4)
        self.sound_toggle.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                color: #ffcc00;
            }
        """)
        self.sound_toggle.clicked.connect(self.handle_toggle_sound)

    def _start_timer(self):
        self.update_timer()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def update_timer(self):
        now = QDateTime.currentDateTime()
        minutes, seconds = calculate_timer(now)
        status = get_status(now)

        if self.last_status is None:
            play_beep_started()
        if status != self.last_status and self.last_status is None:
            if status == IN_PROGRESS:
                play_beep_started()
            elif status == BREAK:
                play_beep_finished()

        self.last_status = status

        color = {
            IN_PROGRESS: "#80B3FF",
            LAST_MINUTES: "#FF8080",
            BREAK: "#37C8AB"
        }.get(status, "#80B3FF")

        self.time_label.setText(f"{minutes:02}:{seconds:02}")
        self.setStyleSheet(f"background-color: {color}; color: white;")

    def handle_toggle_sound(self):
        enabled = toggle_sound()
        self.sound_toggle.setText("🔊" if enabled else "🔇")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None
