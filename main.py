import sys
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit


class TimeTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Time Tracker")
        self.setGeometry(100, 100, 300, 300)
        self.setFixedSize(300, 300)

        self.time_label = QLabel("00:00:00", self)
        self.time_label.setStyleSheet("font-size: 24px")
        self.time_label.setAlignment(Qt.AlignCenter)

        self.rate_label = QLabel("Ставка в час (руб.):", self)
        self.rate_input = QLineEdit(self)
        self.rate_input.setPlaceholderText("Введите ставку")

        self.start_button = QPushButton("Старт", self)
        self.start_button.clicked.connect(self.start_timer)

        self.stop_button = QPushButton("Стоп", self)
        self.stop_button.clicked.connect(self.stop_timer)
        self.stop_button.setEnabled(False)

        self.reset_button = QPushButton("Сброс", self)
        self.reset_button.clicked.connect(self.reset_timer)
        self.reset_button.setEnabled(False)

        self.total_label = QLabel("Всего заработано (руб.):", self)
        self.total_earned_label = QLabel("0.00", self)
        self.total_earned_label.setStyleSheet("font-size: 18px")

        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        layout.addWidget(self.rate_label)
        layout.addWidget(self.rate_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.total_label)
        layout.addWidget(self.total_earned_label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.current_time = QTime(0, 0)
        self.is_timer_running = False
        self.rate = 0.0
        self.total_earned = 0.0

    def start_timer(self):
        rate_text = self.rate_input.text()
        try:
            self.rate = float(rate_text)
        except ValueError:
            self.rate = 0.0

        self.is_timer_running = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.reset_button.setEnabled(False)
        self.timer.start(1000)

    def stop_timer(self):
        self.is_timer_running = False
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.reset_button.setEnabled(True)
        self.timer.stop()

    def reset_timer(self):
        self.current_time = QTime(0, 0)
        self.total_earned = 0.0
        self.time_label.setText(self.current_time.toString("hh:mm:ss"))
        self.total_earned_label.setText("0.00")
        self.reset_button.setEnabled(False)

    def update_time(self):
        self.current_time = self.current_time.addSecs(1)
        self.time_label.setText(self.current_time.toString("hh:mm:ss"))

        if self.is_timer_running:
            self.total_earned += self.rate / 3600
            self.total_earned_label.setText(f"{self.total_earned:.2f}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
                        QWidget {
                        background-color: #2c3e50;
                        color: #ffffff;
                    }
                    
                    QLabel {
                        color: #ffffff;
                    }
                    
                    QLineEdit {
                        background-color: #34495e;
                        border: 1px solid #2c3e50;
                        border-radius: 5px;
                        padding: 5px;
                        color: #ffffff;
                    }
                    
                    QPushButton {
                        background-color: #3498db;
                        color: #ffffff;
                        border: none;
                        border-radius: 5px;
                        padding: 5px 10px;
                    }
                    
                    QPushButton:hover {
                        background-color: #5dade2;
                    }
                    
                    QPushButton:pressed {
                        background-color: #2980b9;
                    }
                    
                    QPushButton:disabled {
                        background-color: #2980b9;
                        color: #bdc3c7;
                    }
    """)
    window = TimeTracker()
    window.show()
    sys.exit(app.exec_())
